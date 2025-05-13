# syntax=docker/dockerfile:1
FROM python:3.13-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY marketplace marketplace
COPY requirements.txt requirements.txt
COPY migrations migrations
CMD ["python3", "-m", "marketplace"]
