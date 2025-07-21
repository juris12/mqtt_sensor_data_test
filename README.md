# IoT sensor data storage and processing with postgreSQL and MQTT.


## Dashbord site map

#### See all buildings from all customers

```http
  GET /buildings/
```
<img width="1847" height="390" alt="image" src="https://github.com/user-attachments/assets/3ff17d2b-1008-4fe1-bd96-91de812aea2a" />


#### See all sensors in building x

```http
  GET /buildings/sensor_data_list/4
```

<img width="1848" height="313" alt="image" src="https://github.com/user-attachments/assets/a5eb0896-919c-43d1-9e38-d75b7e884a88" />

#### See all latest sensors x parameters values 

```http
  GET /buildings/sensor/detail/9/
```

<img width="1846" height="511" alt="image" src="https://github.com/user-attachments/assets/473d1343-67e9-440f-a218-4d68f875aa1e" />

#### See all  sensors x parameters y values 

```http
  GET /buildings/sensor/9/field/5/
```
<img width="1853" height="696" alt="image" src="https://github.com/user-attachments/assets/d53d9877-ca2e-4a30-ae35-bddda07bd8bb" />

To create and edit info django admin panel is used.

### DB shema
<img width="1003" height="1065" alt="Untitled (1)" src="https://github.com/user-attachments/assets/1bc5af7f-a350-45f0-84cc-1e45983008da" />

# db notes
When user is created server automaticly asign mqtt client and pwd.
Admin can create Sensor categorys with diferent prameters. For example CO2 sensor with prameter co2_level.
Then sensor model can be asign to that category. That allows multiple sensors to all have the same category, to be the same type of sensor.
Individual sensor is sensor instace that is located in some building.


### MQTT broker/server

I have created mock data publisher that publishes random data.
It is published by multilpe clients to client spesific topic. For example user1/building_1/sensors/temperature
Clients are conected to the MQTT broker with username and password.

Then there is subsriber script that subscribes to all topic.
Onece it gets message from broker based on sensor name it selects apropriate parser script and after cleaning data it saves it to db.


