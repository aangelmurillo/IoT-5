import time
import json
from ConnectionArduino import ConnectionArduino
from ConnectionMongoDB import ConnectionMongoDB
from File import File

def parse_data(data):
    try:
        data_dict = {}
        for item in data.split(','):
            if ':' in item:
                key, value = item.split(':')
                value = value.strip()
                try:
                    data_dict[key.strip()] = float(value)
                except ValueError:
                    data_dict[key.strip()] = value  
        return data_dict
    except ValueError as e:
        print(f"Error parsing data: {e}")
        return None

def create_sensor_entry(name, sensor_type, value, unit):
    return {
        "nombre": name,
        "tipo": sensor_type,
        "info_sensor": {
            "valor": value,
            "unidad": unit,
        }
    }

def main():
    port = "/dev/ttyUSB1"
    uri = "url-aqui"
    db = "octavio-binary"
    collection = "sensor"
    collection_sec = "sensorAZ163"
    id = None
    connection_arduino = ConnectionArduino(port)
    connection_mongodb = ConnectionMongoDB(uri, db, collection)
    connection_mongodb2 = ConnectionMongoDB(uri, db, collection_sec)
    json_file = File()
    send = True

    try:
        while True:            
            raw_data = connection_arduino.read()
            
            data_dict = parse_data(raw_data)
            if data_dict:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                sensor_entries = []
                if "temperature_C" in data_dict:
                    sensor_entries.append(create_sensor_entry("bme-260", "temperatura", data_dict["temperature_C"], "°C"))
                if "pressure_hPa" in data_dict:
                    sensor_entries.append(create_sensor_entry("bme-260", "presion", data_dict["pressure_hPa"], "hPa"))
                if "altitude_m" in data_dict:
                    sensor_entries.append(create_sensor_entry("bme-260", "altitud", data_dict["altitude_m"], "m"))
                if "humidity_percent" in data_dict:
                    sensor_entries.append(create_sensor_entry("bme-260", "humedad", data_dict["humidity_percent"], "%"))
                if "hscr_04" in data_dict:
                    sensor_entries.append(create_sensor_entry("hscr_04", "hscr_04", data_dict["hscr_04"], None))
                if "latitude" in data_dict:
                    sensor_entries.append(create_sensor_entry("gps-latitud", "gps-latitud", data_dict["latitude"], "latitude"))
                if "longitude" in data_dict:
                    sensor_entries.append(create_sensor_entry("gps-longitud", "gps-longitud", data_dict["longitude"], "longitude"))
                if "mq2_value" in data_dict:
                    sensor_entries.append(create_sensor_entry("mq2", "mq2", data_dict["mq2_value"], None))
                if "mq135_value" in data_dict:
                    sensor_entries.append(create_sensor_entry("mq135", "mq135", data_dict["mq135_value"], None))
                if "fc28_value" in data_dict:
                    sensor_entries.append(create_sensor_entry("fc28", "fc28", data_dict["fc28_value"], None))
                if "casco_id" in data_dict:
                    casco_id = data_dict["casco_id"]

                id = casco_id

                document = {
                    "helmet_id": casco_id,
                    "sensors": sensor_entries,
                    "timestamp": timestamp
                }
                
                print(document)

                if connection_mongodb.check_wifi_and_connection():
                    connection_mongodb.insert(document)
                    connection_mongodb2.insert(document)
                else:
                    json_file.save_json(document, "casco_" + str(id) + ".json")
                    send = True

                if send and connection_mongodb.check_wifi_and_connection():
                    json_files = json_file.read_json("casco_" + str(id) + ".json")
                    for file in json_files:
                        connection_mongodb.insert(file)
                        connection_mongodb2.insert(file)
                    json_file.borrar_contenido_json("casco_" + str(id) + ".json")
                    send = False

            time.sleep(1)
    except KeyboardInterrupt:
        connection_arduino.close()
        print("Connection closed 1")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        connection_arduino.close()
        print("Connection closed 2")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection_arduino.close()
        print("Connection closed 4")

if __name__ == '__main__':
    main()
