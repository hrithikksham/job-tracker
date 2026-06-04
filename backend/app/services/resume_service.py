from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId

from app.database.mongodb import database

fs = AsyncIOMotorGridFSBucket(database)


async def upload_resume(file):
    file_data = await file.read()

    file_id = await fs.upload_from_stream(
        file.filename,
        file_data
    )

    return str(file_id)


async def get_resume(file_id: str):
    stream = await fs.open_download_stream(
        ObjectId(file_id)
    )

    file_data = await stream.read()

    return file_data


async def delete_resume(file_id: str):
    await fs.delete(
        ObjectId(file_id)
    )

    return True