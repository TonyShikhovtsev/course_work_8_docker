FROM python:3

WORKDIR /hw_code

COPY ./requirements.txt /hw_code

RUN pip install -r /hw_code/requirements.txt

COPY . .



