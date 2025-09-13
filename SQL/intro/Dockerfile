#Using python image
FROM python:3.11-slim

#Setting de workspace
WORKDIR /app

#Copying necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY script.py .

#Run the script
CMD ["python", "script.py"]
