import os
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='db-service', port=6379)

@app.route('/')
def index():
    hits = cache.incr('hits')
    container_id = os.environ.get('HOSTNAME', 'inconnu')
    return f"Bonjour ! Cette page a été vue {hits} fois. Je suis le conteneur [{container_id}]"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)