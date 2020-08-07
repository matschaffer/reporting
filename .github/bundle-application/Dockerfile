FROM python:3.8.5

COPY requirements.txt /
RUN pip install --upgrade pip &&\
    pip install --use-feature=2020-resolver -r /requirements.txt

COPY entrypoint.py /
ENTRYPOINT ["python", "/entrypoint.py"]
