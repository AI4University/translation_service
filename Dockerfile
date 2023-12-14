FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000 10010 10020 10030 10040 10050 10060 10070 10080 10090 10100
CMD [ "python", "./traductor.py"]