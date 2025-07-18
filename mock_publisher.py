import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# User credentials dictionary
USER_CREDENTIALS = {
    "dd": "dd",
    "monitor": "monitorpass"  # Special monitoring user
}

# Sensor templates with more realistic data patterns
import random
import datetime
def get_current_time():
    return datetime.datetime.now(datetime.UTC)

def get_current_time_iso():
    return get_current_time().isoformat(timespec='milliseconds') + "Z"

def get_current_hour():
    return get_current_time().hour

def get_dt_timestamp():
    return f"DT#{get_current_time().strftime('%Y-%m-%d-%H:%M:%S')}"


SENSOR_TEMPLATES = {
    "AM103": {
        "battery": lambda: random.randint(40, 50),  # Typically around 44
        "co2": lambda: random.randint(500, 550),   # Typically around 512
        "devEUI": "24e124725d021011",
        "humidity": lambda: random.randint(45, 50), # Typically around 48
        "temperature": lambda: round(random.uniform(21.5, 22.5), 1),  # Typically around 22.1
        "time": lambda: datetime.datetime.utcnow().isoformat() + "Z"
    },
    "UC300": {
        "OstasSkati_cold_side": lambda: random.randint(2450, 2500),  # Typically around 2480
        "OstasSkati_current_flow": 0,
        "OstasSkati_current_power": 0,
        "OstasSkati_energy": 1429938,
        "OstasSkati_hot_side": lambda: random.randint(2450, 2480),  # Typically around 2460
        "OstasSkati_temp_diff": lambda: random.randint(-25, -15),  # Typically around -20
        "adv_1": 0,
        "devEUI": "24e124445d226973",
        "gpio_in_1": "off",
        "gpio_in_2": "off",
        "gpio_in_3": "off",
        "gpio_in_4": "off",
        "gpio_out_1": "off",
        "gpio_out_2": "off",
        "pt100_1": lambda: round(random.uniform(12.0, 12.5), 1),  # Typically around 12.2
        "pt100_2": lambda: round(random.uniform(12.0, 12.5), 1),  # Typically around 12.1
        "time": lambda: datetime.datetime.utcnow().isoformat() + "Z"
    },
    "Vicki": {
        "applicationID": 5,
        "attachedBackplate": True,
        "batteryVoltage": 3.3,
        "brokenSensor": False,
        "calibrationFailed": False,
        "childLock": 1,
        "devEUI": "70b3d52dd301015d",
        "deviceName": "Vicki-VWMT",
        "highMotorConsumption": False,
        "lowMotorConsumption": False,
        "motorPosition": lambda: random.randint(0, 10),  # Typically around 6
        "motorRange": 515,
        "newVersion": True,
        "openProcentage": lambda: round(random.uniform(95, 100), 6),  # Typically around 98.83
        "openWindow": False,
        "perceiveAsOnline": True,
        "relativeHumidity": lambda: random.randint(45, 55),  # Typically around 50
        "sensorTemperature": lambda: round(random.uniform(23.0, 24.0), 6),  # Typically around 23.588
        "targetTemperature": 24,
        "time": lambda: datetime.datetime.utcnow().isoformat() + "Z"
    },
    "ZennerSP12": {
        "devEUI": "04b6480450052428",
        "device": "ZennerSP12",
        "ok": True,
        "volumes": lambda: [
            {"hour": (datetime.datetime.utcnow().hour - 2) % 24, "val": random.randint(1024000, 1024500)},
            {"hour": (datetime.datetime.utcnow().hour - 1) % 24, "val": random.randint(1024500, 1024700)},
            {"hour": datetime.datetime.utcnow().hour % 24, "val": random.randint(1024700, 1025000)}
        ],
        "time": lambda: datetime.datetime.utcnow().isoformat() + "Z"
    },
    "EL_uzskaite_3": {
        "SN": "105945",
        "name": "EL_uzskaite_3",
        "header": {
            "startTime": lambda: datetime.datetime.utcnow().isoformat(timespec='milliseconds') + "Z",
            "endTime": lambda: datetime.datetime.utcnow().isoformat(timespec='milliseconds') + "Z",
            "recordCount": 1,
            "columns": {
                "0": {
                    "id": "0",
                    "name": "Sk1_aktiva_jauda",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "1": {
                    "id": "1",
                    "name": "SK1_kopeja_jauda",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "2": {
                    "id": "2",
                    "name": "Sk1_aktivas_en_paterins",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "3": {
                    "id": "3",
                    "name": "Sk1_reaktivas_en_paterins",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "4": {
                    "id": "4",
                    "name": "Sk2_aktiva_jauda",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "5": {
                    "id": "5",
                    "name": "SK2_kopeja_jauda",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "6": {
                    "id": "6",
                    "name": "Sk2_aktivas_en_paterins",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "7": {
                    "id": "7",
                    "name": "Sk2_reaktivas_en_paterins",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "8": {
                    "id": "8",
                    "name": "Sk3_aktiva_jauda",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "9": {
                    "id": "9",
                    "name": "SK3_kopeja_jauda",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "10": {
                    "id": "10",
                    "name": "Sk3_aktivas_en_paterins",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "11": {
                    "id": "11",
                    "name": "Sk3_reaktivas_en_paterins",
                    "dataType": "NUMBER",
                    "format": "float"
                },
                "12": {
                    "id": "12",
                    "name": "61_imports",
                    "dataType": "NUMBER",
                    "format": "signed long long"
                },
                "13": {
                    "id": "13",
                    "name": "61_eksports",
                    "dataType": "NUMBER",
                    "format": "signed long long"
                },
                "14": {
                    "id": "14",
                    "name": "61_frekvence",
                    "dataType": "NUMBER",
                    "format": "unsigned short"
                },
                "15": {
                    "id": "15",
                    "name": "62_imports",
                    "dataType": "NUMBER",
                    "format": "signed long long"
                },
                "16": {
                    "id": "16",
                    "name": "62_eksports",
                    "dataType": "NUMBER",
                    "format": "signed long long"
                },
                "17": {
                    "id": "17",
                    "name": "63_imports",
                    "dataType": "NUMBER",
                    "format": "signed long long"
                },
                "18": {
                    "id": "18",
                    "name": "63_eksports",
                    "dataType": "NUMBER",
                    "format": "signed long long"
                }
            }
        },
        "data": [{
            "ts": lambda: datetime.datetime.utcnow().isoformat(timespec='milliseconds') + "Z",
            "f": {
                "0": {"v": round(random.uniform(75, 85), 4)},  # Sk1_aktiva_jauda
                "1": {"v": round(random.uniform(85, 90), 4)},   # SK1_kopeja_jauda
                "2": {"v": round(random.uniform(1500000, 1600000), 4)},  # Sk1_aktivas_en_paterins
                "3": {"v": round(random.uniform(600000, 700000), 4)},    # Sk1_reaktivas_en_paterins
                "4": {"v": round(random.uniform(1.0, 2.0), 4)},         # Sk2_aktiva_jauda
                "5": {"v": round(random.uniform(1.0, 2.0), 4)},         # SK2_kopeja_jauda
                "6": {"v": round(random.uniform(20000, 25000), 4)},      # Sk2_aktivas_en_paterins
                "7": {"v": round(random.uniform(0.1, 0.2), 4)},          # Sk2_reaktivas_en_paterins
                "8": {"v": round(random.uniform(35, 40), 4)},            # Sk3_aktiva_jauda
                "9": {"v": round(random.uniform(40, 45), 4)},            # SK3_kopeja_jauda
                "10": {"v": round(random.uniform(190000, 200000), 4)},   # Sk3_aktivas_en_paterins
                "11": {"v": round(random.uniform(110000, 120000), 4)},   # Sk3_reaktivas_en_paterins
                "12": {"v": random.randint(380000000, 390000000)},       # 61_imports
                "13": {"v": random.randint(200000000, 210000000)},      # 61_eksports
                "14": {"v": 5001},                                      # 61_frekvence
                "15": {"v": random.randint(30000, 40000)},               # 62_imports
                "16": {"v": random.randint(230000000, 240000000)},       # 62_eksports
                "17": {"v": random.randint(20000, 30000)},               # 63_imports
                "18": {"v": random.randint(240000000, 250000000)}        # 63_eksports
            }
        }]
    },
    "SK1-P14": {
        "Lib_version": "v1.2",
        "name": "SK1-P14",
        "manufacturer": "Schneider",
        "model": "iEM3250",
        "type": "Electric meters",
        "slave_id": 1,
        "DPS": lambda: [
            {
                "SN": 23516044,
                "reg_nr": 129,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Curr_avg": round(random.uniform(0.5, 0.7), 3),
                "reg_nr": 3009,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Curr_fr": round(random.uniform(49.9, 50.1), 3),
                "reg_nr": 3109,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "TAP": round(random.uniform(0.2, 0.25), 3),
                "reg_nr": 3059,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "TEI": round(random.uniform(1300, 1400), 3),
                "reg_nr": 45099,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "LL_avg": round(random.uniform(400, 405), 3),
                "reg_nr": 3025,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            }
        ]
    },
    "TP_wago": {
        "Lib_version": "v1.2",
        "name": "TP_wago",
        "manufacturer": "WAGO",
        "model": "751-9301",
        "serial": "37SUN31564010260470190+0000000002428588",
        "type": "PLC",
        "DPS": lambda: [
            {
                "max strava": round(random.uniform(900, 950), 3),
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "TP1_temp": round(random.uniform(26.0, 27.5), 1),
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "TP2_temp": round(random.uniform(30.0, 31.0), 1),
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_TP1": 0,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_TP2": 0,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            }
        ]
    },
    "PN_4": {
        "Lib_version": "v1.2",
        "name": "PN_4",
        "manufacturer": "Corrigo",
        "model": "E_G3",
        "serial": "012110194059",
        "type": "AHU",
        "slave_id": 1,
        "DPS": lambda: [
            {
                "UnitRunMode": 2,
                "reg_nr": 283,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "RunMode": 5,
                "reg_nr": 2,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Temp_SupplyAir": 201,
                "reg_nr": 6,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Temp_ExtractAir": 0,
                "reg_nr": 8,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Temp_Room1": 0,
                "reg_nr": 9,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Temp_Room2": 0,
                "reg_nr": 10,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "CO2_Level": 0,
                "reg_nr": 16,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Humidity_Duct": 0,
                "reg_nr": 23,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Humidity_Room": 0,
                "reg_nr": 22,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_SupplyAirTemp": 200,
                "reg_nr": 0,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_CO2": 3,
                "reg_nr": 31,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_Humidity": 500,
                "reg_nr": 36,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Control_Mode": 3,
                "reg_nr": 367,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_SuppECO": 300,
                "reg_nr": 424,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_SuppNormal": 400,
                "reg_nr": 423,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_ExhEco": 300,
                "reg_nr": 426,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Setpoint_ExhNormal": 400,
                "reg_nr": 425,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_Frost": 0,
                "reg_nr": 40,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_Fire": 0,
                "reg_nr": 42,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_Overheated": 0,
                "reg_nr": 55,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_SupplyFan": 0,
                "reg_nr": 33,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_ExtractFan": 0,
                "reg_nr": 34,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_Heater": 0,
                "reg_nr": 35,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_Cooler": 0,
                "reg_nr": 36,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_Exchanger": 0,
                "reg_nr": 37,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            },
            {
                "Alarm_AckById": 255,
                "reg_nr": 399,
                "ts": f"DT#{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            }
        ]
    }
}


def evaluate_callables(data):
    if callable(data):
        return evaluate_callables(data())
    elif isinstance(data, dict):
        return {k: evaluate_callables(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [evaluate_callables(item) for item in data]
    else:
        return data
    
def publish_mock_data():
    clients = {}
    buildings = ["building_1", "building_2", "building_3"]
    
    # Create clients for each user
    for user, password in USER_CREDENTIALS.items():
        if user != "monitor":  # Skip monitor user for publishing
            client = mqtt.Client()
            client.username_pw_set(user, password)
            client.connect(MQTT_BROKER, MQTT_PORT)
            clients[user] = client
    
    try:
        while True:
            for user, client in clients.items():
                for building in buildings:
                    for sensor_name, sensor_template in SENSOR_TEMPLATES.items():
                        topic = f"{user}/{building}/sensors/{sensor_name.lower()}"
                        # Evaluate the sensor data by calling any lambda functions
                        data = evaluate_callables(sensor_template)
                        
                        try:
                            json_data = json.dumps(data)
                            client.publish(topic, json_data)
                            print(f"Published to {topic}: {json.dumps(data, indent=2)}")
                        except Exception as e:
                            print(f"Error publishing {sensor_name}: {str(e)}")
                            continue
                            
                        
                        client.publish(topic, json.dumps(data))
                        print(f"Published to {topic}: {json.dumps(data, indent=2)}")
            time.sleep(30)
    except KeyboardInterrupt:
        for client in clients.values():
            client.disconnect()

if __name__ == "__main__":
    publish_mock_data()

if __name__ == "__main__":
    publish_mock_data()