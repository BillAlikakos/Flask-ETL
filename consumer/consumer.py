from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from config import Config
from util.logger import Logger
from util.constants import Constants

class Consumer:
    
    def __init__(self):
        self.consumer = KafkaConsumer(
            Config.KAFKA_TOPIC_CLOTHES, Config.KAFKA_TOPIC_USERS,
            bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer = lambda x: json.loads(x.decode(Config.KAFKA_MSG_ENCODING)),
            group_id = Config.KAFKA_GROUP_ID,
            auto_offset_reset = Config.KAFKA_AUTO_OFFSET_RESET,
            session_timeout_ms = Config.KAFKA_SESSION_TIMEOUT_MS,
            max_poll_interval_ms = Config.KAFKA_MAX_POLL_INTERVAL_MS,
            heartbeat_interval_ms = Config.KAFKA_HEARTBEAT_INTERVAL_MS,
            enable_auto_commit = Config.KAFKA_ENABLE_AUTO_COMMIT,
            )
        
        self.logger = Logger.get_logger()

        if(self.consumer.bootstrap_connected is False):
            self.logger.warning(f'[{self.__class__.__name__}] Kafka bootstrap is not connected')
        
        self.logger.info(f'[{self.__class__.__name__}] Initialized')
        
        self.mongo_client = MongoClient(Config.MONGODB_URI)
        self.db = self.mongo_client[Config.MONGODB_DB]



    def get_topics(self):
        """Attempts to retrieve the topics from Kafka in order to determibe if it is up
        and running.
            Returns: the retrieved topics
        """
        self.consumer.poll()
        return self.consumer.topics()

    def insert_or_update_user(self, user_id, value, field):
        """Gets a cursor for the corresponding document depending on the field parameter
        and inserts or updates the data of the given field. If an entry already exists in 
        MongoDB, it will be updated with the corresponding field, should the incoming value
        not be present.
        ----------
        Arguments:\n
        user_id
            The id of the user to be added/updated.
        value
            The value of the field to be added/updated.
        field
            The field to be added/updated.
        """
        cursor = self.db.users.find({Constants.USER_ID: user_id})
        if(cursor is not None):
            values = ''                
            for key in cursor:
                current = None
                if(field in key):
                    current = key[field]
                    if(current is not None):
                        values = current
            
            if(values==''):
                values = value
            else:
                if(value not in values):
                    values+=','+str(value)
                else:
                    self.logger.info(f'[{self.__class__.__name__}] [{field}] [Value: {value} has already been added]')
                    return
                
            self.db.users.update_one(
                {Constants.USER_ID: user_id},
                {'$set':{
                        field: values
                    }},upsert=True)
    
    def consume(self):
        """Handles the messages that are published by the producers to the
        corresponding Kafka topics.
        """
        while True:
            for message in self.consumer:
                self.logger.info(f'[{self.__class__.__name__}] Received message: {message}')
                payload = message.value
                if message.topic == Config.KAFKA_TOPIC_CLOTHES:
                    self.db.clothes.update_one(
                        {Constants.CLOTHE_ID: payload[Constants.CLOTHE_ID]},
                        {'$set': payload},
                        upsert=True
                    )
                else:
                    userId = payload[Constants.USER_ID]
                    clothes = payload[Constants.OWNED_CLOTHE_IDS]
                    relationships = payload[Constants.RELATIONSHIPS]
                    
                    friends = []
                    colleagues = []
                    
                    for r in relationships:
                        if r[Constants.RELATIONSHIP_TYPE_PARAM] == Constants.RELATIONSHIP_FRIEND:
                            friends.append(r[Constants.TARGET_USER_ID])
                        elif r[Constants.RELATIONSHIP_TYPE_PARAM] == Constants.RELATIONSHIP_COLLEAGUE:
                            colleagues.append(r[Constants.TARGET_USER_ID])

                    self.logger.info(f'[{self.__class__.__name__}] [userId: {userId}] [Owned clothes: {clothes}] [Friends: {friends}] [Colleagues: {colleagues}]')

                    for i in clothes:
                        self.insert_or_update_user(userId, i, Constants.ENTITY_CLOTHES)

                    for i in friends:
                        self.insert_or_update_user(userId, i, Constants.ENTITY_FRIENDS)
                    
                    for i in colleagues:
                        self.insert_or_update_user(userId, i, Constants.ENTITY_COLLEAGUES)
