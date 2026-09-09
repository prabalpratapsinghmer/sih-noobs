"""API route modules aggregating all prediction, security, portal, and enterprise services."""

from fastapi import APIRouter
from loguru import logger

# Create the main API router that aggregates all sub-routers
api_router = APIRouter()


def include_routers():
    """Register all modular routes into the main API router."""
    # 1. Prediction & ML Models
    try:
        from api.routes.predict import router as predict_router
        api_router.include_router(predict_router, prefix="/predict", tags=["Prediction"])
    except Exception as e:
        logger.warning(f"Could not load predict router: {e}")

    try:
        from api.routes.detect import router as detect_router
        api_router.include_router(detect_router, prefix="/detect", tags=["Mule Detection"])
    except Exception as e:
        logger.warning(f"Could not load detect router: {e}")

    try:
        from api.routes.trigger import router as trigger_router
        api_router.include_router(trigger_router, prefix="/trigger", tags=["Proactive Actions"])
    except Exception as e:
        logger.warning(f"Could not load trigger router: {e}")

    try:
        from api.routes.status import router as status_router
        api_router.include_router(status_router, prefix="/model", tags=["Model Status"])
    except Exception as e:
        logger.warning(f"Could not load status router: {e}")

    # 2. Vector DB & Orchestration (Modern Stack)
    try:
        from api.routes.vector import router as vector_router
        api_router.include_router(vector_router, prefix="/vector", tags=["Vector Search & MO"])
    except Exception as e:
        logger.warning(f"Could not load vector router: {e}")

    try:
        from api.routes.orchestration import router as orch_router
        api_router.include_router(orch_router, prefix="/orchestration", tags=["ML Orchestration"])
    except Exception as e:
        logger.warning(f"Could not load orchestration router: {e}")

    # 3. Authentication & Administration
    try:
        from api.routes.auth import router as auth_router
        api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    except Exception as e:
        logger.warning(f"Could not load auth router: {e}")

    try:
        from api.routes.auth_google import router as auth_google_router
        api_router.include_router(auth_google_router, tags=["Google OAuth"])
    except Exception as e:
        logger.warning(f"Could not load auth_google router: {e}")

    try:
        from api.routes.admin import router as admin_router
        api_router.include_router(admin_router, prefix="/admin", tags=["Administration"])
    except Exception as e:
        logger.warning(f"Could not load admin router: {e}")

    # 4. Command Portals (Police & Victim)
    try:
        from api.routes.police import router as police_router
        api_router.include_router(police_router, prefix="/police", tags=["Police Command"])
    except Exception as e:
        logger.warning(f"Could not load police router: {e}")

    try:
        from api.routes.victim import router as victim_router
        api_router.include_router(victim_router, prefix="/victim", tags=["Victim Portal"])
    except Exception as e:
        logger.warning(f"Could not load victim router: {e}")

    # 5. Banking & External Intermediaries
    try:
        from api.routes.banking import router as banking_router
        api_router.include_router(banking_router, prefix="/banking", tags=["Banking Step-Up API"])
    except Exception as e:
        logger.warning(f"Could not load banking router: {e}")

    try:
        from api.routes.blockchain import router as blockchain_router
        api_router.include_router(blockchain_router, prefix="/blockchain", tags=["Blockchain Audit"])
    except Exception as e:
        logger.warning(f"Could not load blockchain router: {e}")

    try:
        from api.routes.evidence import router as evidence_router
        api_router.include_router(evidence_router, prefix="/evidence", tags=["Evidence & IPFS"])
    except Exception as e:
        logger.warning(f"Could not load evidence router: {e}")

    # 6. Auditing, Notifications & WhatsApp
    try:
        from api.routes.audit import router as audit_router
        api_router.include_router(audit_router, prefix="/audit", tags=["Audit Trail"])
    except Exception as e:
        logger.warning(f"Could not load audit router: {e}")

    try:
        from api.routes.notifications import router as notifications_router
        api_router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
    except Exception as e:
        logger.warning(f"Could not load notifications router: {e}")

    try:
        from api.routes.whatsapp import router as whatsapp_router
        api_router.include_router(whatsapp_router, prefix="/whatsapp", tags=["WhatsApp Webhook"])
    except Exception as e:
        logger.warning(f"Could not load whatsapp router: {e}")

    try:
        from api.routes.llm import router as llm_router
        api_router.include_router(llm_router, prefix="/llm", tags=["LLM AI Agent"])
    except Exception as e:
        logger.warning(f"Could not load llm router: {e}")


include_routers()
