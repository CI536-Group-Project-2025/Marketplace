# syntax=docker/dockerfile:1
FROM python:3.13-alpine
WORKDIR /code
ENV FLASK_APP=src/main.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "src/main.py"]
