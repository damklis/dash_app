FROM python:3.7

USER root 

RUN apt-get update -y
RUN apt-get install -y g++ libsasl2-dev libsasl2-modules

ADD . /app

RUN chmod -x /app/dashboard/dash_app.py

WORKDIR /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 80

ENTRYPOINT ["/app"]

CMD ["python", "dashboard/dash_app.py"]
