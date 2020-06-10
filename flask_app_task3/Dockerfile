FROM python:3.6.1-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN export FLASK_APP=sms.py
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0" ]
