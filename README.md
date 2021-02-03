# 5geve-wp3-dcm-site-plugin script

This repository contains the logic needed for providing a REST API to the Site Brokers to be connected with the Data Collection Manager, in order to handle automatically the life cycle of the topics to be created/deleted in the broker.

Usage: `python3 dcm_site_plugin_rest_client.py [--site_ip_address <site_ip_address>] [--port <port_number>] [--kafka_topics_script_route <kafka_topics_script_route>] [--log <log_level>]`

Default IP address is localhost, default port is 8090, default kafka-topics.sh location is /opt/kafka/bin/kafka-topics.sh and default log level is info.

## Application API

The REST API provided by the `dcm_site_plugin_rest_client.py` can be seen in the corresponding api-docs files in this repository.

## Steps to be followed

First of all, install Python 3 in the server which will hold this script.

```shell
sudo apt install python3-pip
```

Then, export some variables related to the language.

```shell
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
```

After this, install the required packages for this Python script, which can be found in the requirements.txt file.

```shell
pip3 install -r requirements.txt
```

Finally, execute the script.

```shell
python3 dcm_site_plugin_rest_client.py --site_ip_address localhost --port 8090 --kafka_topics_script_route /opt/kafka/bin/kafka-topics.sh --log info
```
