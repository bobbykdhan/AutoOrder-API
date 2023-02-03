FROM selenium/standalone-chrome:latest

# Install Python
RUN #apt-get update && apt-get install -y python3 python3-pip


# Install Python dependencies

WORKDIR /app
ADD ./ /app
COPY ./requirements.txt requirements.txt
RUN sudo apt-get -yq update && sudo apt-get install -y python3 python3-pip && \
    sudo pip3 install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/

CMD ["uvicorn", "main:app"]
