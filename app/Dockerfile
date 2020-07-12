FROM python:3.8.1

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# add app
COPY . /app

# set working directory
WORKDIR /
CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "app.wsgi:app"]