# def parse(data: dict, save_sensor_data):
#     try:
#         cleaned_data = {
#             "cold_side": int(data["OstasSkati_cold_side"]),
#             "current_flow": int(data["OstasSkati_current_flow"]),
#             "current_power": int(data["OstasSkati_current_power"]),
#             "energy": int(data["OstasSkati_energy"]),
#             "hot_side": int(data["OstasSkati_hot_side"]),
#             "temp_diff": int(data["OstasSkati_temp_diff"]),
#             "dev_eui": data["devEUI"],
#             "pt100_1": float(data["pt100_1"]),
#             "pt100_2": float(data["pt100_2"]),
#             "timestamp": data["time"],
#         }
#         return cleaned_data
#     except (KeyError, ValueError, TypeError) as e:
#         print(f"Error parsing UC300 data: {e}")
#         return None
