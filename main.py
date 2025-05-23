import os
from typing import List

from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlmodel import select

from model import Details
from database import create_db_and_tables, get_session
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

origins = [
    "http://16.171.25.216/5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/app/upload/")
async def upload_pdf(
        name: str = Form(...),
        emp_id: int = Form(...),
        upload_file: UploadFile = File(...),
        session: Session = Depends(get_session)
):
    if upload_file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})

    upload_dir = "uploaded_pdfs"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, upload_file.filename)

    with open(file_location, "wb") as f:
        f.write(await upload_file.read())

    detail = Details(name=name, emp_id=emp_id, file_path=file_location)
    try:
        session.add(detail)
        session.commit()
        session.refresh(detail)
    except Exception as e:
        session.rollback()
        print("Error committing to DB:", e)

    return JSONResponse(
        content={
            "message": "PDF uploaded and name stored successfully.",
            "name": name,
            "empId": emp_id
        },
        status_code=200
    )
@app.get("/app/all/", response_model=List[Details])
def get_all_uploads(session: Session = Depends(get_session)):
    try:
        statement = select(Details)
        results = session.exec(statement).all()
        return results
    except Exception as e:
        print("Error fetching data from DB:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")




