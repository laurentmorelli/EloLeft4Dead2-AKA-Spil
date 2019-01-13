# -*- coding: utf-8 -*-
import app.bem
from app.bem import joueur
from app.bem import match
from app.bem import calcul
from numpy import array
from math import log
from numpy.linalg import pinv
import numpy as np
import pickle

import logging
from logging.config import fileConfig
fileConfig('/src/app/logging.ini')
logger = logging.getLogger()

from app.utils import simple_time_tracker

@simple_time_tracker.simple_time_tracker()
def compute_elo_by_methode_by_match(given_match,given_methode=None):
    logger.info('- compute_elo_by_methode_by_match for match %s', str(given_match._id))
    #ok we retrieve all prior matchs
    allmatchs = match.Match.objects().all()
    priormatch =[]
    for inner_match in allmatchs:
        if inner_match.import_date < given_match.import_date:
            priormatch.append(inner_match)
    #yeah yeah no idea why mongoengine can't do it easyly directly, anyway...
    
    #we retrieve the joueurs
    joueurs = joueur.Joueur.objects().all()

    #we create a local dictionnaries of id matchs and dimid
    id_matchs_dim_dict = {}

    nb_count = 0
    for inner_match in priormatch:
        id_matchs_dim_dict[inner_match.id]=nb_count
        nb_count +=1

    #we create a local dictionnaries of id joueurs and dimid
    id_joueurs_dim_dict = {}
    dim_id_joueurs_dict = {}

    nb_count = 0
    for inner_joueurs in joueurs:
        id_joueurs_dim_dict[inner_joueurs.id]=nb_count
        dim_id_joueurs_dict[nb_count]=inner_joueurs.id
        nb_count +=1

    N_joueurs = joueurs.count()
    N_match = len(priormatch)
    
    matrice_participants = np.zeros((N_match, N_joueurs))
    
    matrice_resultats = np.zeros((N_match,1))
    vecteur_elo_initial = 1500 * np.ones((N_joueurs,1))

    for inner_match in priormatch:
        try:
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team1_player1]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team1_player2]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team1_player3]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team1_player4]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team2_player1]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team2_player2]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team2_player3]] =1
            matrice_participants[id_matchs_dim_dict[inner_match.id]][id_joueurs_dim_dict[inner_match.team2_player4]] =1
            matrice_resultats[id_matchs_dim_dict[inner_match.id]][0] = 1000*(inner_match.score_team1-inner_match.score_team2)/(inner_match.score_team1+inner_match.score_team2)
            matrice_resultats[id_matchs_dim_dict[inner_match.id]][0] = 500*(log(inner_match.score_team1)-log(inner_match.score_team2))
        except Exception as exception:
            logger.error(exception)
            logger.error(id_matchs_dim_dict[inner_match.id])
            logger.error(id_joueurs_dim_dict[inner_match.team1_player1])


    pseudoinverted_matrice = pinv(matrice_participants)
    elos = np.dot(pseudoinverted_matrice, matrice_resultats)
    elos = elos + vecteur_elo_initial

    #alright now we save the elo
    for i in range(N_joueurs):
        #we get back the player
        current_id_joueur = dim_id_joueurs_dict[i]
        #we build the id of the calculation
        newcalculId = str(given_match._id) + '-' + str(current_id_joueur)

        if given_methode is not None:
            newcalculId += '-'+ str(given_methode._id)

        #we remove any potential older calculation
        for calc in calcul.Calcul.objects(_id =str(newcalculId)):
            calc.delete()

        newcalcul = calcul.Calcul(
            _id=str(given_match._id) + '-' + str(current_id_joueur),
            id_match=given_match._id,
            id_joueur=current_id_joueur,
            elo=elos[i]
        )

        if given_methode is not None:
            newcalcul.id_methode = given_methode._id
        
        #alright we're all good
        newcalcul.save()
        

    return elos