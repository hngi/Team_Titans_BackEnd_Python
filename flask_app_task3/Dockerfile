FROM python:3.6.1-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN export FLASK_APP=sms.py
CMD gunicorn sms:flask_app --bind 0.0.0.0:$PORT --reload
