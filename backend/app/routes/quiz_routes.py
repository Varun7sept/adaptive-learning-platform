from fastapi import APIRouter, UploadFile, File, Form
import os
from app.utils.pdf_extract import extract_text_from_pdf
from app.services.quiz_gen_service import generate_quiz_questions

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/quiz/test")
def quiz_test():
    return {"message": "Quiz routes are working!"}

@router.post("/quiz/upload")
async def upload_file(
    num_questions: int = Form(...),   # 👈 Required form field (visible in Swagger)
    file: UploadFile = File(...)
):
    """
    Uploads a file, extracts text, and generates quiz questions dynamically
    using Groq AI. The user can specify how many questions to generate.
    """

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file_bytes = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Extract text
    if file.filename.lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        try:
            extracted_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            extracted_text = "Unable to decode file content."

    # Generate quiz dynamically
    quiz_output = generate_quiz_questions(extracted_text, num_questions=num_questions)

    return {
        "filename": file.filename,
        "question_count": num_questions,
        "content_preview": extracted_text[:400],
        "generated_quiz": quiz_output
    }
