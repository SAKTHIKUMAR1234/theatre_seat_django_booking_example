FROM python:3.12

ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE bookmyshow.settings

WORKDIR /app/

COPY . /app/

RUN pip install -r requirements.txt 

EXPOSE 8000