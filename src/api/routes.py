import os
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from src.agents.content_extractor import ContentExtractor
from src.agents.summarizer import Summarizer
from src.agents.slide_generator import SlideGenerator

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for slide generation."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "message": "File uploaded successfully!"}

@router.get("/generate/")
async def generate_presentation():
    """Runs the AI pipeline to generate PowerPoint slides."""
    extractor = ContentExtractor(directory=UPLOAD_DIR)
    extracted_content = extractor.extract_from_directory()
    
    summarizer = Summarizer()
    slide_generator = SlideGenerator(output_dir="output/")
    
    for filename, text in extracted_content.items():
        summary = summarizer.summarize_text(text)
        summary_points = summary.split("\n")  
        slide_generator.create_slide_deck(filename, summary_points)

    pptx_path = "output/generated_presentation.pptx"
    return {"message": "Slides generated!", "download_url": f"/download/?filename={pptx_path}"}

@router.get("/download/")
async def download_presentation(filename: str):
    """Download the generated PowerPoint presentation."""
    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename="AI_Presentation.pptx")
