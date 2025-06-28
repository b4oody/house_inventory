FROM python:3.10.8
LABEL maintainer="b4oody"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/


RUN apt-get update && apt-get install -y netcat-traditional


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN mkdir -p /app/staticfiles /app/media
RUN chown -R my_user:my_user /app


USER my_user


ENTRYPOINT ["/app/entrypoint.sh"]


CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]