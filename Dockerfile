FROM python:3.10.8-slim

RUN mkdir /app

COPY ./bbq_manager/requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY bbq_manager/ /app

WORKDIR /app

CMD ["gunicorn", "bbq_manager.wsgi:application", "--bind", "0:8000" ]