from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from weasyprint import HTML, CSS

app = FastAPI()

app.mount("/web", StaticFiles(directory="web"), name="web")

class Print(BaseModel):
    name: str
    timestamp: str

@app.post("/api")
def print_label(obj_in: Print):
    html_content = generate_html_content(obj_in.name, obj_in.timestamp)
    generate_pdf(html_content)
    return { 'status': 'success'}

def generate_html_content(name: str, timestamp: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="print/print-styles.css">
    </head>
    <body>
        <h1>This item belongs to {name}</h1>
        <p>In the fridge since {timestamp}</p>
    </body>
    </html>
    """

def generate_pdf(html_content: str):
    HTML(string=html_content).write_pdf("print/label.pdf", stylesheets=["print/print-styles.css"])
