# def parse(data: dict, save_sensor_data):
#     try:
#         parsed_data = {
#             "lib_version": data["Lib_version"],
#             "name": data["name"],
#             "manufacturer": data["manufacturer"],
#             "model": data["model"],
#             "serial": data["serial"],
#             "type": data["type"],
#         }

#         # Flatten DPS measurements except timestamps
#         parsed_fields = {}
#         for entry in data["DPS"]:
#             for key, value in entry.items():
#                 if key != "ts":
#                     parsed_fields[key] = value

#         cleaned_data = {
#             **parsed_data,
#             **parsed_fields
#         }
#         return cleaned_data

#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing TP_wago data: {e}")
#         return None
