FROM python:3.9

RUN apt update && apt upgrade -y
RUN apt install python3-pip -y
RUN apt install wkhtmltopdf -y

COPY . /app
WORKDIR /app

RUN pip3 install -U -r requirements.txt
CMD python3 bot.py
