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
            item["request_times"][0] = item["request_times"][1]
            item["request_times"][1] = time.clock()
            return item["response"]
    data = requests.get(url, params=in_params, headers=in_headers)
    buffered_urls.append({"url": url, "time": time.time(), "request_times":[time.clock() - 1, time.clock()], "params": in_params, "headers": in_headers, "response": data})
    return data

cleaning_thread = Thread(target=cleaningTask)