FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN echo "HackUTT{R3ad_f1Le_is_s0_34sy}" > /flag.txt
RUN chmod 644 /flag.txt

CMD ["python", "app.py"]
