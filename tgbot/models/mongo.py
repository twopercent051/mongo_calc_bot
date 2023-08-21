from typing import Optional, Literal

from pymongo.mongo_client import MongoClient

from create_bot import config


class MongoDB:

    def __init__(self):
        # uri = config.mongo.uri
        uri = "mongodb://83.222.10.29:27017"
        client = MongoClient(uri)
        self.table = client.tgbot_db


class UsersDB(MongoDB):

    def __init__(self):
        super().__init__()
        self.__collection = self.table.users

    def create_user(self, **data):
        self.__collection.insert_one(data)

    def get_user(self, user_id: int) -> Optional[dict]:
        return self.__collection.find_one(filter={"tid": user_id})

    def update_user(self, user_id: int, update_object):
        self.__collection.update_one({"tid": user_id}, {"$set": update_object})

    def get_list_object(self,
                        user_id: int,
                        list_object: Literal["last_ticket", "currencies", "custom_currencies"]) -> list:
        user = self.__collection.find_one(filter={"tid": user_id})
        return user[list_object] if user.keys().__contains__(list_object) else []

    def get_saved_tickets(self, user_id: int) -> list:
        user = self.__collection.find_one(filter={"tid": user_id})
        if user.keys().__contains__("saved_tickets"):
            return sorted(user["saved_tickets"], key=lambda x: x["timestamp"], reverse=True)
        else:
            return []

    def get_saved_ticket_by_timestamp(self, user_id: int, timestamp: float):
        saved_tickets = self.get_saved_tickets(user_id=user_id)
        return list(filter(lambda x: x["timestamp"] == timestamp, saved_tickets))[0]

    def get_saved_tickets_after_delete(self, user_id: int, timestamp: float):
        saved_tickets = self.get_saved_tickets(user_id=user_id)
        return list(filter(lambda x: x["timestamp"] != timestamp, saved_tickets))


class RatesDB(MongoDB):
    def __init__(self):
        super().__init__()
        self.__collection = self.table.rates

    def create_rates(self, **data):
        self.__collection.insert_one(data)

    def get_rates(self):
        return self.__collection.find_one()

    def drop_collection(self):
        self.__collection.drop()
