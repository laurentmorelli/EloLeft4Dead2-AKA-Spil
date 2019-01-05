# -*- coding: utf-8 -*-
""" Data models"""
import datetime
from app.main import db



#--------------
# Joueur Document
#--------------
class Joueur(db.Document):
    _id = db.StringField(required=True, primary_key=True)         
    import_date = db.DateTimeField(default=datetime.datetime.now)
    prenom = db.StringField()
    pseudo = db.StringField()
    bot = db.BooleanField(default=False)
    comment = db.StringField()
