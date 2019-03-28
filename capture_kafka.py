#!/usr/bin/env python
import argparse

import cv2
import time
import io
from fastavro import writer, parse_schema

from kafka import KafkaProducer

schema = {
    'doc': 'Image capture',
    'name': 'ImageCapture',
    'namespace': 'test',
    'type': 'record',
    'fields': [
        {'name': 'timestamp', 'type': 'long'},
        {'name': 'image_jpeg', 'type': 'bytes'}
    ],
}
parsed_schema = parse_schema(schema)


def get_snapshot():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        if not cap.isOpened():
            print("error")
        print('Capturing image...')
        return_value, image = cap.read()
    finally:
        del cap

    if return_value:
        result, buf = cv2.imencode(".jpg", image)
        if result:
            return buf.tobytes()
    return None


def create_record(image):
    return {u'timestamp': time.time_ns(), u'image_jpeg': image}


def send_to_kafka(record, bootstrap_servers, topic, message_key):
    new_file = io.BytesIO()
    writer(new_file, parsed_schema, [record])
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, key_serializer=str.encode)
    producer.send(topic, key=message_key, value=new_file.getvalue())
    producer.flush()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--bootstrap-servers', required=True)
    parser.add_argument('--topic', required=True)
    parser.add_argument('--message-key', default='raspberry-pi-1')

    args = parser.parse_args()

    image = get_snapshot()
    if image is not None:
        record = create_record(image)
        send_to_kafka(record, args.bootstrap_servers, args.topic, args.message_key)
    else:
        print("Failed to capture image")


if __name__ == '__main__':
    main()
