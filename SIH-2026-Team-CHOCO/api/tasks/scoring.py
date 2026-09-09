"""Celery tasks for batch mule scoring."""

from api.tasks.celery_app import celery_app


@celery_app.task(name="scoring.batch_chain", bind=True, max_retries=3)
def batch_score_chain_task(self, complaint_id: str):
    """Score all accounts in a complaint's chain (runs sync via asyncio.run)."""
    try:
        import asyncio

        from api.database.postgres import get_db_session
        from api.services.mule_scoring import batch_score_chain

        async def _run():
            # Celery runs in non-async context; create its own session
            async with get_db_session() as session:
                results = await batch_score_chain(complaint_id, session=session)
                await session.commit()
            return results

        results = asyncio.run(_run())
        return {"complaint_id": complaint_id, "scored": len(results), "mules": results}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30) from exc


@celery_app.task(name="scoring.atm_predictions", bind=True, max_retries=3)
def atm_predictions_task(self, complaint_id: str, account_ids: list[str]):
    """Run ATM prediction pipeline for a complaint."""
    try:
        import asyncio

        async def _run():
            from api.services.predict import predict_atms
            return await predict_atms(complaint_id, account_ids)

        results = asyncio.run(_run())
        return {"complaint_id": complaint_id, "predictions": results}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30) from exc
