FROM python:3

WORKDIR /usr/src/app

COPY ./backend .
RUN pip install --no-cache-dir -r requirements.txt
#RUN python -m pip install pika --upgrade
EXPOSE 5001
CMD [ "python", "./server.py" ]
