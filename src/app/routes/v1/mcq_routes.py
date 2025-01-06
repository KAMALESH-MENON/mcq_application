from fastapi import APIRouter, Depends

from app.schemas.mcq_schemas import MCQ, MCQCreate, UserOutput
from app.services import McqUnitOfWork, mcq_services, user_services

router = APIRouter(prefix="/mcqs", tags=["MCQs"])


@router.get("/types", response_model=list[str])
def get_mcq_types(current_user: UserOutput = Depends(user_services.get_current_user)):
    """
    Endpoint to fetch distinct MCQ types.
    """
    unit_of_work = McqUnitOfWork()
    return mcq_services.fetch_mcq_types(unit_of_work=unit_of_work)


@router.post("/", status_code=201)
def create_mcq(
    mcq_data: MCQCreate,
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Endpoint to create a new MCQ.
    """
    unit_of_work = McqUnitOfWork()
    mcq_data = MCQ(**mcq_data.model_dump(), created_by=current_user.user_id)
    return mcq_services.add_mcq(
        mcq=mcq_data, unit_of_work=unit_of_work, current_user=current_user
    )
