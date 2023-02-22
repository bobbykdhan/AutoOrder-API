
FROM docker.io/python:3.10-buster

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip


# Install Python dependencies

WORKDIR /app
ADD ./ /app
COPY ./requirements.txt requirements.txt
RUN apt-get -yq update && pip3 install --no-cache-dir -r requirements.txt

RUN apt-get install firefox-esr -y

COPY . .


RUN mkdir -p /app/drivers && chgrp -R 0 /app/drivers && chmod -R g+wrx /app/drivers
RUN mkdir -p /app/screenshots && chgrp -R 0 /app/screenshots && chmod -R g+wrx /app/screenshots
RUN mkdir -p /.cache && chgrp -R 0 /.cache && chmod -R g+wrx /.cache
RUN touch  /app/geckodriver.log && chgrp -R 0 /app/geckodriver.log && chmod -R a+wrx /app/geckodriver.log
RUN chown -R 1000:2000 /app

RUN groupadd ffgroup --gid 2000  \
    && useradd ffuser \
    --create-home \
    --home-dir /tmp/ffuser \
    --gid 2000 \
    --shell /bin/bash \
    --uid 1000

WORKDIR /app/



CMD ["uvicorn", "backend_server:app", "--port" , "8080", "--host", "0.0.0.0"]
