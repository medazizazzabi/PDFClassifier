FROM python:3.8.10

WORKDIR /Neoplis

COPY requirements.txt requirements.txt
COPY ./webapp ./webapp

RUN pip install -r requirements.txt

CMD ["python", "./webapp/main.py"]