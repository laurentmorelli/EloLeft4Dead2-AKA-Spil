""" Test module"""
import unittest
import json
import datetime

from app import main

from app.bem import calcul
from app.bem import joueur
from app.bem import match
from app.bem import methode_de_calcul


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
    
    def test_add_joueur_success(self):
        """Add one correct joueur"""
        # Request
        response = self.client.post(
            '/api/v1/joueurs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    prenom='prenom',
                    pseudo='pseudo',
                    bot=False,
                    comment='comment',
                )
            ),
            content_type='application/json'
        )
        # Check
        joueur_number = joueur.Joueur.objects.count()
        self.assertEquals(1, joueur_number)
        self.assertEquals('201 CREATED', response.status)

    def test_add_joueur_duplicate(self):
        """Add two joueurs, with same id"""
        # Request 1
        response1 = self.client.post(
            '/api/v1/joueurs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    prenom='prenom',
                    pseudo='pseudo',
                    bot=False,
                    comment='comment',
                )
            ),
            content_type='application/json'
        )
        # Request 2
        response2 = self.client.post(
            '/api/v1/joueurs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    prenom='prenom',
                    pseudo='pseudo',
                    bot=False,
                    comment='comment',
                )
            ),
            content_type='application/json'
        )
        # Check
        joueur_number = joueur.Joueur.objects.count()
        self.assertEquals(1, joueur_number)
        #self.assertEquals('400 BAD REQUEST', response2.status)
    #---------
    # Get joueur info
    #---------
    def test_get_joueurs_empty(self):
        """Get joueurs info when no joueur at all"""
        # Request
        response = self.client.get('/api/v1/joueurs', content_type='application/json')
        # Check
        self.assertEquals(['count'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(0, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)

    def test_get_joueurs_not_empty(self):
        """Get joueurs info"""
        self.test_add_joueur_success()
        # Request
        response = self.client.get('/api/v1/joueurs', content_type='application/json')
        # Check
        self.assertEquals(['count', 'joueurs', 'last_import_date' ], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(1, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_specific_joueur(self):
        """Get joueurs info"""
        self.test_add_joueur_success()
        # Request
        response = self.client.get('/api/v1/joueurs/599dfae00000000000000000', content_type='application/json')
        # Check
        self.assertEquals('201 CREATED', response.status)
    #---------
    # Delete all joueurs
    #---------
    def test_delete_all_joueurs(self):
        """Delete all joueurs"""
        self.test_add_joueur_success()
        # Request
        response = self.client.delete('/api/v1/joueurs', content_type='application/json')
        # Check
        count = joueur.Joueur.objects.count()
        self.assertEquals(0, count)
        self.assertEquals('200 OK', response.status)
    #---------
    # Delete a joueur
    #---------
    def test_delete_joueur_fail(self):
        """Delete a not existing joueur"""
        self.test_add_joueur_success()
        # Request
        response = self.client.delete('/api/v1/joueurs/599dfae00000000000000001', content_type='application/json')
        # Check
        count = joueur.Joueur.objects.count()
        self.assertEquals(1, count)
        self.assertEquals('404 NOT FOUND', response.status)
    def test_delete_joueur_success(self):
        """Delete an existing joueur"""
        self.test_add_joueur_success()
        # Request
        response = self.client.delete('/api/v1/joueurs/599dfae00000000000000000', content_type='application/json')
        # Check
        self.assertEquals('200 OK', response.status)
        count = joueur.Joueur.objects.count()
        self.assertEquals(0, count)
    #### methode de calcul TEST
    #---------
    # Add methode_de_calcul
    #---------
    def test_add_methode_de_calcul_success(self):
        """Add one correct methode_de_calcul"""
        # Request
        response = self.client.post(
            '/api/v1/methode_de_calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                )
            ),
            content_type='application/json'
        )
        # Check
        methode_de_calcul_number = methode_de_calcul.MethodeDeCalcul.objects.count()
        self.assertEquals(1, methode_de_calcul_number)
        self.assertEquals('201 CREATED', response.status)
    
    def test_add_methode_de_calcul_duplicate(self):
        """Add two methode_de_calculs, with same id"""
        # Request 1
        response1 = self.client.post(
            '/api/v1/methode_de_calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                )
            ),
            content_type='application/json'
        )
        # Request 2
        response2 = self.client.post(
            '/api/v1/methode_de_calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                )
            ),
            content_type='application/json'
        )
        # Check
        methode_de_calcul_number = methode_de_calcul.MethodeDeCalcul.objects.count()
        self.assertEquals(1, methode_de_calcul_number)
        self.assertEquals('201 CREATED', response2.status)

    #---------
    # Get methode_de_calcul info
    #---------
    def test_get_methode_de_calculs_empty(self):
        """Get methode_de_calculs info when no methode_de_calcul at all"""
        # Request
        response = self.client.get('/api/v1/methode_de_calculs', content_type='application/json')
        # Check
        self.assertEquals(['count'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(0, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_methode_de_calculs_not_empty(self):
        """Get methode_de_calculs info"""
        self.test_add_methode_de_calcul_success()
        # Request
        response = self.client.get('/api/v1/methode_de_calculs', content_type='application/json')
        # Check
        self.assertEquals(['count', 'last_import_date'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(1, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_specific_methode_de_calcul(self):
        """Get methode_de_calculs info"""
        self.test_add_methode_de_calcul_success()
        # Request
        response = self.client.get('/api/v1/methode_de_calculs/599dfae00000000000000000', content_type='application/json')
        # Check
        self.assertEquals('201 CREATED', response.status)

    #---------
    # Delete all methode_de_calculs
    #---------
    def test_delete_all_methode_de_calculs(self):
        """Delete all methode_de_calculs"""
        self.test_add_methode_de_calcul_success()
        # Request
        response = self.client.delete('/api/v1/methode_de_calculs', content_type='application/json')
        # Check
        count = methode_de_calcul.MethodeDeCalcul.objects.count()
        self.assertEquals(0, count)
        self.assertEquals('200 OK', response.status)

    #---------
    # Delete a methode_de_calcul
    #---------
    def test_delete_methode_de_calcul_fail(self):
        """Delete a not existing methode_de_calcul"""
        self.test_add_methode_de_calcul_success()
        # Request
        response = self.client.delete('/api/v1/methode_de_calculs/599dfae00000000000000001', content_type='application/json')
        # Check
        count = methode_de_calcul.MethodeDeCalcul.objects.count()
        self.assertEquals(1, count)
        self.assertEquals('404 NOT FOUND', response.status)
    def test_delete_methode_de_calcul_success(self):
        """Delete an existing methode_de_calcul"""
        self.test_add_methode_de_calcul_success()
        # Request
        response = self.client.delete('/api/v1/methode_de_calculs/599dfae00000000000000000', content_type='application/json')
        # Check
        self.assertEquals('200 OK', response.status)
        count = methode_de_calcul.MethodeDeCalcul.objects.count()
        self.assertEquals(0, count)
    ###Calcul TEST
    #---------
    # Add calcul
    #---------
    def test_add_calcul_success(self):
        """Add one correct calcul"""
        # Request
        response = self.client.post(
            '/api/v1/calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    id_match=15,
                    id_methode='toto',
                    id_joueur='toto',
                    elo=10,
                )
            ),
            content_type='application/json'
        )
        # Check
        calcul_number = calcul.Calcul.objects.count()
        self.assertEquals(1, calcul_number)
        self.assertEquals('201 CREATED', response.status)
    def test_add_calcul_value_fail(self):
        """Add one calcul (wrong value)"""
        # Request
        response = self.client.post(
            '/api/v1/calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    id_match='toto',
                    id_methode='toto',
                    id_joueur='toto',
                    elo='toto',
                )
            ),
            content_type='application/json'
        )
        # Check
        calcul_number = calcul.Calcul.objects.count()
        self.assertEquals(0, calcul_number)
        self.assertEquals('400 BAD REQUEST', response.status)
    
    def test_add_calcul_duplicate(self):
        """Add two calculs, with same id"""
        # Request 1
        response1 = self.client.post(
            '/api/v1/calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    id_match=15,
                    id_methode='toto',
                    id_joueur='toto',
                    elo=10,
                )
            ),
            content_type='application/json'
        )
        # Request 2
        response2 = self.client.post(
            '/api/v1/calculs',
            data=json.dumps(
                dict(
                    _id='599dfae00000000000000000',
                    id_match=15,
                    id_methode='toto',
                    id_joueur='toto',
                    elo=10,
                )
            ),
            content_type='application/json'
        )
        # Check
        calcul_number = calcul.Calcul.objects.count()
        self.assertEquals(1, calcul_number)
        #self.assertEquals('400 BAD REQUEST', response2.status)

    #---------
    # Get calcul info
    #---------
    def test_get_calculs_empty(self):
        """Get calculs info when no calcul at all"""
        # Request
        response = self.client.get('/api/v1/calculs', content_type='application/json')
        # Check
        self.assertEquals(['count'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(0, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_calculs_not_empty(self):
        """Get calculs info"""
        self.test_add_calcul_success()
        # Request
        response = self.client.get('/api/v1/calculs', content_type='application/json')
        # Check
        self.assertEquals(['count', 'last_import_date'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(1, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_specific_calcul(self):
        """Get calculs info"""
        self.test_add_calcul_success()
        # Request
        response = self.client.get('/api/v1/calculs/599dfae00000000000000000', content_type='application/json')
        # Check
        self.assertEquals('201 CREATED', response.status)

    #---------
    # Delete all calculs
    #---------
    def test_delete_all_calculs(self):
        """Delete all calculs"""
        self.test_add_calcul_success()
        # Request
        response = self.client.delete('/api/v1/calculs', content_type='application/json')
        # Check
        count = calcul.Calcul.objects.count()
        self.assertEquals(0, count)
        self.assertEquals('200 OK', response.status)
    #---------
    # Delete a calcul
    #---------
    def test_delete_calcul_fail(self):
        """Delete a not existing calcul"""
        self.test_add_calcul_success()
        # Request
        response = self.client.delete('/api/v1/calculs/599dfae00000000000000001', content_type='application/json')
        # Check
        count = calcul.Calcul.objects.count()
        self.assertEquals(1, count)
        self.assertEquals('404 NOT FOUND', response.status)
    def test_delete_calcul_success(self):
        """Delete an existing calcul"""
        self.test_add_calcul_success()
        # Request
        response = self.client.delete('/api/v1/calculs/599dfae00000000000000000', content_type='application/json')
        # Check
        self.assertEquals('200 OK', response.status)
        count = calcul.Calcul.objects.count()
        self.assertEquals(0, count)

    #### Match TEST
    #---------
    # Add match
    #---------
    def test_add_match_success(self):
        """Add one correct match"""
        # Request
        response = self.client.post(
            '/api/v1/matchs',
            data=json.dumps(
                dict(
                    _id=1,
                    team1_player1='toto',
                    team1_player2='toto',
                    team1_player3='toto',
                    team1_player4='toto',
                    team2_player1='toto',
                    team2_player2='toto',
                    team2_player3='toto',
                    team2_player4='toto',
                    score_team1=10,
                    score_team2=0,
                    date='02/03/1985',
                    map='toto',
                    game_type='toto',
                )
            ),
            content_type='application/json'
        )
        # Check
        match_number = match.Match.objects.count()
        self.assertEquals(1, match_number)
        self.assertEquals('201 CREATED', response.status)
    def test_add_match_value_fail(self):
        """Add one match (wrong value)"""
        # Request
        response = self.client.post(
            '/api/v1/matchs',
            data=json.dumps(
                dict(
                    _id=1,
                    team1_player1='toto',
                    team1_player2='toto',
                    team1_player3='toto',
                    team1_player4='toto',
                    team2_player1='toto',
                    team2_player2='toto',
                    team2_player3='toto',
                    team2_player4='toto',
                    score_team1='toto',
                    score_team2=0,
                    date=str(datetime.datetime.now),
                    map='toto',
                    game_type='toto',
                )
            ),
            content_type='application/json'
        )
        # Check
        match_number = match.Match.objects.count()
        self.assertEquals(0, match_number)
        self.assertEquals('400 BAD REQUEST', response.status)
    
    def test_add_match_duplicate(self):
        """Add two matchs, with same id"""
        # Request 1
        response1 = self.client.post(
            '/api/v1/matchs',
            data=json.dumps(
                dict(
                    _id=1,
                    team1_player1='toto',
                    team1_player2='toto',
                    team1_player3='toto',
                    team1_player4='toto',
                    team2_player1='toto',
                    team2_player2='toto',
                    team2_player3='toto',
                    team2_player4='toto',
                    score_team1=10,
                    score_team2=0,
                    date=str(datetime.datetime.now),
                    map='toto',
                    game_type='toto',
                )
            ),
            content_type='application/json'
        )
        # Request 2
        response2 = self.client.post(
            '/api/v1/matchs',
            data=json.dumps(
                dict(
                    _id=1,
                    team1_player1='toto',
                    team1_player2='toto',
                    team1_player3='toto',
                    team1_player4='toto',
                    team2_player1='toto',
                    team2_player2='toto',
                    team2_player3='toto',
                    team2_player4='toto',
                    score_team1=10,
                    score_team2=0,
                    date=str(datetime.datetime.now),
                    map='toto',
                    game_type='toto',
                )
            ),
            content_type='application/json'
        )
        # Check
        match_number = match.Match.objects.count()
        self.assertEquals(1, match_number)
        self.assertEquals('201 CREATED', response2.status)

    #---------
    # Get match info
    #---------
    def test_get_matchs_empty(self):
        """Get matchs info when no match at all"""
        # Request
        response = self.client.get('/api/v1/matchs', content_type='application/json')
        # Check
        self.assertEquals(['count'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(0, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_matchs_not_empty(self):
        """Get matchs info"""
        self.test_add_match_success()
        # Request
        response = self.client.get('/api/v1/matchs', content_type='application/json')
        # Check
        self.assertEquals(['count', 'last_import_date', 'matchs'], list(json.loads(response.data)['data'].keys()))
        self.assertEquals(1, json.loads(response.data)['data']['count'])
        self.assertEquals('200 OK', response.status)
    def test_get_specific_match(self):
        """Get matchs info"""
        self.test_add_match_success()
        # Request
        response = self.client.get('/api/v1/matchs/1', content_type='application/json')
        # Check
        self.assertEquals('201 CREATED', response.status)

    #---------
    # Delete all matchs
    #---------
    def test_delete_all_matchs(self):
        """Delete all matchs"""
        self.test_add_match_success()
        # Request
        response = self.client.delete('/api/v1/matchs', content_type='application/json')
        # Check
        count = match.Match.objects.count()
        self.assertEquals(0, count)
        self.assertEquals('200 OK', response.status)
    #---------
    # Delete a match
    #---------
    def test_delete_match_fail(self):
        """Delete a not existing match"""
        self.test_add_match_success()
        # Request
        response = self.client.delete('/api/v1/matchs/2', content_type='application/json')
        # Check
        count = match.Match.objects.count()
        self.assertEquals(1, count)
        self.assertEquals('404 NOT FOUND', response.status)
    def test_delete_match_success(self):
        """Delete an existing match"""
        self.test_add_match_success()
        # Request
        response = self.client.delete('/api/v1/matchs/1', content_type='application/json')
        # Check
        self.assertEquals('200 OK', response.status)
        count = match.Match.objects.count()
        self.assertEquals(0, count)