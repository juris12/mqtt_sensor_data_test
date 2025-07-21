# def parse(data: dict, save_sensor_data):
#     try:
#         cleaned_data = {
#             "dev_eui": data["devEUI"],
#             "device": data["device"],
#             "ok": bool(data["ok"]),
#             "volumes": [
#                 {
#                     "hour": int(entry["hour"]),
#                     "value": int(entry["val"])
#                 }
#                 for entry in data["volumes"]
#             ],
#             "timestamp": data["time"],
#         }
#         return cleaned_data
#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing Zenner SP12 data: {e}")
#         return None
