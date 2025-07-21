# def parse(data: dict, save_sensor_data):
#     try:
#         parsed_data = {
#             "lib_version": data["Lib_version"],
#             "name": data["name"],
#             "manufacturer": data["manufacturer"],
#             "model": data["model"],
#             "type": data["type"],
#             "slave_id": int(data["slave_id"]),
#         }

#         # Flatten DPS dynamic fields
#         parsed_fields = {}
#         for item in data["DPS"]:
#             # Each dict in DPS contains 1 or more keys besides reg_nr and ts
#             for key, value in item.items():
#                 if key not in ("reg_nr", "ts"):
#                     parsed_fields[key] = value
        
#         cleaned_data = {
#             **parsed_data,
#             **parsed_fields  # dynamically added measurements
#         }

#         return cleaned_data

#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing SK1-P14 data: {e}")
#         return None
