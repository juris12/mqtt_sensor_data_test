# def parse(data: dict, save_sensor_data):
#     try:
#         record = data["data"][0]
#         fields = record["f"]
#         columns = data["header"]["columns"]

#         # Dynamically build the result dictionary from the columns
#         parsed_fields = {}
#         for key, column in columns.items():
#             column_name = column["name"]
#             value = fields[key]["v"]
#             parsed_fields[column_name] = float(value) if isinstance(value, float) else int(value)

#         # Add metadata and timestamps
#         cleaned_data = {
#             "sn": data["SN"],
#             "name": data["name"],
#             "timestamp": record["ts"],
#             "start_time": data["header"]["startTime"],
#             "end_time": data["header"]["endTime"],
#             "record_count": int(data["header"]["recordCount"]),
#             **parsed_fields,  # dynamically added measurements
#         }

#         return cleaned_data
#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing EL uzskaite 3 data: {e}")
#         return None
