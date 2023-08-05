# Stage 0: build twweb
######################
FROM python:3-alpine as builder

RUN apk add \
    git

WORKDIR /build
COPY . .
RUN python3 setup.py bdist_wheel

# Stage 1: create twweb's image
###############################
FROM python:3-alpine

EXPOSE 5456

RUN apk --no-cache add \
    build-base \
    task \
    linux-headers \
    pcre-dev

# Install twweb
WORKDIR /tmp/twweb

COPY --from=builder /build/dist/*.whl .
RUN pip3 install \
    uwsgi \
    *.whl \
&& rm -rf /tmp/twweb \
&& rm -rf /root/.cache/pip/*

COPY docker /

# By default TWW_SECRET is empty, which will cause generating it at the runtime
ENV TWW_CFG_SECRET=
ENV TWW_CFG_PIN twweb
ENV TWW_CFG_DB_ENGINE sqlite
ENV TWW_CFG_DB_HOST /data/twweb.db
ENV TWW_CFG_TW_TASKRC /data/taskrc

# A place where twweb's configuration will be generated at the runtime.
ENV TWWEB_SETTINGS /data/twweb.cfg

ENTRYPOINT ["twweb-entrypoint"]

VOLUME /data
WORKDIR /data

CMD uwsgi --ini /data/uwsgi.ini
