"""Supabase Dual-Mode Backend & Realtime Broadcast Service for SIH26184.

Features:
- Seamless cloud integration with hosted Supabase PostgreSQL instances.
- Supabase Realtime Broadcast: Pushes instant high-risk mule alerts and ATM predictions
  directly to frontend dashboards via WebSocket channels.
- Supabase Storage: Secure storage for victim evidence files, bank statements, and FIR PDFs.
- Resilient Dual-Mode: Automatically detects whether Supabase is configured; falls back
  to local PostgreSQL and local disk storage when running offline.
"""

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import httpx
from loguru import logger

from api.config import get_settings

settings = get_settings()


class SupabaseService:
    """Enterprise client for Supabase Realtime, Storage, and Database integration."""

    def __init__(self):
        s = get_settings()
        self.url = s.supabase_url.rstrip("/") if s.supabase_url else ""
        self.anon_key = s.supabase_key or ""
        self.service_role_key = s.supabase_service_role_key or self.anon_key
        self.bucket = s.supabase_storage_bucket or "evidence"
        self.is_enabled = bool(self.url and (self.anon_key or self.service_role_key))

        if self.is_enabled:
            logger.info(f"✓ Supabase Service configured for endpoint: {self.url}")
        else:
            logger.info("Supabase credentials not set; running in local PostgreSQL & disk storage mode.")

    def _get_headers(self, use_service_role: bool = False) -> Dict[str, str]:
        key = self.service_role_key if use_service_role else self.anon_key
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

    async def broadcast_event(self, channel: str, event: str, payload: Dict[str, Any]) -> bool:
        """Broadcast live events to Supabase Realtime channels.
        
        Examples:
        - channel: "police_alerts", event: "NEW_HIGH_RISK_MULE", payload: {...}
        - channel: "victim_updates", event: "COMPLAINT_STATUS_CHANGED", payload: {...}
        """
        if not self.is_enabled:
            logger.debug(f"[Local Broadcast] Channel: {channel} | Event: {event} | Payload: {payload.get('id', '')}")
            return True

        url = f"{self.url}/realtime/v1/api/broadcast"
        body = {
            "messages": [
                {
                    "topic": f"realtime:{channel}",
                    "event": event,
                    "payload": {
                        **payload,
                        "broadcast_time": datetime.now().isoformat(),
                    },
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.post(url, headers=self._get_headers(use_service_role=True), json=body)
                if res.status_code in [200, 201, 202, 204]:
                    return True
                logger.warning(f"Supabase broadcast status {res.status_code}: {res.text[:100]}")
                return False
        except Exception as e:
            logger.warning(f"Supabase broadcast connection note: {e}")
            return False

    async def upload_evidence_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
    ) -> Dict[str, Any]:
        """Upload evidence to Supabase Storage bucket, or fallback to local disk."""
        if not self.is_enabled:
            # Fallback to local uploads directory
            upload_dir = Path("data/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            local_path = upload_dir / filename
            with open(local_path, "wb") as f:
                f.write(file_bytes)
            return {
                "storage": "local_disk",
                "filename": filename,
                "file_path": str(local_path),
                "url": f"/static/uploads/{filename}",
            }

        url = f"{self.url}/storage/v1/object/{self.bucket}/{filename}"
        headers = {
            "apikey": self.service_role_key,
            "Authorization": f"Bearer {self.service_role_key}",
            "Content-Type": content_type,
            "x-upsert": "true",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, headers=headers, content=file_bytes)
                if res.status_code in [200, 201]:
                    public_url = f"{self.url}/storage/v1/object/public/{self.bucket}/{filename}"
                    return {
                        "storage": "supabase",
                        "bucket": self.bucket,
                        "filename": filename,
                        "url": public_url,
                    }
                else:
                    logger.warning(f"Supabase storage upload returned {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Supabase storage upload error: {e}")

        # Local fallback on error
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        local_path = upload_dir / filename
        with open(local_path, "wb") as f:
            f.write(file_bytes)
        return {
            "storage": "local_disk_fallback",
            "filename": filename,
            "file_path": str(local_path),
            "url": f"/static/uploads/{filename}",
        }

    async def insert_victim(
        self,
        victim_id: str,
        complaint_id: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        upi_id: Optional[str] = None,
    ) -> bool:
        """Insert a victim record into Supabase PostgreSQL via PostgREST."""
        if not self.is_enabled:
            return False

        url = f"{self.url}/rest/v1/victims"
        payload = {
            "victim_id": victim_id,
            "complaint_id": complaint_id,
            "email": email,
            "upi_id": upi_id,
        }
        # Filter None values
        payload = {k: v for k, v in payload.items() if v is not None}

        headers = {
            **self._get_headers(use_service_role=True),
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code in [200, 201, 204]:
                    logger.info(f"✓ Victim {victim_id} synced to Supabase")
                    return True
                logger.warning(f"Supabase insert_victim status {res.status_code}: {res.text}")
                return False
        except Exception as e:
            logger.warning(f"Supabase insert_victim network error: {e}")
            return False

    async def insert_complaint(
        self,
        complaint_id: str,
        amount: float,
        fraud_type: str,
        victim_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        fraudster_upi: Optional[str] = None,
        fraudster_phone: Optional[str] = None,
        fraudster_bank: Optional[str] = None,
        transaction_reference: Optional[str] = None,
        status: str = "SUBMITTED",
    ) -> bool:
        """Insert a complaint record into Supabase PostgreSQL via PostgREST."""
        if not self.is_enabled:
            return False

        url = f"{self.url}/rest/v1/complaints"
        payload = {
            "complaint_id": complaint_id,
            "victim_id": victim_id,
            "amount": float(amount),
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "fraud_type": fraud_type,
            "fraudster_upi": fraudster_upi,
            "fraudster_phone": fraudster_phone,
            "fraudster_bank": fraudster_bank,
            "transaction_reference": transaction_reference,
            "status": status,
        }
        # Filter None values
        payload = {k: v for k, v in payload.items() if v is not None}

        headers = {
            **self._get_headers(use_service_role=True),
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code in [200, 201, 204]:
                    logger.info(f"✓ Complaint {complaint_id} synced to Supabase")
                    # Also broadcast realtime alert for police dashboard
                    await self.broadcast_event(
                        channel="police_alerts",
                        event="NEW_COMPLAINT_SUBMITTED",
                        payload={
                            "complaint_id": complaint_id,
                            "amount": amount,
                            "fraud_type": fraud_type,
                            "fraudster_upi": fraudster_upi,
                        },
                    )
                    return True
                logger.warning(f"Supabase insert_complaint status {res.status_code}: {res.text}")
                return False
        except Exception as e:
            logger.warning(f"Supabase insert_complaint network error: {e}")
            return False

    async def get_complaint(self, complaint_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a complaint by ID directly from Supabase PostgreSQL."""
        if not self.is_enabled:
            return None

        url = f"{self.url}/rest/v1/complaints?complaint_id=eq.{complaint_id}&select=*"
        headers = self._get_headers(use_service_role=True)

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    rows = res.json()
                    if rows and len(rows) > 0:
                        return rows[0]
                return None
        except Exception as e:
            logger.warning(f"Supabase get_complaint error: {e}")
            return None

    async def update_complaint_status(self, complaint_id: str, new_status: str) -> bool:
        """Update complaint status in Supabase."""
        if not self.is_enabled:
            return False

        url = f"{self.url}/rest/v1/complaints?complaint_id=eq.{complaint_id}"
        headers = {
            **self._get_headers(use_service_role=True),
            "Prefer": "return=minimal",
        }
        payload = {
            "status": new_status,
            "updated_at": datetime.utcnow().isoformat(),
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.patch(url, headers=headers, json=payload)
                return res.status_code in [200, 204]
        except Exception as e:
            logger.warning(f"Supabase update_complaint_status error: {e}")
            return False

    async def insert_user(
        self,
        user_id: str,
        username: str,
        email: str,
        password_hash: str = "oauth_managed",
        role: str = "CONSTABLE",
        station: Optional[str] = None,
        badge_number: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> bool:
        """Insert or sync a user record into Supabase PostgreSQL public.users table."""
        if not self.is_enabled:
            return False

        # Ensure role matches allowed Supabase userrole enum ('ADMIN', 'INSPECTOR', 'CONSTABLE', 'CITIZEN')
        valid_role = role.upper() if role.upper() in ["ADMIN", "INSPECTOR", "CONSTABLE", "CITIZEN"] else "CONSTABLE"

        url = f"{self.url}/rest/v1/users"
        payload = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "role": valid_role,
            "station": station,
            "badge_number": badge_number,
            "phone": phone,
            "is_active": True,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        headers = {
            **self._get_headers(use_service_role=True),
            "Prefer": "resolution=merge-duplicates,return=minimal",
        }

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code in [200, 201, 204]:
                    logger.info(f"✓ User {username} ({email}) synced to Supabase public.users")
                    return True
                logger.warning(f"Supabase insert_user status {res.status_code}: {res.text}")
                return False
        except Exception as e:
            logger.warning(f"Supabase insert_user network error: {e}")
            return False

    async def sync_user_auth(
        self,
        email: str,
        password: Optional[str] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Provision or sync user in Supabase GoTrue Auth via Admin API."""
        if not self.is_enabled:
            return None

        url = f"{self.url}/auth/v1/admin/users"
        headers = self._get_headers(use_service_role=True)
        payload = {
            "email": email,
            "email_confirm": True,
            "user_metadata": user_metadata or {},
        }
        if password:
            payload["password"] = password

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code in [200, 201]:
                    logger.info(f"✓ User {email} provisioned in Supabase GoTrue Auth")
                    return res.json()
                logger.debug(f"Supabase GoTrue sync notice ({res.status_code}): {res.text[:120]}")
                return None
        except Exception as e:
            logger.warning(f"Supabase GoTrue sync error: {e}")
            return None

    def get_status(self) -> Dict[str, Any]:
        """Check Supabase configuration and connectivity status."""
        return {
            "is_enabled": self.is_enabled,
            "endpoint": self.url or "not_configured (running local PostgreSQL)",
            "storage_bucket": self.bucket if self.is_enabled else "local_disk",
            "realtime_enabled": self.is_enabled,
        }




# Global singleton instance
_supabase_service = None


def get_supabase_service(force_reload: bool = False) -> SupabaseService:
    """Get or create singleton SupabaseService."""
    global _supabase_service
    if _supabase_service is None or force_reload:
        _supabase_service = SupabaseService()
    return _supabase_service
