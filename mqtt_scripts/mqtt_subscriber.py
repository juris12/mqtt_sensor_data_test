import paho.mqtt.client as mqtt
import json
import importlib
from save_to_db import save_sensor_data

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = "monitor"
MQTT_PASSWORD = "monitorpass"

def load_parser(sensor_name):
    try:
        parser_module = importlib.import_module(f'parser_scripts.{sensor_name}_parser')
        return parser_module.parse
    except:
        print(f"No parser found for {sensor_name}, skipping.")
        return None


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to everything from all clients
    client.subscribe("#")


def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        if len(topic_parts) < 4:
            print(f"Ignoring malformed topic: {msg.topic}")
            return
        
        user, building, _, sensor_name = topic_parts

        data = json.loads(msg.payload.decode())
        parser_func = load_parser(sensor_name.lower())
        if parser_func is None:
            # print(f"{sensor_name} does not have parser func!")
            return
        if parser_func != "data saved":
            cleaned_data = parser_func(data, save_sensor_data, topic_parts)
            # save_sensor_data(
            #     sensor_type=sensor_name.lower(),
            #     user=user,
            #     building=building,
            #     timestamp=cleaned_data["timestamp"],
            #     value=cleaned_data["value"],
            #     unit=cleaned_data["unit"]
            # )
        print(f"Saved cleaned {sensor_name} data for {user} / {building}")

    except Exception as e:
        print(f"Error processing message: {e}")


client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()
