FROM python:3.12.0

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

CMD python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && python3 manage.py runserver 0.0.0.0:8000
