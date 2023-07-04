# pull official base image
FROM python:3.8.5-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev dos2unix tzdata jpeg-dev zlib-dev g++ libffi-dev openssl-dev rust cargo

WORKDIR /usr/share/zoneinfo
RUN cp /usr/share/zoneinfo/Europe/Nicosia /etc/localtime
WORKDIR /usr/src/app
# install dependencies
RUN pip install --upgrade pip
COPY . .
#COPY ./requirements.txt .
RUN pip install -r requirements.txt
#COPY ./entry/entrypoint.sh .
RUN dos2unix entrypoint.env.sh
RUN chmod +x entrypoint.env.sh
ENTRYPOINT ["/usr/src/app/entrypoint.env.sh"]