FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/media
RUN chmod +x start.sh

CMD ["./start.sh"]