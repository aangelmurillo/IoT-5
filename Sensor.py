from Helmet import Helmet
from InfoSensor import InfoSensor
from File import File
from Convert import Convert

class Sensor(File, Convert):
    def __init__(self, casco_id: int = None, sensors: list = None):
        self.casco_id = casco_id
        self.sensors = sensors or []

    def __str__(self):
        return f"Casco ID: {self.casco_id}" if self.casco_id else "Sensor Container"

    def add_sensor(self, nombre, tipo, valor, unidad, fecha):
        info_sensor = {
            "nombre": nombre,
            "tipo": tipo,
            "info_sensor": {
                "valor": valor,
                "unidad": unidad,
                "fecha": fecha
            }
        }
        self.sensors.append(info_sensor)

    def to_dict(self):
        return {
            "casco_id": self.casco_id,
            "sensor": self.sensors
        }
