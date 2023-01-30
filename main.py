import time
from fastapi import FastAPI, status, HTTPException, Depends, File, UploadFile, Form
from database import Base, engine, SessionLocal
from pydantic import EmailStr
from subscription import subscribe_email, unsubscribe_email, \
    send_message_to_sqs
from utils import upload_file_to_s3, delete_file_from_s3
from sqlalchemy.orm import Session
import models
import os
import pathlib

Base.metadata.create_all(engine)

app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "Hello World"


@app.post("/uploadfile/",  status_code=status.HTTP_201_CREATED)
async def create_upload_file(file: UploadFile, name: str = Form(), session: Session = Depends(get_session)):
    file_location = f"images/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    await upload_file_to_s3(file.filename, name)
    file_stat = os.stat(f"{file_location}")
    image_size = file_stat.st_size
    updated_at = time.ctime(file_stat.st_mtime)
    file_extension = pathlib.Path(file_location).suffix
    image = models.Image(
        name=name,
        image_size=image_size,
        file_extension=file_extension,
        updated_at=updated_at
    )

    session.add(image)
    session.commit()
    session.refresh(image)

    send_message_to_sqs(f"Image name: {name}\nImage size: {image_size}\n"
                        f"File extension: {file_extension}\n"
                        f"Updated at: {updated_at}")

    os.remove(file_location)

    return image


@app.delete("/delete/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(name: str, session: Session = Depends(get_session)):
    image = session.query(models.Image).get(name)
    if image:
        session.delete(image)
        session.commit()
        await delete_file_from_s3(name)
    else:
        raise HTTPException(status_code=400, detail=f"Image item with name '{name}' not found")


@app.post("/subscribe/{email}")
def subscribe_for_notification(email: EmailStr):
    if subscribe_email(email)["SubscriptionArn"]:
        return HTTPException(status_code=200)
    return HTTPException(status_code=400, detail="Can't subscribe")


@app.delete("/unsubscribe/{email}")
def unsubscribe_for_notification(email: EmailStr):
    unsubscribe_email(email)
