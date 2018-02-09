# -*- coding: utf-8 -*-
""" Data models"""
import datetime
from app.main import db



#--------------
# Match Document
#--------------
class Match(db.Document):
    _id = db.StringField(required=True, primary_key=True)         
    import_date = db.DateTimeField(default=datetime.datetime.now)
    team1_player1= db.StringField() 
    team1_player2= db.StringField() 
    team1_player3= db.StringField() 
    team1_player4= db.StringField() 
    team2_player1= db.StringField() 
    team2_player2= db.StringField() 
    team2_player3= db.StringField() 
    team2_player4= db.StringField() 
    score_team1 = db.IntField(required=True)
    score_team2 = db.IntField(required=True)
    date = db.DateTimeField(default=datetime.datetime.now)
    map = db.StringField()         
    game_type = db.StringField()