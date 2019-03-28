# Pre-requisites
    
    * Python 3
    * virtualenv

# Installing system requirements

    sudo apt-get install libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

Or

    sudo apt-get install python-opencv

# Python Environment

    virtualenv -p $(which python3) venv
    
    source venv/bin/activate
    
    pip install -r requirements.txt
    
# Examples

## Image Capture using OpenCV

This is suitable for USB WebCam

    python ./capture_file.py

## Image Capture using Pi Camera

## Image Camera to Kafka

    ./capture_kafka.py

## Image Camera to MQTT

### Generate Device's private key

    ssh-keygen -t rsa -b 4096 -m PEM -f private-key.key
    openssl rsa -in private-key.key -pubout -outform PEM -out public-key.pem
    
### Register device in MQTT registry

Register the device in the GCP's MQTT registry and upload the device's public key 
    
### Running capture    

    capture_gcp_mqtt.py \
        --algorithm RS256 \
        --device_id <device id> \
        --private_key_file <device's private key> \
        --registry_id <mqtt registry> \
        --project_id <gcp project> \
        --cloud_region <gcp region>