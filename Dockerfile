FROM python:3.7-alpine
RUN addgroup -g 1000 sb && \
    adduser -D -u 1000 -G sb sb

RUN mkdir -p /home/sb && chown sb:sb -R /home/sb
RUN apk add git 
ADD src /downloaData/
ADD .git /downloaData/.git/
RUN mkdir -p /downloaData/{amfidata,json_data} && chown sb:sb -R /downloaData
USER sb
RUN cd /downloaData && pwd && pip install --upgrade pip --user && export PATH=/home/sb/.local/bin:$PATH \
    && export PYTHONPATH=/home/sb/.local/lib/python3.7/site-packages:$PYTHONPATH \
    && pip install -r amfi/build-requires.txt --user \
    && pip install -r amfi/requirements.txt --user \ 
    && python -V && python setup.py install -v --user
#VOLUME ["/downloaData/amfidata", "/downloaData/json_data"]
COPY bin/data.py /bin
ENTRYPOINT ['python', '/bin/data.py']
