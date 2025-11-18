FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y default-mysql-server && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /shared && \
    echo "HackUTT{R3ad_f1le_fr0m_1ns1de_c0nt41ner}" > /shared/flag.txt && \
    chmod 644 /shared/flag.txt

RUN mkdir -p /etc/mysql/mysql.conf.d && \
    printf "[mysqld]\nsecure-file-priv=\n" > /etc/mysql/mysql.conf.d/zzz-custom.cnf

EXPOSE 5005

CMD ["python", "app.py"]
