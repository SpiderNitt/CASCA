import requests

def get_sys_stats(host):
    url="http://"+host+":8080/"
    response=requests.get(url)
    response_json=response.json()
    return response_json