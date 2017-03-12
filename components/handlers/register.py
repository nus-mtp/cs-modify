'''
    This module handles account registration.
'''

import hashlib
import uuid
from app import RENDER, SESSION
import web
from components import model


## For login test
class Register(object):
    '''
        Class handles registration (put user in database)
    '''
    def GET(self):
        '''
            This function is called when /register is accessed.
        '''
        SESSION['id'] = 0
        return RENDER.register(SESSION['id'])


    def POST(self):
        '''
            This function is called when the register button is clicked.

            1) If username is taken, an alert will indicate that username
               is taken.
            2) If all validations pass, the account is inserted into the database.
        '''
        '''
            Blank inputs are blocked by front-end. For full extent of validation
            we also perform validation here should the front-end happen to be
            bypassed in some manner. 
        '''
        credentials = web.input()

        try:
            input_id = credentials.id
            input_password = credentials.password
        except(AttributeError):
            SESSION['id'] = 0
            raise web.seeother('/register')

        if credentials.id == '' or credentials.password == '':
            raise web.seeother('/register')

        # If user ID already exists, alert user that the ID is taken.
        if model.is_userid_taken(credentials.id):
            SESSION['id'] = web.ACCOUNT_CREATED_UNSUCCESSFUL
            raise web.seeother('/register')
        # Else, the new account is valid, and add it to the database.
        else:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(credentials.password
                                             + salt).hexdigest()
            model.add_admin(credentials.id, salt, hashed_password)
            SESSION['id'] = web.ACCOUNT_CREATED_SUCCESSFUL

            raise web.seeother('/login')