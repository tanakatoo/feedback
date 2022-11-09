from flask import session
class Helpers():

    def write_to_session(variable,value):
        session[variable]=value
        return True
        