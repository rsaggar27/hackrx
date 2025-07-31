import re
import mimetypes
import requests
import chardet
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from bs4 import BeautifulSoup
import email


def extract_text_from_url(url: str) -> str:
    """
    Extracts and returns plain text from a file at the given URL.
    Supported formats: PDF, DOCX, TXT, EML.
    Automatically handles Google Drive links and Azure blob SAS URLs.
    """

    # Convert Google Drive URL to direct download link
    if "drive.google.com" in url:
        file_id = extract_google_drive_file_id(url)
        if not file_id:
            raise ValueError("Invalid Google Drive link format.")
        url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Download the file
    response = requests.get(url)
    response.raise_for_status()
    file_bytes = response.content

    # Determine file type from headers or URL
    content_type = response.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(content_type) or get_extension_from_url(url)

    if ext in [".pdf", "application/pdf"]:
        return extract_text_from_pdf(file_bytes)
    elif ext in [".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return extract_text_from_docx(file_bytes)
    elif ext in [".txt", "text/plain"]:
        return extract_text_from_txt(file_bytes)
    elif ext in [".eml", "message/rfc822"]:
        return extract_text_from_email(file_bytes)
    else:
        raise ValueError(f"Unsupported or unknown file type: {ext}")


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])


def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = DocxDocument(BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(file_bytes: bytes) -> str:
    encoding = chardet.detect(file_bytes)["encoding"] or "utf-8"
    return file_bytes.decode(encoding, errors="ignore")


def extract_text_from_email(file_bytes: bytes) -> str:
    msg = email.message_from_bytes(file_bytes)
    parts = []

    for part in msg.walk():
        content_type = part.get_content_type()
        charset = part.get_content_charset() or 'utf-8'

        if content_type == "text/plain":
            parts.append(part.get_payload(decode=True).decode(charset, errors="ignore"))
        elif content_type == "text/html":
            html = part.get_payload(decode=True).decode(charset, errors="ignore")
            text = BeautifulSoup(html, "html.parser").get_text()
            parts.append(text)

    return "\n".join(parts)


def extract_google_drive_file_id(url: str) -> str | None:
    patterns = [
        r"https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_extension_from_url(url: str) -> str:
    """
    Attempts to determine the file extension from the URL.
    """
    ext = url.split("?")[0].split("/")[-1].lower()
    if ext.endswith(".pdf"):
        return ".pdf"
    elif ext.endswith(".docx"):
        return ".docx"
    elif ext.endswith(".txt"):
        return ".txt"
    elif ext.endswith(".eml"):
        return ".eml"
    return ""
