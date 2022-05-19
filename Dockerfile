FROM python:3.10-alpine3.15

WORKDIR /home/code

ADD requirements.txt /home/code
RUN pip install --no-cache-dir -r requirements.txt

ADD . /home/code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
