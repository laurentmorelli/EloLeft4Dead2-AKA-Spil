""" Test module"""
import unittest
import json
import datetime

from app import main

from app.bem import calcul
from app.bem import joueur
from app.bem import match
from app.bem import methode_de_calcul

from app.businesslogiclayer import calculator


class AppTest(unittest.TestCase):

    def setUp(self):
        #init test context
        self.app = main.create_app()
        self.client = self.app.test_client()
        #remove previous collections
        calcul.Calcul.objects.delete()
        joueur.Joueur.objects.delete()
        match.Match.objects.delete()
        methode_de_calcul.MethodeDeCalcul.objects.delete()
    
    def tearDown(self):
        pass
    

    #### GLOBAL TEST

    def test_scenarri_one(self):
        json_data = open('/src/tests/scenarii_one.json').read()
        jdata = json.loads(json_data)

        #we make all the calls to the rest API joueurs
        for inner_joueur in jdata["joueurs"]:
            response = self.client.post(
            '/api/v1/joueurs',
            data = json.dumps(
                dict(
                    _id=str(inner_joueur['_id']),
                    prenom=inner_joueur['prenom'],
                    pseudo=inner_joueur['pseudo'],
                    bot=inner_joueur['bot'],
                    comment=inner_joueur['comment'],
                    )
                ),
                content_type='application/json'
            )
        #we check that everything is fine
        joueur_number = joueur.Joueur.objects.count()
        self.assertEquals(15, joueur_number)

        #we make all the calls to the rest API matchs
        for inner_match in jdata["matchs"]:
            response = self.client.post(
            '/api/v1/matchs',
            data=json.dumps(
                dict(
                    _id=str(inner_match['_id']),
                    team1_player1=str(inner_match['team1_player1']),
                    team1_player2=str(inner_match['team1_player2']),
                    team1_player3=str(inner_match['team1_player3']),
                    team1_player4=str(inner_match['team1_player4']),
                    team2_player1=str(inner_match['team2_player1']),
                    team2_player2=str(inner_match['team2_player2']),
                    team2_player3=str(inner_match['team2_player3']),
                    team2_player4=str(inner_match['team2_player4']),
                    score_team1=inner_match['score_team1'],
                    score_team2=inner_match['score_team2'],
                    date=inner_match['date'],
                    map=inner_match['map'],
                    game_type=inner_match['game_type'],
                )
            ),
            content_type='application/json'
        )
        #we check that everything is fine
        match_number = match.Match.objects.count()
        self.assertEquals(64, match_number)

        #for the moment we don't have any calculation in our database
        calcul_number = calcul.Calcul.objects.count()
        self.assertEquals(0, calcul_number)

        #alright let's try to calculate the elo for the last match -> 63

        match_to_calculate = match.Match.objects(_id = 63).first()
        calculator.compute_elo_by_methode_by_match(given_match = match_to_calculate)

        #ok we shall have now some calculations recorded in our db ;)
        calcul_number = calcul.Calcul.objects.count()
        self.assertEquals(15, calcul_number)

