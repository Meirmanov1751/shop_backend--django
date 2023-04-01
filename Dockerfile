FROM python:3.8

WORKDIR .

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get --assume-yes install build-essential gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt  /usr/src/app
RUN pip install -r requirements.txt

COPY . .

CMD 'python manage.py runserver 0.0.0.0'
