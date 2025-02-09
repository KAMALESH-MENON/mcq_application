import json
import random
from typing import List
from uuid import UUID

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.models.data_models import MCQ, Submission, UserHistory, UserHistoryDetail
from app.schemas.mcq_schemas import (
    AttemptedMcqWithAnswer,
    MCQCreate,
    MCQCreateOutput,
    MCQDisplay,
    PaginatedResponse,
    SubmissionInput,
    SubmissionOutput,
    TypeEnum,
    UserHistoryInput,
    UserOutput,
)
from app.services.aws_services import generate_certificate, generate_presigned_url_func
from app.services.unit_of_work import (
    BaseUnitOfWork,
    HistoryUnitOfWork,
    SubmissionUnitOfWork,
)


def fetch_mcq_types(unit_of_work: BaseUnitOfWork) -> List[TypeEnum]:
    """
    Retrieve distinct MCQ types using Unit of Work.

    Args:
        unit_of_work (BaseUnitOfWork): UnitOfWork instance.

    Returns:
        list[TypeEnum]: List of MCQ types.
    """
    with unit_of_work:
        types = unit_of_work.mcq.get_mcq_types()
        return [TypeEnum(str(type_[0])) for type_ in types]


def add_mcq(
    unit_of_work: BaseUnitOfWork, mcq: MCQCreate, current_user: UserOutput
) -> MCQCreateOutput:
    """
    Adds a new MCQ to the database. Only users with the role of "admin" can create the MCQ.

    Args:
        unit_of_work (BaseUnitOfWork): The unit of work object that manages database transactions and repositories.
        mcq (MCQCreate): MCQ schema
        current_user (UserOutput): The current authenticated user, used to check authorization.

    Returns:
        MCQCreateOutput: The output model containing the data of the newly created MCQ, including its ID.

    Raises:
        HTTPException: If the user's role is not "admin".
        HTTPException: If the provided MCQ type is not valid.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )
    with unit_of_work:
        existing_types = fetch_mcq_types(unit_of_work=unit_of_work)
        if mcq.type not in existing_types:
            raise HTTPException(status_code=400, detail="Invalid MCQ type input.")

        duplicate_mcq = (
            unit_of_work.session.query(MCQ).filter_by(question=mcq.question).first()
        )
        if duplicate_mcq:
            raise HTTPException(status_code=400, detail="Duplicate question found.")

        mcq_data = mcq.model_dump()
        mcq = MCQ(**mcq_data)
        unit_of_work.session.add(mcq)
        unit_of_work.session.flush()
        unit_of_work.session.refresh(mcq)

        return MCQCreateOutput(**mcq.__dict__)


def bulk_add_mcqs(
    unit_of_work: BaseUnitOfWork, file: UploadFile, current_user: UserOutput
) -> int:
    """
    Bulk adds MCQs from an uploaded file to the database if the question does not exist in database otherwise skips.

    Args:
        unit_of_work (BaseUnitOfWork): The unit of work object that manages database transactions and repositories.
        file (UploadFile): Uploaded Excel file containing MCQ data.
        current_user (UserOutput): Current authenticated user.

    Returns:
        int: Count of MCQs successfully added.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: The file format is invalid or if validation fails.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Upload an Excel file."
        )

    try:
        df = pd.read_excel(file.file, dtype=str, keep_default_na=False)

        required_columns = [
            "category",
            "question",
            "option A",
            "option B",
            "option C",
            "option D",
            "correct_option",
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}",
            )

        invalid_entries = []
        for index, row in df.iterrows():
            for column in required_columns:
                if row[column] in [""] or (
                    column == "correct_option"
                    and row[column] not in ["a", "b", "c", "d"]
                ):
                    invalid_entries.append(f"Row {index + 2}, Column '{column}'")

        if invalid_entries:
            raise HTTPException(
                status_code=400,
                detail=f"Validation errors in entries: {'; '.join(invalid_entries)}",
            )

        added_count = 0
        skipped_count = 0
        with unit_of_work:
            for _, row in df.iterrows():
                question_exist = unit_of_work.mcq.get_all(question=row.get("question"))

                if question_exist:
                    skipped_count += 1
                else:
                    options_dict = {
                        "a": row.get("option A"),
                        "b": row.get("option B"),
                        "c": row.get("option C"),
                        "d": row.get("option D"),
                    }

                    # Convert the dictionary to a JSON string
                    options_json = json.dumps(options_dict)

                    # Parse the JSON string back into a dictionary to avoid escape characters
                    options_cleaned = json.loads(options_json)

                    mcq_data = {
                        "type": row.get("category"),
                        "question": row.get("question"),
                        "options": options_cleaned,
                        "correct_option": row["correct_option"],
                        "created_by": current_user.user_id,
                    }
                    mcq = MCQ(**mcq_data)
                    unit_of_work.mcq.add(mcq)
                    added_count += 1

        return added_count, skipped_count

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


def get_all(
    unit_of_work: BaseUnitOfWork,
    type: str,
    page: int,
    page_size: int,
    current_user: UserOutput,
) -> dict:
    """
    Retrieve paginated MCQs with optional type filter and pagination.
    """
    with unit_of_work:
        mcqs = unit_of_work.mcq.get_all(type_=type)

        if mcqs is None:
            raise HTTPException(
                status_code=404, detail="No MCQs found for the given type"
            )

        mcqs_list_object = []
        for mcq in mcqs:
            mcq_dict = {
                "mcq_id": mcq.mcq_id,
                "type": mcq.type,
                "question": mcq.question,
                "options": mcq.options,
            }
            mcqs_list_object.append(MCQDisplay(**mcq_dict))

        random.shuffle(mcqs_list_object)

        limited_mcqs_list_object = mcqs_list_object[:page_size]

        total_count = len(limited_mcqs_list_object)
        total_pages = (total_count // page_size) + (
            1 if total_count % page_size > 0 else 0
        )

        start = (page - 1) * page_size
        end = start + page_size

        paginated_mcqs_list_object = mcqs_list_object[start:end]

        next_page = page + 1 if page < total_pages else None

        submission = Submission(
            user_id=current_user.user_id, total_questions=total_count, type=type
        )
        unit_of_work.submission.add(submission)

        return PaginatedResponse(
            currentPage=page,
            totalPage=total_pages,
            nextPage=next_page,
            totalCount=total_count,
            data=paginated_mcqs_list_object,
        )


def process_submission(
    submission: SubmissionInput,
    unit_of_work: SubmissionUnitOfWork,
    current_user: UserOutput,
) -> SubmissionOutput:
    """
    Processes the submission of MCQ answers, calculates the score and percentage,
    and updates the user's submission history.

    Parameters:
        submission : SubmissionInput
            The submission data containing user ID and attempted MCQs.
        unit_of_work : SubmissionUnitOfWork
            The Unit of Work instance for managing database transactions.
        current_user : UserOutput
            The current logged-in user.

    Returns:
        SubmissionOutput The output containing user ID, details of the attempted MCQs, and the percentage score.

    Raises:
        HTTPException If an MCQ is not found.
    """
    user_id = current_user.user_id
    total_score = 0
    submission_details = []

    with unit_of_work as uow:
        last_submission_total_question = uow.submission.get_all(
            user_id=user_id, sort_by="created_at", order="desc"
        )
        total_questions = last_submission_total_question[0].total_questions

        user_history = UserHistory(
            user_id=user_id,
            total_score=0,
            percentage=0,
            total_attempts=total_questions,
            submission_id=last_submission_total_question[0].submission_id,
        )

        for attempted_mcq in submission.attempted:
            mcq = uow.mcq.get(mcq_id=attempted_mcq.mcq_id)
            if not mcq:
                raise HTTPException(
                    status_code=404, detail=f"MCQ {attempted_mcq.mcq_id} not found"
                )
            is_correct = attempted_mcq.user_answer.value == mcq.correct_option
            total_score += 1 if is_correct else 0

            detail = UserHistoryDetail(
                history_id=user_history.history_id,
                mcq_id=mcq.mcq_id,
                user_answer=attempted_mcq.user_answer.value,
                is_correct=is_correct,
            )
            user_history.details.append(detail)

            submission_details.append(
                AttemptedMcqWithAnswer(
                    mcq_id=mcq.mcq_id,
                    type=mcq.type,
                    question=mcq.question,
                    options=mcq.options,
                    correct_option=mcq.correct_option,
                    user_answer=attempted_mcq.user_answer.value,
                )
            )

        percentage = (
            (total_score / total_questions) * 100 if total_questions != 0 else 0
        )

        data = {
            "name": current_user.username,
            "type": mcq.type,
            "percentage": percentage,
        }
        generated_certificate_name = (
            generate_certificate(data=data).get("body").get("object_name")
        )

        user_history.total_score = total_score
        user_history.percentage = percentage
        user_history.certificate = generated_certificate_name
        uow.history.add(user_history)

        return SubmissionOutput(
            user_id=user_id,
            data=submission_details,
            total_score=total_score,
            total_attempts=total_questions,
            percentage=percentage,
        )


def view_history_of_submission_of_user(
    unit_of_work: HistoryUnitOfWork,
    current_user: UserOutput,
    sort_by: str = None,
    order: str = "asc",
):
    """
    Retrieves the submission histories for the current user.

    Parameters:
        unit_of_work : HistoryUnitOfWork
            The Unit of Work instance for managing database transactions.
        current_user : UserOutput
            The current logged-in user.

    Returns:
        List[UserHistoryInput]
            A list of the user's submission history records.
    """
    with unit_of_work as uow:
        histories = uow.history.get_all(
            user_id=current_user.user_id,
            sort_by=sort_by,
            order=order,
        )
        return [UserHistoryInput(**history.__dict__) for history in histories]


def view_particular_history(
    unit_of_work: SubmissionUnitOfWork,
    current_user: UserOutput,
    history_id: UUID,
) -> SubmissionOutput:
    """
    Retrieves a particular submission details.
    """
    with unit_of_work as uow:
        history = uow.history.get(history_id=history_id)
        history_dict = history.__dict__

        details = uow.history_details.get_all(history_id=history_id)

        details_list = []
        for detail in details:
            mcq = uow.mcq.get(mcq_id=detail.mcq_id)
            details_list.append(
                {
                    "mcq_id": str(detail.mcq_id),
                    "type": mcq.type,
                    "question": mcq.question,
                    "options": mcq.options,
                    "correct_option": mcq.correct_option,
                    "user_answer": detail.user_answer,
                    "is_correct": detail.is_correct,
                }
            )

        return SubmissionOutput(
            user_id=history_dict.get("user_id"),
            data=details_list,
            total_score=history_dict.get("total_score"),
            total_attempts=history_dict.get("total_attempts"),
            percentage=history_dict.get("percentage"),
        )


def create_certificate(unit_of_work: SubmissionUnitOfWork, current_user: UserOutput):
    """
    generates a certificate
    """
    with unit_of_work as uow:
        histories = uow.history.get_all(user_id=current_user.user_id, order="desc")
        last_submitted_history_dict = histories[-1].__dict__
        last_submission = uow.submission.get_all(
            user_id=current_user.user_id, order="desc"
        )
        mcq_type = last_submission[0].type
        last_submitted_history_percentage = last_submitted_history_dict.get(
            "percentage"
        )

    data = {
        "name": current_user.username,
        "type": mcq_type,
        "percentage": last_submitted_history_percentage,
    }

    return generate_certificate(data=data)


def generate_certificate_presigned_url(
    unit_of_work: HistoryUnitOfWork,
    current_user: UserOutput,
    history_id: UUID,
):
    """
    generates a presigned link of existing certificate
    """
    with unit_of_work as uow:
        history = uow.history.get(history_id=history_id)
        if not history:
            raise HTTPException(status_code=404, detail="History not found")
        certificate = history.certificate
        if certificate:
            return generate_presigned_url_func(file_key=certificate)
        else:
            raise HTTPException(status_code=404, detail="Certtificate not found.")
