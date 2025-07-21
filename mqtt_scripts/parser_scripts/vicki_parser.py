# def parse(data: dict, save_sensor_data):
#     try:
#         cleaned_data = {
#             "application_id": int(data["applicationID"]),
#             "attached_backplate": bool(data["attachedBackplate"]),
#             "battery_voltage": float(data["batteryVoltage"]),
#             "broken_sensor": bool(data["brokenSensor"]),
#             "calibration_failed": bool(data["calibrationFailed"]),
#             "child_lock": int(data["childLock"]),
#             "dev_eui": data["devEUI"],
#             "device_name": data["deviceName"],
#             "high_motor_consumption": bool(data["highMotorConsumption"]),
#             "low_motor_consumption": bool(data["lowMotorConsumption"]),
#             "motor_position": int(data["motorPosition"]),
#             "motor_range": int(data["motorRange"]),
#             "new_version": bool(data["newVersion"]),
#             "open_percentage": float(data["openProcentage"]),
#             "open_window": bool(data["openWindow"]),
#             "perceive_as_online": bool(data["perceiveAsOnline"]),
#             "relative_humidity": int(data["relativeHumidity"]),
#             "sensor_temperature": float(data["sensorTemperature"]),
#             "target_temperature": int(data["targetTemperature"]),
#             "timestamp": data["time"],
#         }
#         return cleaned_data
#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing Vicki data: {e}")
#         return None
