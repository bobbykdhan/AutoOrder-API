
FROM seleniarm/standalone-firefox:latest
USER 0
# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip build-essential pipx screen python3-venv
USER 1200


WORKDIR /app

# Password handling
RUN #x11vnc -storepasswd <your-password-here> /home/seluser/.vnc/passwd
ENV SE_VNC_NO_PASSWORD=1
RUN cd /opt && ls -la

COPY requirements.txt /tmp/
ADD image.py /app
ADD login.py /app
ADD order_manager.py /app
ADD backend_server.py /app
ADD my_twilio.py /app
ADD webdriver_handler.py /app
ADD start_both.sh /app
ADD start-selenium-standalone.sh /opt/bin/
USER 0
RUN python3 -m venv /app/venv
RUN chmod a+x /opt/bin/start-selenium-standalone.sh && chmod a+x /app/start_both.sh

RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r /tmp/requirements.txt


EXPOSE 7900
EXPOSE 5900
EXPOSE 4444
EXPOSE 8080


#COPY . .

#RUN ["screen -d -m /opt/bin/start-selenium-standalone.sh"]
#CMD ["screen -d -m /app/venv/bin/python /app/backend_server.py"]
USER 1200
CMD ["/app/start_both.sh"]
#CMD ["/opt/bin/start-selenium-standalone.sh"]
#ENTRYPOINT "/app/venv/bin/python" "/app/backend_server.py"