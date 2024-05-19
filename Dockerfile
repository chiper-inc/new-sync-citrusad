FROM python:3.9

WORKDIR /sync-catalog-citrusad
ADD . /sync-catalog-citrusad

ADD start.py /
RUN pip install -r requirements.txt

CMD python start.py