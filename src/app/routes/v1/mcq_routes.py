from fastapi import APIRouter, Depends, Query

from app.schemas.mcq_schemas import UserOutput
from app.services import McqUnitOfWork, mcq_services, user_services

router = APIRouter(prefix="/mcqs", tags=["User Routes for MCQ app"])


@router.get("/types", response_model=list[str])
def get_mcq_types(current_user: UserOutput = Depends(user_services.get_current_user)):
    """
    Endpoint to fetch distinct MCQ types.
    """
    unit_of_work = McqUnitOfWork()
    return mcq_services.fetch_mcq_types(unit_of_work=unit_of_work)


@router.get("")
async def get_random_mcqs(
    type: str = Query(..., description="MCQ type to filter by"),
    page_size: int = Query(10, le=100, description="Number of MCQs to return"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    current_user: UserOutput = Depends(user_services.get_current_user),
):
    """
    Fetches random MCQs of a chosen type, paginated by the given limit.

    Parameters:
    - type: MCQ type to filter the MCQs.
    - limit: Number of MCQs to return in the response (pagination).

    Returns:
    - List of MCQs based on the given type, paginated by the limit.
    """
    unit_of_work = McqUnitOfWork()
    mcqs = mcq_services.get_all(
        unit_of_work=unit_of_work, type=type, page_size=page_size, page=page
    )
    return mcqs
