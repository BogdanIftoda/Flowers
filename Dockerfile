FROM python:3.9.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY Pipfile /app/
RUN  pip install pipenv  \
  && pipenv lock --keep-outdated --requirements > requirements.txt \
  && pip install -r requirements.txt
COPY . /app/
EXPOSE 8000   
