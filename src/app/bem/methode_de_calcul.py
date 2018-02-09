# -*- coding: utf-8 -*-
""" Data models"""
import datetime
from app.main import db



#--------------
# Methode de calcul Document
#--------------
class MethodeDeCalcul(db.Document):
    _id = db.StringField(required=True, primary_key=True)         
    #what ????