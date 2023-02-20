
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


WORKDIR /app/

CMD ["uvicorn", "backend_server:app", "--port" , "8080", "--host", "0.0.0.0"]
