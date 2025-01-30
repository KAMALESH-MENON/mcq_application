import boto3
from fastapi import HTTPException, UploadFile

from app.config.settings import app_config
from app.schemas.mcq_schemas import UserOutput

s3_client = boto3.client("s3")


def upload_template(file: UploadFile, current_user: UserOutput):
    """
    Upload a .docx file to S3 as a certificate template.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=401, detail="Access denied. Admin role required."
        )

    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a .jpg file."
        )

    file_name = "image_template/template_ui.jpg"

    s3_client.upload_fileobj(file.file, app_config["BUCKET_NAME"], file_name)

    return {"message": f"File uploaded successfully to {file_name}"}
