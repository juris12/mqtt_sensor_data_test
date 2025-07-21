# def parse(data: dict, save_sensor_data):
#     try:
#         base = {
#             "lib_version": data["Lib_version"],
#             "name": data["name"],
#             "manufacturer": data["manufacturer"],
#             "model": data["model"],
#             "serial": data["serial"],
#             "type": data["type"],
#             "slave_id": data["slave_id"]
#         }

#         parsed_fields = {}
#         for entry in data["DPS"]:
#             for key, value in entry.items():
#                 if key != "ts" and key != "reg_nr":
#                     parsed_fields[key] = value

#         result = {**base, **parsed_fields}
#         return result

#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing PN_4 data: {e}")
#         return None
