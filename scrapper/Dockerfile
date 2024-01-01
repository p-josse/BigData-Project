FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Crée un dossier pour stocker les fichiers de sortie
RUN mkdir /app/output

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 5000

CMD ["python", "scrapper.py"]
