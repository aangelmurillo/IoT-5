class InfoSensor:
    def __init__(self, value: any, unit: any, timestamp: any):
        self.value = value
        self.unit = unit
        self.timestamp = timestamp
    
    def __str__(self):
        return f"{self.value} {self.unit} ({self.timestamp})"