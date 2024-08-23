import serial

class ConnectionArduino:
    def __init__(self, puerto):
        self.puerto = puerto
        self.conexion = serial.Serial(self.puerto, 9600)

    def read(self):
        return self.conexion.readline().decode('utf-8').strip()

    def write(self, mensaje):
        self.conexion.write(mensaje.encode('utf-8'))

    def close(self):
        self.conexion.close()

    