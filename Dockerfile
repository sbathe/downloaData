FROM amancevice/pandas
#RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt-get update && apt-get install git
RUN addgroup --gid 1000 sb && \
    adduser --uid 1000 --gid 1000 sb
RUN mkdir -p /home/sb && chown sb:sb -R /home/sb
ADD src /downloadData/
ADD .git /downloadData/.git/
RUN mkdir -p /downloadData/{amfidata,json_data} && chown sb:sb -R /downloadData
USER sb
RUN cd /downloadData && pwd && pip install --upgrade pip --user && export PATH=/home/sb/.local/bin:$PATH \
    && export PYTHONPATH=/home/sb/.local/lib/python3.7/site-packages:$PYTHONPATH \
    && pip install -r amfi/build-requires.txt --user \
    && pip install -r amfi/requirements.txt --user \ 
    && python -V && python setup.py install -v --user
#VOLUME ["/downloadData/amfidata", "/downloadData/json_data"]
COPY bin/data.py /bin
ENV MONGOURL localhost:12707
ENV MONGOPASS aPass
ENV MONGOUSER aUser

ENTRYPOINT ["/usr/bin/env", "python", "/bin/data.py"]
