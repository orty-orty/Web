FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /shared && echo "HackUTT{R3ad_f1Le_is_s0_34sy}" > /shared/flag.txt
RUN chmod 644 /shared/flag.txt

EXPOSE 5005

CMD ["python", "app.py"]
