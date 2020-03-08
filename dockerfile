FROM python:3

WORKDIR /usr/src/app

COPY ./backend .
RUN pip install --no-cache-dir -r requirements.txt
#RUN python -m pip install pika --upgrade

CMD [ "python", "./server.py" ]
EXPOSE 5000