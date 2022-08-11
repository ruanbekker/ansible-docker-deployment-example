FROM python:3.8-alpine

ENV APP_TITLE Welcome
ENV APP_ENV Development

RUN pip install flask

WORKDIR /application
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/templates/*.html templates/
COPY src/handlers/*.py handlers/
COPY src/tests/*.py tests/
COPY src/*.py .

RUN pytest -v

CMD ["python", "app.py"]
