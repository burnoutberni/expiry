# expiry
WIP label printer setup for the fridge at gt_

## Usage

Set up virtualenv and install dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi weasyprint pycups
```

Start FastAPI server

```
uvicorn main:app --reload
```

This serves all static files from `/web` as well as a rudimentary api at `/print` (plus automatically generate documenation at `/docs`).

Whenever the API is called, a new PDF is generated at `print/label.pdf`.

Printer set-up not tested yet.