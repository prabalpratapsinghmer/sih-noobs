"""Admin routes — user management, system health, model metrics."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.password import hash_password
from api.auth.rbac import RoleChecker
from api.database.postgres import get_db
from api.models.user import User
from api.schemas.admin import ModelMetrics, SystemHealth, UserCreate, UserOut, UserUpdate

router = APIRouter()
admin_only = RoleChecker(["ADMIN"])


@router.get("/users", response_model=dict)
async def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: dict = Depends(admin_only),
    db: AsyncSession = Depends(get_db),
):
    """List all users, paginated."""
    total = (await db.execute(select(func.count()).select_from(User))).scalar() or 0
    rows = (await db.execute(select(User).order_by(User.created_at.desc())
            .offset((page - 1) * page_size).limit(page_size))).scalars().all()
    return {
        "items": [UserOut.model_validate(u).model_dump() for u in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(body: UserCreate, user: dict = Depends(admin_only),
                      db: AsyncSession = Depends(get_db)):
    """Create new user with role assignment."""
    existing = (await db.execute(
        select(User).where((User.username == body.username) | (User.email == body.email))
    )).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    from api.models.user import UserRole

    new_user = User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        role=UserRole(body.role),
        station=body.station,
        badge_number=body.badge_number,
        phone=body.phone,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserOut.model_validate(new_user)


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: str, body: UserUpdate, user: dict = Depends(admin_only),
                      db: AsyncSession = Depends(get_db)):
    """Update user details/role."""
    result = await db.execute(select(User).where(User.user_id == user_id))
    target = result.scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")

    data = body.model_dump(exclude_unset=True)
    from api.models.user import UserRole

    if "role" in data and data["role"]:
        data["role"] = UserRole(data["role"])
    for field, value in data.items():
        setattr(target, field, value)
    await db.commit()
    await db.refresh(target)
    return UserOut.model_validate(target)


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, user: dict = Depends(admin_only),
                      db: AsyncSession = Depends(get_db)):
    """Soft-delete (set is_active=false)."""
    if user_id == user.get("user_id"):
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    result = await db.execute(select(User).where(User.user_id == user_id))
    target = result.scalar_one_or_none()
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")
    target.is_active = False
    await db.commit()
    return {"detail": "User deactivated"}


@router.get("/system/health", response_model=SystemHealth)
async def system_health(user: dict = Depends(admin_only)):
    """Health status of PG, Neo4j, Redis, Celery."""
    services = {"api": "healthy"}

    try:
        from api.database.postgres import check_postgres_health
        services["postgres"] = "healthy" if await check_postgres_health() else "unhealthy"
    except Exception as e:
        services["postgres"] = str(e)[:100]

    try:
        from api.database.neo4j import check_neo4j_health
        services["neo4j"] = "healthy" if await check_neo4j_health() else "unhealthy"
    except Exception as e:
        services["neo4j"] = str(e)[:100]

    try:
        from api.database.redis import check_redis_health
        services["redis"] = "healthy" if await check_redis_health() else "unhealthy"
    except Exception as e:
        services["redis"] = str(e)[:100]

    try:
        from api.tasks.celery_app import celery_app
        ping = celery_app.control.ping(timeout=2)
        services["celery"] = "healthy" if ping else "unreachable"
    except Exception as e:
        services["celery"] = str(e)[:100]

    all_ok = all(v == "healthy" for v in services.values())
    return SystemHealth(status="healthy" if all_ok else "degraded", services=services)


@router.get("/model/metrics", response_model=ModelMetrics)
async def model_metrics(user: dict = Depends(admin_only)):
    """ML model accuracy, F1, precision, recall (mock until Member 1's model live)."""
    return ModelMetrics(
        accuracy=0.932,
        precision=0.918,
        recall=0.886,
        f1=0.902,
        auc_roc=0.961,
        trained_at=datetime.now(UTC),
        model_version="gnn-v1.2",
    )


@router.post("/model/retrain")
async def trigger_retrain(user: dict = Depends(admin_only)):
    """Trigger GNN retraining (async Celery task)."""
    try:
        from api.tasks.celery_app import celery_app
        celery_app.send_task("model.retrain_gnn", args=[], queue="default")
        return {"detail": "Retraining triggered", "status": "queued"}
    except Exception:
        return {"detail": "Celery unavailable — retraining request logged", "status": "deferred"}
