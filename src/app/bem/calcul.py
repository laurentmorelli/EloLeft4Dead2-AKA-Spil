# -*- coding: utf-8 -*-
""" Data models"""
import datetime
from app.main import db



#--------------
# Calcul Document
#--------------
class Calcul(db.Document):
    _id = db.StringField(required=True, primary_key=True)         
    import_date = db.DateTimeField(default=datetime.datetime.now)
    id_match=db.IntField() 
    id_methode=db.StringField() 
    id_joueur=db.StringField() 
    elo =db.IntField() 
    