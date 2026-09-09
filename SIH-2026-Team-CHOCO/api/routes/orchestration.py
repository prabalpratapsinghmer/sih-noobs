"""Orchestration API routes — ML pipeline execution, data drift reports, and model lifecycle."""

from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from orchestration.flows.retraining_flow import run_retraining_pipeline

router = APIRouter()

# In-memory history of flow runs
_flow_history = []


class RetrainTriggerRequest(BaseModel):
    min_records: int = Field(default=50, ge=10, description="Minimum new verified complaints required to trigger run")
    epochs: int = Field(default=3, ge=1, le=20, description="Retraining epochs")
    force: bool = Field(default=False, description="Force retraining even if drift is low")


@router.post("/retrain", tags=["ML Orchestration"])
async def trigger_retraining(request: RetrainTriggerRequest):
    """Trigger the automated Prefect ML retraining and validation pipeline."""
    try:
        run_summary = run_retraining_pipeline(
            min_records=request.min_records,
            epochs=request.epochs,
        )
        _flow_history.insert(0, run_summary)
        if len(_flow_history) > 20:
            _flow_history.pop()
        return run_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")


@router.get("/status", tags=["ML Orchestration"])
async def get_orchestration_status():
    """Get current status of ML orchestration engine and latest run metrics."""
    latest_run = _flow_history[0] if _flow_history else None
    return {
        "orchestration_engine": "Prefect ML Workflow Engine",
        "scheduler_active": True,
        "total_runs_tracked": len(_flow_history),
        "latest_run": latest_run,
    }


@router.get("/history", tags=["ML Orchestration"])
async def get_orchestration_history():
    """Retrieve history of automated retraining pipeline runs."""
    return {
        "count": len(_flow_history),
        "history": _flow_history,
    }
