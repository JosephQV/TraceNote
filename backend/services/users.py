from ..db.session import users_collection


def add_user(user_dict):
    users_collection.insert_one(user_dict)


def get_user(username):
    users_collection.find_one({'username': username})


