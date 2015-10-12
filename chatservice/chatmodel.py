
from flask.ext.sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import hashlib
import os

class ChatModel():
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
        hasher = hashlib.md5()
        hasher.update(password.encode())
        hash_blob = hasher.digest()
        self.eng.execute(self.user_table.insert().values(username=username, password=hash_blob))


    def user_exists(self, username):
        query = self.db.select([self.user_table]).where(self.user_table.c.username == username)
        rs = self.eng.execute(query).fetchall()
        if rs:
            return True
        else:
            return False


    def is_valid_user(self, username, password):

        query = self.db.select([self.user_table]).where(self.user_table.c.username == username)
        res = self.eng.execute(query)
        rec = res.first()
        valid_user = True if rec else False

        _, db_hash = rec
        hasher = hashlib.md5()
        hasher.update(password.encode())
        hashed_arg = hasher.digest()
        valid_password = True if db_hash == hashed_arg else False

        if valid_user and valid_password:
            return True
        return False

    def is_strong_password(self, pw):
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
        insert = self.message_table.insert().values(username=username, message=message)
        self.eng.execute(insert)

    @property
    def Messages(self):
        query = self.db.select([self.message_table]).order_by(self.message_table.c.id)
        messages = [dict(id=id, user=user, message=message) for id, user, message in self.eng.execute(query).fetchall()]

        return messages
