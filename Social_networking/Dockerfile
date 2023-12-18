FROM python:3.9-slim-buster

WORKDIR /app

# COPY requirements.txt .
# RUN pip3 install -r requirements.txt

RUN pip install --upgrade pip
RUN python -m pip install --upgrade pip setuptools

# RUN cat requirements.txt
# RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD  python manage.py runserver
