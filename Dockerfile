FROM python:3.10.8
LABEL maintainer="b4oody"

ENV PYTHONNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR app/

RUN apt-get update && apt-get install -y netcat-traditional

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user /files/media
RUN chmod -R 755 /files/media


COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER my_user

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]