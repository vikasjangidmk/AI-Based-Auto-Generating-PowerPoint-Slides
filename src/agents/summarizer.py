import os
from dotenv import load_dotenv
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings  # Correct way to set global LLM

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Summarizer:
    def __init__(self):
        """Initialize the LlamaIndex summarization model with OpenAI."""
        Settings.llm = OpenAI(model="gpt-4", api_key=OPENAI_API_KEY)  # Set global LLM

    def summarize_text(self, text):
        """Summarizes extracted text using LlamaIndex."""
        documents = [Document(text=text)]  # Correct way to initialize Document
        index = GPTVectorStoreIndex.from_documents(documents)  # Create index
        query_engine = index.as_query_engine()
        
        response = query_engine.query("Summarize this text into key points suitable for a PowerPoint slide.")
        return response.response  # Extract summary text

if __name__ == "__main__":
    # Test Summarizer
    sample_text = """AI is transforming industries by automating repetitive tasks and enabling data-driven decision-making.
    This project aims to generate PowerPoint slides automatically based on input documents.
    It will extract text from PDFs, DOCX, TXT, and CSV files and convert them into well-structured slides.
    The AI will use OpenAI's GPT models for text summarization and LlamaIndex for information retrieval."""
    
    summarizer = Summarizer()
    summary = summarizer.summarize_text(sample_text)
    
    print("\n🔹 **Summarized Text:**\n")
    print(summary)
