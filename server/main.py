import redis
from os import environ
import logging
from flask import Flask, Response
import json

logging.basicConfig(level=logging.DEBUG)
app = Flask('')
MIME_TYPE = 'text/event-stream'
HEADERS = {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
}


@app.get('/sse')
def new_connection():

    def generate_messages():
        logging.info(f'Connecting to "{environ.get("R_URL")}"')
        r = redis.Redis.from_url(
            url=environ['R_URL']
        )
        subscriber = r.pubsub()
        logging.debug(f'Subscribing to "{environ["R_TOPIC"]}')
        subscriber.subscribe(environ['R_TOPIC'])
        for message in subscriber.listen():
            logging.debug(f'Received: "{message}"')
            if message is None:
                return
            
            if message['data'] == 1:
                continue
            yield f'event: NewAlert\ndata: {message["data"].decode("utf-8")}\n\n'
    return Response(generate_messages(), mimetype=MIME_TYPE, headers=HEADERS)


def main():
    app.run('0.0.0.0', 80)


if __name__ == '__main__':
    main()
