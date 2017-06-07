import Queue
import mysql.connector


class ConnectionPool(object):
    def __init__(self, connection_config, size=1):
        self.size = size
        self.connection_config = connection_config
        self.is_initialised = False
        self.initialise()

    def initialise(self):
        self.connections = Queue.Queue(self.size)
        for index in range(self.size):
            cnx = mysql.connector.connect(**self.connection_config)
            self.connections.put(cnx)

        self.is_initialised = True

    def get_connection(self):
        if not self.is_initialised:
            self.initialise()

        if self.is_initialised:
            conn = self.connections.get()

            return conn

    def release_connection(self, connection):
        self.connections.put(connection)
