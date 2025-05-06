import io
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import json
from env_config import logger

async def convert_pdf_to_docx(pdf_bytes, filename):
    """Convert PDF to DOCX format"""
    try:
        # Read PDF
        pdf = PdfReader(io.BytesIO(pdf_bytes))
        doc = Document()
        
        # Extract text from each page
        for page in pdf.pages:
            text = page.extract_text()
            doc.add_paragraph(text)
            
        # Save to buffer
        docx_buffer = io.BytesIO()
        doc.save(docx_buffer)
        docx_buffer.seek(0)
        
        return {
            'success': True,
            'file': docx_buffer,
            'filename': f"{filename.rsplit('.', 1)[0]}.docx",
            'message': "Successfully converted to Word format!"
        }
    except Exception as e:
        logger.error(f"PDF to DOCX conversion error: {e}")
        return {
            'success': False,
            'error': str(e)
        }

async def convert_json_to_csv(json_bytes, filename):
    """Convert JSON to CSV format"""
    try:
        # Parse JSON
        json_data = json.loads(json_bytes.decode())
        df = pd.DataFrame(json_data)
        
        # Save to buffer
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Convert to bytes buffer
        bytes_buffer = io.BytesIO(csv_buffer.getvalue().encode())
        
        return {
            'success': True,
            'file': bytes_buffer,
            'filename': f"{filename.rsplit('.', 1)[0]}.csv",
            'message': "Successfully converted to CSV format!"
        }
    except Exception as e:
        logger.error(f"JSON to CSV conversion error: {e}")
        return {
            'success': False,
            'error': str(e)
        }

async def convert_excel_to_pdf(excel_bytes, filename):
    """Convert Excel to PDF format"""
    try:
        # Read Excel
        df = pd.read_excel(io.BytesIO(excel_bytes))
        
        # Convert to HTML first (better formatting)
        html = df.to_html()
        
        # Use WeasyPrint to convert HTML to PDF
        from weasyprint import HTML
        pdf_buffer = io.BytesIO()
        HTML(string=html).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        
        return {
            'success': True,
            'file': pdf_buffer,
            'filename': f"{filename.rsplit('.', 1)[0]}.pdf",
            'message': "Successfully converted to PDF format!"
        }
    except Exception as e:
        logger.error(f"Excel to PDF conversion error: {e}")
        return {
            'success': False,
            'error': str(e)
        }