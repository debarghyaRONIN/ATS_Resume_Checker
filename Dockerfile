
FROM python:3.9-slim


RUN apt-get update && apt-get install -y poppler-utils


WORKDIR /app


COPY . .


RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "your_script.py"]
