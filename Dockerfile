FROM python:3.9

ENV DEBIAN_FRONTEND=noninteractive

ADD model/ /model
COPY requirements.txt /requirements.txt
COPY predict.py /predict.py

RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt && python3.9 -m pip install gunicorn

COPY app.py /app.py

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:9000", "app:app"]
