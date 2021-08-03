FROM python:3.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache build-base libxml2-dev libxslt-dev git nodejs npm g++ make libffi-dev && rm -rf /var/cache/apk/*

# update pip
RUN python -m pip install wheel

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

COPY . /app

RUN set -ex && pip3 install -r requirements.txt

RUN npm install

RUN npm rebuild node-sass

RUN npm run build

ENV PORT=7001

CMD ["sh", "-c", "gunicorn -c gunicorn_config.py application"]