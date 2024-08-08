from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from weasyprint import HTML, CSS
# import cups
import subprocess

app = FastAPI()
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

class Print(BaseModel):
    name: str
    timestamp: str

@app.post("/print")
def print_label(obj_in: Print):
    html_content = generate_html_content(obj_in.name, obj_in.timestamp)
    generate_pdf(html_content)
    # print_file('print/label.pdf', 'QL600')
    # print_string = 'this item belongs to \n'
    # print_string += obj_in.name
    # print_string += '\n\nprinted at'
    # print_string += obj_in.timestamp
    subprocess.run(['lpr', '-o', 'landscape' '-P', 'QL600', 'print/label.pdf'])
    return { 'status': 'success' }

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

def print_file(file_path: str, printer_name: str):
    conn = cups.Connection()
    printers = conn.getPrinters()

    if printer_name in printers:
        try:
            conn.printFile(printer_name, file_path, "Print Job", {})
            print("File sent to printer successfully.")
        except cups.IPPError as e:
            print(f"Error printing file: {e}")
    else:
        print(f"Printer '{printer_name}' not found.")