FROM python:3.12-slim

WORKDIR /app

COPY ci/requirements/requirements.txt .


RUN pip install -r requirements.txt



RUN apt update && apt install -y tree
COPY . .
ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]
