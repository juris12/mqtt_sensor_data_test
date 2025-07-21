import psycopg2
from datetime import datetime

def save_sensor_data(mqtt_username, building_name, sensor_name, timestamp, field_name, value):
    conn = psycopg2.connect(
        dbname="mqtt_test_db",
        user="mqtt_user",
        password="janis",
        host="localhost"
    )
    try:
        cur = conn.cursor()

        # 1. Check user exists with mqtt_username
        cur.execute("""
            SELECT user_id FROM accounts_userprofile WHERE mqtt_username = %s
        """, (mqtt_username,))
        user_row = cur.fetchone()
        if not user_row:
            print("User not found")
            return False
        user_id = user_row[0]

        # 2. Check building exists and belongs to that user
        cur.execute("""
            SELECT id FROM sensor_data_building 
            WHERE name = %s AND user_id = %s
        """, (building_name, user_id))
        building_row = cur.fetchone()
        if not building_row:
            print("Building not found or not assigned to user")
            return False
        building_id = building_row[0]
        # 3. Check sensor with sensor_name exists and belongs to that building (via IndividualSensor)
        cur.execute("""
            SELECT sensor_data_individualsensor.id, sensor_data_sensor.sensor_category_id FROM sensor_data_individualsensor
            JOIN sensor_data_sensor ON sensor_data_individualsensor.sensor_id = sensor_data_sensor.id
            WHERE sensor_data_sensor.name = %s AND sensor_data_individualsensor.building_id = %s
        """, (sensor_name, building_id))
        sensor_row = cur.fetchone()
        if not sensor_row:
            print("Sensor not found in building")
            return False
        individual_sensor_id, sensor_category_id = sensor_row

        # 4. Check DataField exists for this sensor_category and matches field_name
        cur.execute("""
            SELECT id, field_type FROM sensor_data_datafield
            WHERE sensor_category_id = %s AND name = %s
        """, (sensor_category_id, field_name))
        field_row = cur.fetchone()
        if not field_row:
            print("DataField not found for sensor category")
            return False
        datafield_id, field_type = field_row

        # 4. Check if SensorReading already exists for this sensor and timestamp
        cur.execute("""
            SELECT id FROM sensor_data_sensorreading
            WHERE individual_sensor_id = %s AND timestamp = %s
        """, (individual_sensor_id, timestamp))
        reading_row = cur.fetchone()

        if reading_row:
            reading_id = reading_row[0]
        else:
            cur.execute("""
                INSERT INTO sensor_data_sensorreading (individual_sensor_id, timestamp)
                VALUES (%s, %s) RETURNING id
            """, (individual_sensor_id, timestamp))
            reading_id = cur.fetchone()[0]

        # Prepare value fields according to field_type
        float_value = int_value = str_value = bool_value = None
        if field_type == 'FLOAT':
            float_value = float(value)
        elif field_type == 'INT':
            int_value = int(value)
        elif field_type == 'STR':
            str_value = str(value)
        elif field_type == 'BOOL':
            bool_value = bool(value)
        else:
            print("Unknown field type")
            return False
        
        cur.execute("""
            INSERT INTO sensor_data_measurement 
            (reading_id, field_id, float_value, int_value, str_value, bool_value)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (reading_id, datafield_id, float_value, int_value, str_value, bool_value))

        conn.commit()
        print("Saved sensor data successfully")
        return True

    except Exception as e:
        print(f"Error saving sensor data: {e}")
        conn.rollback()
        return False

    finally:
        cur.close()
        conn.close()
