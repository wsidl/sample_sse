import redis
from os import environ
import logging
import json
import time
import random

logging.basicConfig(level=logging.DEBUG)

logging.info(f'Connecting to "{environ.get("R_URL")}"')
r = redis.Redis.from_url(
    url=environ['R_URL']
)


def send_message(key: str, message: str):
    logging.info(f'sending "{key}" : "{message}"')
    r.publish(
        environ['R_TOPIC'],
        json.dumps({
            'key': key,
            'message': message
        })
    )


def main():
    logging.info('Starting Iterator')
    while True:
        send_message(
            str(random.randint(1, 10)),
            f'Sending Message: {random.random()}'
        )
        time.sleep(int(environ.get('DELAY', 2)))


if __name__ == '__main__':
    logging.info('Starting Generator')
    main()
