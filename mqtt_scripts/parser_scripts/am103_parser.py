import datetime

def parse(data: dict, save_sensor_data, topic_parts):
    try:
        timestamp = datetime.datetime.fromisoformat(data["time"].replace("Z", "+00:00"))
        mqtt_username = topic_parts[0]
        building_name = topic_parts[1]

        co2 = int(data["co2"])
        humidity = float(data["humidity"])
        temperature = float(data["temperature"])
        saved = False
        if 1 < co2 < 2000:
            saved |= save_sensor_data(
                mqtt_username, building_name, "am103_co2", timestamp, "co2_level", co2
            )

        if 0.0 <= humidity <= 100.0:
            saved |= save_sensor_data(
                mqtt_username, building_name, "am103_humidity", timestamp, "humidity_percent", humidity
            )

        if -40.0 <= temperature <= 80.0:
            saved |= save_sensor_data(
                mqtt_username, building_name, "am103_temperature", timestamp, "temperature_c", temperature
            )

        if saved:
            print(f"Saved cleaned am103 data for {mqtt_username} / {building_name}")
            return "data saved"
        else:
            print(f"No valid AM103 data to save for {mqtt_username} / {building_name}")
            return "nothing valid to save"

    except (KeyError, ValueError, TypeError) as e:
        print(f"Error parsing AM103 data: {e}")
        return None
