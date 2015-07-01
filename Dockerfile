FROM alpine:3.2

RUN apk add --update py-pip python \
    && pip install -U pip \
    && rm -rf /var/cache/apk/* \
    && ln -s /usr/etc/tvdbapi_client /etc/tvdbapi_client

COPY . /tvdbapi_client/

WORKDIR /tvdbapi_client

RUN apk add --update git g++ python-dev \
    && pip install -U -r requirements.txt \
    && python setup.py install \
    && apk del git g++ python-dev \
    && rm -rf /var/cache/apk/* \
    && rm -rf .git/ \
    && rm -rf build/

VOLUME ["/usr/etc/tvdbapi_client"]
EXPOSE 5000

CMD ["/bin/sh"]

