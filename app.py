from flask import Flask, jsonify, make_response
from http import HTTPStatus
from flask import request
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
from producers.er_producer import ERProducer
from producers.graph_producer import GraphProducer
from consumer.consumer import Consumer
import threading
from util.commons import Commons
from util.logger import Logger
from util.constants import Constants
import time
from kafka.errors import NoBrokersAvailable

logger = Logger.get_logger()

er_producer = None
graph_producer = None
consumer = None
db = None
threads = []

def start_background_thread(name, thread):
        logger.info(f'Starting {name}')
        thread.start()
        threads.append(thread)

def initialize_application():
    global er_producer, graph_producer, consumer, threads, db
    
    try:
        mongo_client = MongoClient(Config.MONGODB_URI)
        db = mongo_client[Config.MONGODB_DB]
    except ConnectionFailure:
        logger.error('Error while connecting to MongoDB')
        raise
        
    try:
        er_producer = ERProducer()
        graph_producer = GraphProducer()
        consumer = Consumer()
        
        start_background_thread('Kafka consumer', threading.Thread(target=consumer.consume, daemon=True))
        
        topics = consumer.get_topics()
        attempts = 0
        
        while not topics and attempts < Config.KAFKA_CONNECT_ATTEMPTS:
            logger.warning(f'Kafka is not ready yet, will wait {Config.KAFKA_RECONNECT_INTERVAL_S} seconds.')
            time.sleep(Config.KAFKA_RECONNECT_INTERVAL_S)
            topics = consumer.get_topics()
            attempts += 1
            
        if not topics:
            logger.error(f"Couldn't connect to Kafka after {Config.KAFKA_CONNECT_ATTEMPTS} attempts")
            raise NoBrokersAvailable(f"Failed to get topics after {Config.KAFKA_CONNECT_ATTEMPTS} attempts")
            
        logger.info(f'Kafka topics: {topics}')
        
        start_background_thread('er_producer', threading.Thread(target=er_producer.produce, daemon=True))
        start_background_thread('graph_producer', threading.Thread(target=graph_producer.produce, daemon=True))
        
    except NoBrokersAvailable as e:
        logger.error(f"Kafka broker error: {e}")
        raise

def post_worker_init(worker):
    with app.app_context():
        logger.info("Initializing application in Gunicorn worker")
        initialize_application()

app = Flask(__name__)

if __name__ == "__main__":
    with app.app_context():
        initialize_application()
    app.run(host='0.0.0.0', port=5000)

@app.route('/users', methods=[Constants.HTTP_METHOD_GET])
def get_users():
    """
    Returns: a list containing each user's ID, owned clothe IDs. along with the userIds
    of the user's friends and colleagues.
    """
    users = list(db.users.find({}, {Constants.MONGO_DB_ID: 0}))
    return jsonify(users) if users else ('No users found in mongoDB', 404)

@app.route('/clothes', methods=[Constants.HTTP_METHOD_GET])
def get_clothes():
    """
    Returns: a list containing the data associated with each clothe ID (brand, color, price & style).
    """
    clothes = list(db.clothes.find({}, {Constants.MONGO_DB_ID: 0}))
    return jsonify(clothes) if clothes else ('No clothes found in mongoDB', 404)

def retrieve_clothe_attrs(clothes):
    """Retrieves the data of the given clothe IDs.\n
    Arguments:\n
    clothes
        A list containing the IDs of the clothes to be retrieved.
    Returns: a list containing the data of the clothes that were given as input.
    """
    clothe_atts = []
    for clothe in clothes:
        clothe_atts.append(db.clothes.find_one({Constants.CLOTHE_ID: clothe}, {Constants.MONGO_DB_ID: 0}))
    return clothe_atts

def retrieve_entity_clothes(user, type):
    """Retrieves the data of the given clothe IDs.\n
    Arguments:\n
    user
        An object with the data of the given user.
    type
        The type of the entity that the information will be retrieved for (friend/colleague).
    Returns: a dictionary containing the clothes owned by the given entity.
    """
    entity_clothes = {}
    
    if(user[type] is not None):
        entity_list = user[type].split(',')
        entity_ids = []
        entity_clothe_ids = []

        for entity_id in entity_list:
            entity_ids.append(db.users.find_one({Constants.USER_ID: entity_id}, {Constants.MONGO_DB_ID: 0}))

        for entity_obj in entity_ids:
            if(entity_obj is not None):
                entity_clothe_ids = entity_obj[Constants.ENTITY_CLOTHES].split(',')
                entity_clothes.update({entity_obj[Constants.USER_ID]:retrieve_clothe_attrs(entity_clothe_ids)})
    
    return entity_clothes

@app.route('/user/<user_id>', methods=[Constants.HTTP_METHOD_GET])
def get_user(user_id):
    """Retrieves the data of the given user.\n
    Arguments:\n
    user_id
        The id of the user to retrieve.
    Returns: An object containing the data of the user with the given id (user_data, owned_clothes, friend_clothes, colleague_clothes).
    """
    user = db.users.find_one({Constants.USER_ID: user_id}, {Constants.MONGO_DB_ID: 0})

    response_data = None
    if(user is not None):
        if(Constants.ENTITY_CLOTHES in user):
            clothes = user[Constants.ENTITY_CLOTHES].split(',')
            user_attrs = retrieve_clothe_attrs(clothes)

            friend_clothes = {}
            colleague_clothes = {}

            if(Constants.ENTITY_FRIENDS in user):
                friend_clothes = retrieve_entity_clothes(user, Constants.ENTITY_FRIENDS)
            if(Constants.ENTITY_COLLEAGUES in user):
                colleague_clothes = retrieve_entity_clothes(user, Constants.ENTITY_COLLEAGUES)

            response_data = {Constants.RESPONSE_PARAM_USER_DATA:user, Constants.RESPONSE_PARAM_USER_CLOTHES:user_attrs, Constants.RESPONSE_PARAM_FRIEND_CLOTHES:friend_clothes, 
                             Constants.RESPONSE_PARAM_COLLEAGUE_CLOTHES:colleague_clothes}

    return jsonify(response_data) if response_data else (make_response(jsonify({Constants.RESPONSE_PARAM_ERROR:'Requested user was not found'}), HTTPStatus.NOT_FOUND))

@app.route('/user/<user_id>/recommend', methods=[Constants.HTTP_METHOD_GET])
def recommend_to_user(user_id):
    """Recommends a new clothe for the given user based on the clothes owned by the user's friends and colleagues.\n
    If the recommended clothe is already owned by the given user, the most popular clothe owned by all users
    will be recommended.\n
    Arguments:\n
    user_id
        The id of the user to recommend a new clothe.
    Returns: The id of the recommended clothe.
    """
    response_data = get_user(user_id)
    recommendation = ''

    if response_data._status_code == 200:
        owned_clothes = response_data.get_json()[Constants.RESPONSE_PARAM_USER_CLOTHES]
        owned_clothes_ids = Commons.extract_clothe_data(owned_clothes)
        
        friend_clothes = response_data.get_json()[Constants.RESPONSE_PARAM_FRIEND_CLOTHES]    
        friend_clothes = Commons.extract_clothe_data_from_entity(friend_clothes)
        recommendation = Commons.extract_recommended_clothe(owned_clothes_ids, friend_clothes)

        logger.info(f'[{request.path}] Recommendation for user {user_id} based on clothes that are owned by the user\'s friends: {recommendation}')
        if(recommendation==''):
            logger.info(f'[{request.path}] No recommendations based on user\'s friends found , checking for recommendations based on clothes that are owned by the user\'s colleagues')
            
            colleague_clothes = response_data.get_json()[Constants.RESPONSE_PARAM_COLLEAGUE_CLOTHES]
            colleague_clothes = Commons.extract_clothe_data_from_entity(colleague_clothes)
            recommendation = Commons.extract_recommended_clothe(owned_clothes_ids, colleague_clothes)
            if(recommendation!=""):
                logger.info(f'[{request.path}] Recommendation for user {user_id} based on clothes that are owned by the user\'s colleagues: {recommendation}')

        if(recommendation==''):
            logger.info(f'[{request.path}] No recommendations based on user\'s colleagues found, checking for the most popular product...')
            query = [
                {
                    "$project": {
                        "clothes": { "$split": ["$clothes", ","] }
                    }
                },
                {
                    "$unwind": "$clothes"
                },
                {
                    "$group": {
                        "_id": "$clothes",
                        "count": { "$sum": 1 }
                    }
                },
                {
                    "$sort": { "count": -1 }
                },
                {
                    "$limit": 1
                }
            ]
            
            result = db.users.aggregate(query)
            
            if(result is not None):
                for document in result:
                    most_popular_count = document['count']
                    recommendation = document[Constants.MONGO_DB_ID]
                    logger.info(f'[{request.path}] Found most popular clothe: {recommendation} with {most_popular_count} instances')

                    if recommendation in owned_clothes_ids:
                        logger.warning(f'[{request.path}] Recommended clothe {recommendation} is already owned by user {user_id}')
                        response_data = {Constants.RESPONSE_PARAM_ERROR:"No recommendation can be made for current user. Most popular clothe is already owned."}
                        return (make_response(response_data, HTTPStatus.NOT_FOUND))
            else:
                logger.warning(f'[{request.path}] No recommendations found for user {user_id}')
                response_data = {Constants.RESPONSE_PARAM_ERROR:"No result was returned while searching for the most popular clothe"}
                return (make_response(response_data, HTTPStatus.NOT_FOUND))
    else:
        return (make_response(response_data, HTTPStatus.NOT_FOUND))
    
    response_data = {Constants.RESPONSE_PARAM_RECOMMENDED_CLOTHE:recommendation}
    
    return jsonify(response_data)
