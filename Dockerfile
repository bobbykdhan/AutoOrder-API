
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

RUN groupadd ffgroup --gid 2000  \
    && useradd ffuser \
    --create-home \
    --home-dir /tmp/ffuser \
    --gid 2000 \
    --shell /bin/bash \
    --uid 1000

RUN chgrp -R 0 /tmp && chmod -R a+wrx /tmp
RUN chmod g+s /tmp
RUN mkdir -p /app/drivers && chgrp -R 0 /app/drivers && chmod -R a+wrx /app/drivers
RUN mkdir -p /app/screenshots && chgrp -R 0 /app/screenshots && chmod -R a+wrx /app/screenshots
RUN chgrp -R 0 /tmp/ffuser && chmod -R a+wrx /tmp/ffuser
RUN mkdir -p /.cache && chgrp -R 0 /.cache && chmod -R a+wrx /.cache
RUN touch  /app/geckodriver.log && chgrp -R 0 /app/geckodriver.log && chmod -R a+wrx /app/geckodriver.log
RUN #touch  mkdir /var/www/.mozilla && chgrp -R 0 mkdir /var/www/.mozilla && chmod -R a+wrx mkdir /var/www/.mozilla
RUN #touch  mkdir /var/www/.cache && chgrp -R 0 mkdir /var/www/.cache && chmod -R a+wrx mkdir /var/www/.cache
RUN chgrp root /app




WORKDIR /app/


USER ROOT
#CMD ["su", "-", "ffuser", "-c" , "'uvicorn", "backend_server:app", "--port" , "8080", "--host", "0.0.0.0'"]
CMD ["uvicorn", "backend_server:app", "--port" , "8080", "--host", "0.0.0.0"]
