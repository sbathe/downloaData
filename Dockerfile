ARG ALPINE_VERSION=3.10
ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS base
WORKDIR /var/lib/pandas/
COPY Pipfile* /var/lib/pandas/
RUN pip install pipenv==2018.11.26 && \
    pipenv lock -r > requirements.txt && \
    pipenv lock -r -d > requirements-dev.txt

FROM alpine:${ALPINE_VERSION} as alpine-pandas
WORKDIR /var/lib/pandas/
COPY --from=base /var/lib/pandas/ .
RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache --virtual .build-deps g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install -r requirements.txt && \
    apk del .build-deps


FROM alpine-pandas
RUN apk add git py-pip
RUN addgroup -g 1000 sb && \
    adduser -u 1000 -G sb -D sb
#RUN mkdir -p /home/sb && chown sb:sb -R /home/sb
ADD src /downloadData/
ADD .git /downloadData/.git/
RUN mkdir -p /downloaData/{amfidata,jsondata}
RUN cd /downloadData && pwd && pip install --upgrade pip && export PATH=/home/sb/.local/bin:$PATH \
    && export PYTHONPATH=/home/sb/.local/lib/python3.7/site-packages:$PYTHONPATH \
    && pip install -r amfi/build-requires.txt \
    && pip install -r amfi/requirements.txt \
    && python -V && pwd && ls -la && python setup.py install -v
RUN chown sb:sb -R /downloaData
COPY bin/data.py /bin
USER sb
ENV MONGOURL localhost:12707
ENV MONGOPASS aPass
ENV MONGOUSER aUser

ENTRYPOINT ["/usr/bin/env", "python", "/bin/data.py"]
