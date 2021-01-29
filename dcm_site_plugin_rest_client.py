import requests
import argparse
import logging
import coloredlogs
from flask import Flask, request, jsonify
from flask_swagger import swagger
from waitress import serve
import subprocess
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.future import log
import json

app = Flask(__name__)
logger = logging.getLogger("DCMSitePluginRestClient")

@app.route('/', methods=['GET'])
def server_status():
    """
    Get status.
    ---
    describe: get status
    responses:
      200:
        description: OK
    """
    logger.info("GET /")
    return '', 200

@app.route("/spec", methods=['GET'])
def spec():
    """
    Get swagger specification.
    ---
    describe: get swagger specification
    responses:
      swagger:
        description: swagger specification
    """
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "DCM Site Plugin REST API"
    return jsonify(swag)

@app.route('/dcm_plugin/<topic>', methods=['POST'])
def create_topic(topic):
    """
    Create Kafka topic.
    ---
    describe: create Kafka topic
    parameters:
      - in: path
        name: topic
        type: string
        description: topic name
    responses:
      200:
        description: successful result
      500:
        description: error during the execution
    """
    logger.info("Request received - POST /dcm_plugin")
    try:
        subprocess.call(['/bin/bash', kafka_topics_script_route, '--create', '--zookeeper', site_ip_address+":2181", '--replication-factor', '1', '--partitions', '1', '--topic', topic])
    except Exception as e:
        logger.error("Error executing command")
        logger.exception(e)
        return str(e), 500
    return '', 200

@app.route('/dcm_plugin/<topic>', methods=['DELETE'])
def delete_topic(topic):
    """
    Delete Kafka topic.
    ---
    describe: delete Kafka topic
    parameters:
      - in: path
        name: topic
        type: string
        description: topic name
    responses:
      200:
        description: successful result
      500:
        description: error during the execution
    """
    logger.info("Request received - DELETE /dcm_plugin")
    try:
        subprocess.call(['/bin/bash', kafka_topics_script_route, '--delete', '--zookeeper', site_ip_address+":2181", '--topic', topic])
    except Exception as e:
        logger.error("Error executing command")
        logger.exception(e)
        return str(e), 500
    return '', 200

def checkValidPort(value):
    ivalue = int(value)
    # RFC 793
    if ivalue < 0 or ivalue > 65535:
        raise argparse.ArgumentTypeError("%s is not a valid port" % value)
    return value

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site_ip_address",
        help='Site IP address, default IP is localhost',
        default='localhost')
    parser.add_argument(
        "--port",
        type=checkValidPort,
        help='The port you want to use as an endpoint, default port is 8090',
        default="8090")
    parser.add_argument(
        "--kafka_topics_script_route",
        help='Route to find the kafka-topics.sh script',
        default='/opt/kafka/bin/kafka-topics.sh')
    parser.add_argument(
        "--log",
        help='Sets the Log Level output, default level is "info"',
        choices=[
            "info",
            "debug",
            "error",
            "warning"],
        nargs='?',
        default='info')

    args = parser.parse_args()
    numeric_level = getattr(logging, str(args.log).upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    coloredlogs.install(
        fmt='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=numeric_level)
    logging.getLogger("DCMSitePluginRestClient").setLevel(numeric_level)
    logging.getLogger("requests.packages.urllib3").setLevel(logging.ERROR)

    args = parser.parse_args()
    global site_ip_address 
    site_ip_address= str(args.site_ip_address)

    global kafka_topics_script_route
    kafka_topics_script_route = str(args.kafka_topics_script_route)

    logger.info("Serving DCMSitePluginRestClient on port %s", str(args.port))
    serve(app, host='0.0.0.0', port=args.port)
