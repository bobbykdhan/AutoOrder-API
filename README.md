# AutoOrder-API

Allows the user to order from on demand using HTTP requests to an API I created. Uses Selenium and Python to navigate through OnDemand in a headless browser hosted in a Docker container. 

Adapted from [AutoOrder](https://github.com/bobbykdhan/AutoOrder). Now allows the orders to be process none interactivly and allows better automation.

## Installation

```
git clone https://github.com/bobbykdhan/AutoOrder-API.git
pip install -r requirements.txt
docker build -t <image_tag> . && docker run -p 127.0.0.1:4444:4444 -p 127.0.0.1:7900:7900 -p 127.0.0.1:5900:5900 -p 127.0.0.1:8080:8080 --name SeleniumFirefox <image_tag> 
```

## Demo

Coming Soon


## Frameworks used

[Selenium](https://www.selenium.dev) - Used to automate the browser and send the commands.
[FastAPI](https://fastapi.tiangolo.com) - Used to handle the api requests for the orders

## License
GNU GPLv3 © Bobby Dhanoolal
