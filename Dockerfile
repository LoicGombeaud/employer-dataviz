FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .
ENV DJANGO_SETTINGS_MODULE="dataviz.settings"
ENV PYTHONPATH="/usr/src/app/"

CMD [ "django-admin", "runserver", "0.0.0.0:80" ]
