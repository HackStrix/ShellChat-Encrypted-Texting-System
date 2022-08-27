FROM python

WORKDIR /usr/src/server

COPY requirements.txt /usr/src/server/requirements.txt

COPY server.py /usr/src/server/server.py

RUN pip3 install -r requirements.txt
CMD python3 server.py

EXPOSE 5000