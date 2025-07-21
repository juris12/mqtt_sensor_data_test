import datetime

def parse(data: dict, save_sensor_data, topic_parts):
    try:
        timestamp = datetime.datetime.fromisoformat(data["time"].replace("Z", "+00:00"))
        mqtt_username = topic_parts[0]
        building_name = topic_parts[1]

        saved = False

        motor_position = int(data["motorPosition"])
        if 0 <= motor_position <= 100:
            saved |= save_sensor_data(
                mqtt_username, building_name, "vicki", timestamp, "motor_position", motor_position
            )

        open_percentage = float(data["openProcentage"])
        if 0.0 <= open_percentage <= 100.0:
            saved |= save_sensor_data(
                mqtt_username, building_name, "vicki", timestamp, "open_percentage", open_percentage
            )

        relative_humidity = int(data["relativeHumidity"])
        if 0 <= relative_humidity <= 100:
            saved |= save_sensor_data(
                mqtt_username, building_name, "vicki", timestamp, "relative_humidity", relative_humidity
            )

        sensor_temperature = float(data["sensorTemperature"])
        if -40.0 <= sensor_temperature <= 80.0:
            saved |= save_sensor_data(
                mqtt_username, building_name, "vicki", timestamp, "sensor_temperature", sensor_temperature
            )

        target_temperature = int(data["targetTemperature"])
        if 5 <= target_temperature <= 35:
            saved |= save_sensor_data(
                mqtt_username, building_name, "vicki", timestamp, "target_temperature", target_temperature
            )

        child_lock = bool(data["childLock"])
        saved |= save_sensor_data(
            mqtt_username, building_name, "vicki", timestamp, "child_lock", child_lock
        )

        open_window = bool(data["openWindow"])
        saved |= save_sensor_data(
            mqtt_username, building_name, "vicki", timestamp, "open_window", open_window
        )

        if saved:
            print(f"Saved cleaned Vicki data for {mqtt_username} / {building_name}")
            return "data saved"
        else:
            print(f"No valid Vicki data to save for {mqtt_username} / {building_name}")
            return "nothing valid to save"

    except (KeyError, ValueError, TypeError) as e:
        print(f"Error parsing Vicki data: {e}")
        return None
