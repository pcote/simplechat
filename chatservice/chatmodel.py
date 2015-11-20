
from flask.ext.sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import hashlib
import os

class ChatModel():
    """
    Handles application logic and persistence issues as concerned with user account setup or
    passing chat messages to/from the database.
    """


    def __init__(self, app):
        self.app = app
        import os
        config_file_name = "settings.ini"
        config_dir = __file__.rsplit(os.path.sep, maxsplit=1)[0]
        config_file_abs_path = "{}{}{}".format(config_dir, os.path.sep, config_file_name)
        
        parser = ConfigParser()
        parser.read(config_file_abs_path)
        db_user = parser["settings"]["db_user"]
        db_pw = parser["settings"]["db_password"]
        db_conn_str = "mysql+pymysql://{}:{}@localhost/simplechat".format(db_user, db_pw)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_conn_str
        self.db = SQLAlchemy(app)
        self.eng = self.db.get_engine(self.app)

        self.user_table = self.db.Table("users",
                          self.db.Column("username", self.db.VARCHAR(50), primary_key=True),
                          self.db.Column("password", self.db.BLOB))

        self.message_table = self.db.Table("messages",
                                           self.db.Column("id", self.db.Integer, autoincrement=True, primary_key=True),
                                           self.db.Column("username", self.db.VARCHAR(50), self.db.ForeignKey("users.username")),
                                           self.db.Column("message", self.db.VARCHAR(140)))

        self.db.create_all()


    def create_user(self, username, password):
        """
        Safely create a new username and encrypted password for a new user account.
        :param username: Name of the user in question.
        :param password: The password user will be using to log in. (note: does get encrypted when stored)
        :return: Nothing.
        """
        hasher = hashlib.md5()
        hasher.update(password.encode())
        hash_blob = hasher.digest()
        self.eng.execute(self.user_table.insert().values(username=username, password=hash_blob))


    def user_exists(self, username):
        """
        Check to see if the user already has an account in the system.
        :param username: Name of the user.
        :return: True if the user account exists in the database, false otherwise.
        """
        query = self.db.select([self.user_table]).where(self.user_table.c.username == username)
        rs = self.eng.execute(query).fetchall()
        if rs:
            return True
        else:
            return False


    def is_valid_user(self, username, password):
        """
        2 things: First, does the user exists and second, is the password legit.
        :param username: Name of the user in question.
        :param password: Password that's being submitted for this user.
        :return: True if the user AND   password are both valid, False otherwise.
        """

        # Validate that there is an actual user account there.
        query = self.db.select([self.user_table]).where(self.user_table.c.username == username)
        res = self.eng.execute(query)
        rec = res.first()
        valid_user = True if rec else False

        # Hash the password arg and check to see if the hash matches the hash stored in the user record.
        _, db_hash = rec
        hasher = hashlib.md5()
        hasher.update(password.encode())
        hashed_arg = hasher.digest()
        valid_password = True if db_hash == hashed_arg else False

        if valid_user and valid_password:
            return True
        return False


    def is_strong_password(self, pw):
        """
        Enforcer for password policy.  Passwords need to be 8 characters with letters, numbers, and characters present.
        :param pw: The password whose strength we are checking.
        :return: True if the password is sufficiently strong.  False otherwise.
        """
        import string
        MINIMUM_STRING_LENGTH = 8

        if len(pw) < MINIMUM_STRING_LENGTH:
            return False
        if not set(pw).intersection(set(string.ascii_letters)):
            return False
        if not set(pw).intersection(set(string.digits)):
            return False
        if not set(pw).intersection(set(string.punctuation)):
            return False

        return True


    def store_message(self, username, message):
        """
        Store the new chat message line in the data store.
        :param username: The name of the user with the chat message to be stored.
        :param message: The actual chat message.
        :return: Nothing.
        """
        insert = self.message_table.insert().values(username=username, message=message)
        self.eng.execute(insert)

    @property
    def Messages(self):
        """
        Simple list of all messages.  Intended to be stored in the running chat window.
        :return: Every chat message.
        """
        query = self.db.select([self.message_table]).order_by(self.message_table.c.id)
        messages = [dict(id=id, user=user, message=message) for id, user, message in self.eng.execute(query).fetchall()]

        return messages
