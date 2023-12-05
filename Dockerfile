FROM python:3.11.2-bullseye

ARG DATABASE_URI
ARG SECRET_KEY
ARG PRODUCTION

ENV DATABASE_URI=${DATABASE_URI}
ENV SECRET_KEY=${SECRET_KEY}
ENV PRODUCTION=${PRODUCTION}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update

# setup python
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . /app/

RUN python manage.py migrate
RUN python manage.py collectstatic

# expose nginx
EXPOSE 8000
ENTRYPOINT ["gunicorn", "karirku.wsgi"]
