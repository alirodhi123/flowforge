from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user, hash_password, verify_password, create_access_token
from app.models.models import User, Tenant, Workflow, WorkflowRun
from app.services.dag import execute_workflow
import uuid

router = APIRouter()

# ── AUTH ──────────────────────────────────────────

@router.post("/auth/register")
def register(data: dict, db: Session = Depends(get_db)):
    tenant = Tenant(id=str(uuid.uuid4()), name=data["tenant_name"])
    db.add(tenant)
    user = User(
        id=str(uuid.uuid4()),
        tenant_id=tenant.id,
        email=data["email"],
        hashed_password=hash_password(data["password"]),
        role="admin"
    )
    db.add(user)
    db.commit()
    return {"message": "Register berhasil"}

@router.post("/auth/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data["email"]).first()
    if not user or not verify_password(data["password"], user.hashed_password):
        raise HTTPException(status_code=400, detail="Email atau password salah")
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

# ── WORKFLOW ──────────────────────────────────────

@router.get("/workflows")
def get_workflows(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workflows = db.query(Workflow).filter(Workflow.tenant_id == current_user.tenant_id).all()
    return workflows

@router.post("/workflows")
def create_workflow(data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workflow = Workflow(
        id=str(uuid.uuid4()),
        tenant_id=current_user.tenant_id,
        name=data["name"],
        description=data.get("description"),
        definition=data["definition"]
    )
    db.add(workflow)
    db.commit()
    return {"message": "Workflow berhasil dibuat", "id": workflow.id}

@router.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.tenant_id == current_user.tenant_id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow tidak ditemukan")
    return workflow

@router.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.tenant_id == current_user.tenant_id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow tidak ditemukan")
    
    db.query(WorkflowRun).filter(WorkflowRun.workflow_id == workflow_id).delete()
    db.delete(workflow)
    db.commit()

    # db.delete(workflow)
    # db.commit()
    return {"message": "Workflow berhasil dihapus"}

# ── RUN ───────────────────────────────────────────

@router.post("/workflows/{workflow_id}/run")
def run_workflow(workflow_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.tenant_id == current_user.tenant_id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow tidak ditemukan")
    
    results = execute_workflow(workflow.definition)
    
    run = WorkflowRun(
        id=str(uuid.uuid4()),
        workflow_id=workflow.id,
        status="success",
        logs=results
    )
    db.add(run)
    db.commit()
    return {"message": "Workflow selesai dijalankan", "results": results}

@router.get("/workflows/{workflow_id}/runs")
def get_runs(workflow_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    runs = db.query(WorkflowRun).filter(WorkflowRun.workflow_id == workflow_id).all()
    return runs