FROM python:3.11.4-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd5esheets ./dnd5esheets

CMD ["uvicorn", "dnd5esheets.app:app", "--host", "0.0.0.0", "--port", "8000"]
