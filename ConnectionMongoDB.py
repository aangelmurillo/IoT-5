from pymongo import MongoClient, errors
from pymongo.errors import ConnectionFailure, OperationFailure
import subprocess

class ConnectionMongoDB:
    def __init__(self, connection, bd, collection, socket_timeout_ms=5000, connect_timeout_ms=5000):
        self.connection = connection
        self.bd = bd
        self.collection = collection
        self.socket_timeout_ms = socket_timeout_ms
        self.connect_timeout_ms = connect_timeout_ms
        self.client = None
        self.db = None

    def connect(self):
        if self.client is None:
            self.client = MongoClient(
                self.connection,
                socketTimeoutMS=self.socket_timeout_ms,
                connectTimeoutMS=self.connect_timeout_ms
            )
            self.db = self.client[self.bd]

    def insert(self, data):
        self.connect()
        self.db[self.collection].insert_one(data)

    def insert_many(self, data):
        self.connect()
        self.db[self.collection].insert_many(data)

    def search(self, filter):
        self.connect()
        return self.db[self.collection].find(filter)

    def update(self, filter, data):
        self.connect()
        self.db[self.collection].update_one(filter, {"$set": data})

    def delete(self, filter):
        self.connect()
        self.db[self.collection].delete_one(filter)

    def close_connection(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def check_wifi_and_connection(self):
        try:
            self.connect()
            self.client.admin.command('ping')
            return True
        except errors.ConnectionFailure as e:
            print(f"Error 1: {e}")
            return False
        except errors.OperationFailure as e:
            print(f"Error 2: {e}")
            return False
        except errors.ConfigurationError as e:
            print(f"Error 3: {e}")
            return False
        except Exception as e:
            print(f"Error 4: {e}")
            return False