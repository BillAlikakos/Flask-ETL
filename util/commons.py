from util.logger import Logger
from util.constants import Constants

class Commons:
    
    @staticmethod
    def extract_clothe_data(clothes):
        """Extracts the clothe ID of each clothe present in the input JSON object.\n
        Arguments:\n
        clothes
            The JSON document containing the data of the clothes.
        Returns: a list containing the extracted clothe IDs.
        """
        ret_val = []
        for clothe in clothes:
            currentClothe = clothe[Constants.CLOTHE_ID]
            ret_val.append(currentClothe)
        return ret_val

    @staticmethod
    def extract_clothe_data_from_entity(json_obj):
        """Extracts the owned clothes of a user's friend/colleague JSON object.\n
        Arguments:\n
        json_obj
            The JSON object of the given user.
        Returns: a list containing the IDs of the clothes owned by the given entity.
        """
        ret_val = []
        for user in json_obj:
            clothes = json_obj[user]
            ret_val += Commons.extract_clothe_data(clothes)
        return ret_val

    @staticmethod
    def extract_recommended_clothe(owned_clothes_ids, clothes_to_compare):
        """Checks if the reccomended clothe is already owned by the given user.\n
        Arguments:\n
        owned_clothes_ids
            The IDs of the user's owned clothes.
        clothes_to_compare
            A list of clothes to compare with the owned clothes.
        Returns: The ID of the recommended clothe. If the clothe is already owned by the user
        an empty string will be returned.
        """
        for clothe_to_compare in clothes_to_compare:
            if clothe_to_compare in owned_clothes_ids:
                Logger.get_logger().warn(f'[{__name__}.extract_recommended_clothe] Recommended clothe {clothe_to_compare} is already owned by user')
            else:
                return clothe_to_compare
        return ''
