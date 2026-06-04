from fastapi import APIRouter, UploadFile, File
from app.dependencies.auth import (
    get_current_user
)
from app.services.resume_service import (
    upload_resume
)

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        return {
            "success": False,
            "message": "Only PDF files allowed"
        }

    file_id = await upload_resume(file)
    current_user =Depends(get_current_user)

    if current_user:
        current_user["resume"] = file_id    
        return {
            "success": True,
            "message": "Resume uploaded successfully",
            "file_id": file_id
        }

@router.get("/download/{file_id}")
async def download_pdf(
    file_id: str
):
    file_data = await get_resume(file_id)

    return {
        "success": True,
        "file_data": file_data
    }

@router.delete("/delete/{file_id}")
async def delete_pdf(
    file_id: str
):
    await delete_resume(file_id)

    return {
        "success": True,
        "message": "Resume deleted successfully"
    }

