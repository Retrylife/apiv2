from databuffer.data import buffered_urls, timeout
from threading import Thread
import time
import requests

def cleaningTask():
    while True:
        for c, item in enumerate(buffered_urls):
            if (time.time() - item["time"]) > timeout:
                buffered_urls.pop(c)
        time.sleep(timeout / 2)

def inquire(url, params={}, headers={}):
    in_params = params
    in_headers = headers
    for item in buffered_urls:
        if item["url"] == url:
            return item["response"]
    data = requests.get(url, params=in_params, headers=in_headers)
    buffered_urls.append({"url": url, "time": time.time(), "params": in_params, "headers": in_headers, "response": data})
    return data

cleaning_thread = Thread(target=cleaningTask)