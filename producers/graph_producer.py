from neo4j import GraphDatabase
import json
import time
from kafka import KafkaProducer
from config import Config
from util.commons import Commons
from util.logger import Logger
from config import Config

class GraphProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode(Config.KAFKA_MSG_ENCODING),
            acks = Config.KAFKA_PRODUCER_ACKS, retries = Config.KAFKA_PRODUCER_RETRIES, 
            retry_backoff_ms = Config.KAFKA_PRODUCER_RETRY_BACKOFF_MS, request_timeout_ms = Config.KAFKA_PRODUCER_REQUEST_TIMEOUT_MS,)
        
        self.logger = Logger.get_logger() 
        self.logger.info(f'[{self.__class__.__name__}] initialized')
        
        if(self.producer.bootstrap_connected is False):
            self.logger.warning(f'[{self.__class__.__name__}] Kafka bootstrap is not connected')

        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
    
    def get_user_data(self, tx):
        """Retrieves the clothes owned by each user as well as each user's relationships.
        """
        query = """
        MATCH (u:User)
                OPTIONAL MATCH (u)-[r]->(other:User)
                RETURN u.userId AS userId, u.clotheIDs AS clothes,
                       collect({
                           type: type(r),
                           targetUserId: other.userId
                       }) AS relationships"""
        return tx.run(query).data()

    def produce(self):
        """Retrieves the data from Neo4J DB and publishes them in batches to the users Kafka topic on a set interval.
        The batch size and the interval are defined by the NEO4J_BATCH_SIZE & NEO4J_BATCH_SLEEP_SECONDS config properties.
        """
        if(self.producer.bootstrap_connected()):
            with self.driver.session() as session:
                user_data = session.read_transaction(self.get_user_data)
                self.logger.info(f'[{self.__class__.__name__}] User data: {user_data}')
                
                returned_data = []
                for entry in user_data:
                    relationships = []
                    for r in entry['relationships']:
                        if r['targetUserId'] is not None:
                            relationships.append(r)
                    
                    user_data = {
                        "userId": entry["userId"],
                        "clothes": entry["clothes"],
                        "relationships": relationships
                    }
                    returned_data.append(user_data)

            count = 0
            for entity in returned_data:
                self.logger.info(f'[{self.__class__.__name__}] Sending {entity}')
                self.producer.send(Config.KAFKA_TOPIC_USERS, entity)
                count = count+1
                if(count >= Config.NEO4J_BATCH_SIZE):
                    time.sleep(Config.NEO4J_BATCH_SLEEP_SECONDS)
                    count = 0
