FROM python:3.9.7
WORKDIR /project
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt
COPY . .
