import os
import pandas as pd
import fitz  # PyMuPDF for PDFs
from docx import Document
from llama_index.core import SimpleDirectoryReader  # Updated import for LlamaIndex

class ContentExtractor:
    def __init__(self, directory="data/"):  # Ensure correct directory path
        self.directory = directory

    def extract_text_from_txt(self, file_path):
        """Extract text from a TXT file."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def extract_text_from_pdf(self, file_path):
        """Extract text from a PDF file."""
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    def extract_text_from_docx(self, file_path):
        """Extract text from a DOCX file."""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_text_from_csv(self, file_path):
        """Extract text from a CSV file."""
        df = pd.read_csv(file_path)
        return df.to_string()

    def extract_from_file(self, file_path):
        """Extract content from different file formats."""
        _, ext = os.path.splitext(file_path)
        if ext == ".txt":
            return self.extract_text_from_txt(file_path)
        elif ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return self.extract_text_from_docx(file_path)
        elif ext == ".csv":
            return self.extract_text_from_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def extract_from_directory(self):
        """Extract content from all files in the directory."""
        extracted_data = {}
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"Directory not found: {self.directory}")

        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):  # Ensure it's a file
                try:
                    extracted_data[filename] = self.extract_from_file(file_path)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        return extracted_data

if __name__ == "__main__":
    extractor = ContentExtractor(directory="data/")  # Ensure correct path
    extracted_content = extractor.extract_from_directory()
    
    for file, content in extracted_content.items():
        print(f"\nExtracted content from {file}:\n{content[:500]}...\n")  # Limit output for readability
