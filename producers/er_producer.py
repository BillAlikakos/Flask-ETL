import mysql.connector
import json
import time
from kafka import KafkaProducer
from config import Config
from util.logger import Logger

class ERProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer = lambda x: json.dumps(x).encode(Config.KAFKA_MSG_ENCODING),
            acks= Config.KAFKA_PRODUCER_ACKS, retries = Config.KAFKA_PRODUCER_RETRIES, 
            retry_backoff_ms = Config.KAFKA_PRODUCER_RETRY_BACKOFF_MS, request_timeout_ms = Config.KAFKA_PRODUCER_REQUEST_TIMEOUT_MS,)
        
        self.mysql_conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB)
        
        self.cursor = self.mysql_conn.cursor(dictionary=True)
        self.logger = Logger.get_logger() 
        if(self.producer.bootstrap_connected is False):
            self.logger.warning(f'[{self.__class__.__name__}] Kafka bootstrap is not connected')

    def on_success(self, record_metadata):
        self.logger.debug(record_metadata.topic)

    def on_error(self, excp):
        self.logger.error(f"[{self.__class__.__name__}] An error occurred while sending message to {Config.KAFKA_TOPIC_CLOTHES}", exc_info=excp)
            
    def produce(self):
        """Retrieves the data from MySQL DB and publishes the rows in batches to the clothes Kafka topic on a set interval.
        The batch size and the interval are defined by the MYSQL_BATCH_SIZE & MYSQL_BATCH_SLEEP_SECONDS config properties.
        """
        while True:
            self.cursor.execute("SELECT * FROM clothes")
            clothes = self.cursor.fetchall()
            self.logger.info(f'[{self.__class__.__name__}] Retrieved clothes from MySQL: {clothes} Cursor length: {self.cursor.rowcount}')
            rowsSent = 0

            if(self.cursor.rowcount>0 and self.producer.bootstrap_connected()):
                for cloth in clothes:
                    self.logger.info(f'[{self.__class__.__name__}] Sending {cloth} to {Config.KAFKA_TOPIC_CLOTHES}')
                    self.producer.send(Config.KAFKA_TOPIC_CLOTHES, cloth).add_callback(self.on_success).add_errback(self.on_error)
                    rowsSent+=1
                    if(rowsSent == Config.MYSQL_BATCH_SIZE):
                        self.logger.info(f'[{self.__class__.__name__}] Sent {rowsSent} rows, will wait for {Config.MYSQL_BATCH_SLEEP_SECONDS}s')
                        time.sleep(Config.MYSQL_BATCH_SLEEP_SECONDS)
                        rowsSent = 0
                        
            self.logger.info(f'[{self.__class__.__name__}] All MySQL rows processed')
            break
                