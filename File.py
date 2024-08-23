import json

class File:
    def __init__(self):
        pass

    def save_json(self, obj, nombre_archivo):
        try:
            existing_data = self.read_json(nombre_archivo)
        except FileNotFoundError:
            existing_data = []

        if isinstance(existing_data, dict):
            existing_data = [existing_data]
        
        existing_data.append(obj)

        with open(nombre_archivo, "w") as archivo:
            json.dump(existing_data, archivo, indent=4)

    def read_json(self, file_name):
        try:
            with open(file_name) as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return [data]
        except FileNotFoundError:
            return []

    def borrar_contenido_json(self, file_name):
        with open(file_name, "w") as archivo:
            json.dump([], archivo, indent=4)
