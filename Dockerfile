FROM python3

RUN apt-get update -y
RUN apt-get install -y g++ libsasl2-dev libsasl2-modules

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

RUN (crontab -l; echo "0 5,11,17,23 * * * cd /opt/dash_app ; python3 query.py") | crontab -
RUN (crontab -l; echo "0 0,6,12,18 * * * supervisorctl restart app") | crontab -

ADD . /opt/dash_app
ADD ./supervisor/* /etc/supervisor/conf.d/
RUN chmod -x /opt/dash_app/dash_app.py

EXPOSE 80
