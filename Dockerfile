FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get upgrade

WORKDIR /app
RUN pip3 install pipenv

COPY . .
RUN pipenv sync

CMD [ "pipenv", "run" , "python", "run_alerter.py"]

