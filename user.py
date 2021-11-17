from mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Email:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL('emailchecker').query_db(query)
        emails = []
        for email in results:
            emails.append( cls(email) )
        return emails
    

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO emails ( email , created_at, updated_at ) VALUES ( %(email)s , NOW() , NOW() );"

        return connectToMySQL('emailchecker').query_db( query, data )