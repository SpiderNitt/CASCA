from flask import Flask
import psutil

app=Flask(__name__)

@app.route("/")
def stats():
    cpus = psutil.cpu_count()
    memory = psutil.virtual_memory().total/(1024*1024)
    cpu_util = psutil.cpu_percent()
    mem_util = psutil.virtual_memory().percent
    cpu_freq = psutil.cpu_freq().current
    return {
        "cpus": cpus,
        "memory": memory,
        "cpu_util": cpu_util,
        "mem_util": mem_util,
        "cpu_freq":cpu_freq,
    }

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)