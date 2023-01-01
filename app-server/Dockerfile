FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD *.py /app
 
EXPOSE 5000

CMD [ "python3", "app.py"]