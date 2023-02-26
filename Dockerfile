FROM python:3

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY pembundle2jks.py /bin/pembundle2jks
RUN chmod a+x /bin/pembundle2jks

ENTRYPOINT [ "pembundle2jks" ]
