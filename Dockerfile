FROM python:3.10
RUN apt-get update && apt-get install -y tesseract-ocr
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000
EXPOSE 8501

COPY . .
CMD ["uvicorn", "manage:app", "--port", "80", "--host", "0.0.0.0"]
# CMD ["uvicorn", "manage:app", "--host","0.0.0.0", "--port","8000"]