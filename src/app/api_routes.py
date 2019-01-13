from app.utils import simple_time_tracker
""" Api routes"""
from flask import Blueprint, jsonify, request, abort, make_response
import app.bem
from app.bem import match
from app.bem import calcul
from app.bem import joueur
from app.bem import methode_de_calcul

from app.businesslogiclayer import calculator

from mongoengine import ValidationError, NotUniqueError
from mongoengine.queryset.visitor import Q
import datetime

import logging
from logging.config import fileConfig
fileConfig('/src/app/logging.ini')
logger = logging.getLogger()


api = Blueprint('api', __name__)

# ---------
# Return JSON helper
# ---------


def response(status_code, data):
    """ JSON Response helper"""
    return make_response(jsonify(data), status_code)


# GENERAL items

# -------
# Match REST
# -------

# ----------
# Get matchs information
# ----------

@api.route('/api/v1/matchs', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def matchs_information():
    """ Get matchs information"""
    try:
        count = match.Match.objects.count()
        if count == 0:
            return response(200, {'data': {'count': count}})

        matchs = [{'id': x._id,
                   'team1_player1': x.team1_player1,
                   'team1_player2': x.team1_player2,
                   'team1_player3': x.team1_player3,
                   'team1_player4': x.team1_player4,
                   'team2_player1': x.team2_player1,
                   'team2_player2': x.team2_player2,
                   'team2_player3': x.team2_player3,
                   'team2_player4': x.team2_player4,
                   'score_team1': x.score_team1,
                   'score_team2': x.score_team2,
                   'date': x.date,
                   'map': x.map,
                   'game_type': x.game_type} for x in match.Match.objects().order_by('-_id')]

        lastmatch = match.Match.objects.only(
            'import_date').order_by("-import_date").limit(-1).first()

        return response(200, {'data': {'count': count, 'last_import_date': lastmatch.import_date, 'matchs': matchs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


@api.route('/api/v1/matchs_by_joueur/<string:joueur_id>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def matchs_information_by_joueur(joueur_id):
    """ Get matchs information"""
    try:
        matchs = [{'id': x._id,
                   'team1_player1': x.team1_player1,
                   'team1_player2': x.team1_player2,
                   'team1_player3': x.team1_player3,
                   'team1_player4': x.team1_player4,
                   'team2_player1': x.team2_player1,
                   'team2_player2': x.team2_player2,
                   'team2_player3': x.team2_player3,
                   'team2_player4': x.team2_player4,
                   'score_team1': x.score_team1,
                   'score_team2': x.score_team2,
                   'date': x.date,
                   'map': x.map,
                   'game_type': x.game_type} for x in match.Match.objects(Q(team1_player1=joueur_id) |
                                                                          Q(team1_player2=joueur_id) |
                                                                          Q(team1_player3=joueur_id) |
                                                                          Q(team1_player4=joueur_id) |
                                                                          Q(team2_player1=joueur_id) |
                                                                          Q(team2_player2=joueur_id) |
                                                                          Q(team2_player3=joueur_id) |
                                                                          Q(team2_player4=joueur_id)).order_by('-_id')]

        lastmatch = match.Match.objects.only(
            'import_date').order_by("-import_date").limit(-1).first()

        return response(200, {'data': {'count': len(matchs), 'last_import_date': lastmatch.import_date, 'matchs': matchs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Get specific matchs information
# ----------
@api.route('/api/v1/matchs/<string:match_id>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def match_information(match_id):
    """ Get matchs information"""
    try:
        currentmatch = match.Match.objects(_id=match_id)
        if not currentmatch:
            return response(404, {'error': 'Invalid request : no match found with provided _id'})
        return response(201, {'data': currentmatch})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Add match
# ----------
@api.route('/api/v1/matchs', methods=['POST'])
@simple_time_tracker.simple_time_tracker()
def add_match():
    """ Add match"""
    try:
        logger.info(str(request.json))
        # we expect a call like
        # {
        #    team1_player1:'toto',
        #    team1_player2:'toto',
        #    team1_player3:'toto',
        #    team1_player4:'toto',
        #    team2_player1:'toto',
        #    team2_player2:'toto',
        #    team2_player3:'toto',
        #    team2_player4:'toto',
        #    score_team1:10,
        #    score_team2:0,
        #    map:'toto',
        #    game_type:'toto'
        # }

        ## Error Management
        errorList = []

        expectedFields = ['team1_player1', 'team1_player2', 'team1_player3', 'team1_player4',
                          'team2_player1', 'team2_player2', 'team2_player3', 'team2_player4',
                          'score_team1', 'score_team2', 'map', 'game_type']
        for field in expectedFields:
            if field not in request.json:
                errorList.append('Field ' + field + 'is missing!!! ')

        # we check that the teams are correct
        team1_player1 = request.json['team1_player1']
        team1_player2 = request.json['team1_player2']
        team1_player3 = request.json['team1_player3']
        team1_player4 = request.json['team1_player4']
        team2_player1 = request.json['team2_player1']
        team2_player2 = request.json['team2_player2']
        team2_player3 = request.json['team2_player3']
        team2_player4 = request.json['team2_player4']

        botTeam1 = sum([1 for x in [team1_player1, team1_player2,
                                    team1_player3, team1_player4] if x == 'bot']) - 1
        if botTeam1 > 2:
                errorList.append('Team 1 is only with bots !!! ')
        botTeam2 = sum([1 for x in [team2_player1, team2_player2,
                                    team2_player3, team2_player4] if x == 'bot']) - 1
        if botTeam2 > 2:
                errorList.append('Team 2 is only with bots !!! ')
    
        score_team1 = int(request.json['score_team1']) if len(str(request.json['score_team1'])) > 0 else 0
        score_team2 = int(request.json['score_team2']) if len(str(request.json['score_team2'])) > 0 else 0

        if score_team1 == 0 and score_team2 ==0:
            errorList.append('No score recorded ')

        if len(errorList) >0:
            logger.error('The following errors have been found : '+ ' / '.join(errorList))
            return response(405, {'data': {'message': 'The following errors have been found : '+ ' / '.join(errorList)}})

        ###ok the data is now expected to be correct

        # do we have the id ?
        if '_id' in request.json:
            matchId = request.json['_id']
        else:
            matchId = match.Match.objects().order_by("-_id").limit(-1).first()._id + 1
        # do we have the date ?
        if 'date' in request.json:
            date_match = request.json['date']
        else:
            date_match = datetime.datetime.now().strftime("%d/%m/%Y")

        # fancy id management like 1 -> 0, 2 -> 1, 3-> 2
        team1_player1 = str(botTeam1) if team1_player1 == 'bot' else team1_player1
        team1_player2 = str(botTeam1) if team1_player2 == 'bot' else team1_player2
        team1_player3 = str(botTeam1) if team1_player3 == 'bot' else team1_player3
        team1_player4 = str(botTeam1) if team1_player4 == 'bot' else team1_player1
        team2_player1 = str(botTeam2) if team2_player1 == 'bot' else team2_player1
        team2_player2 = str(botTeam2) if team2_player2 == 'bot' else team2_player2
        team2_player3 = str(botTeam2) if team2_player3 == 'bot' else team2_player3
        team2_player4 = str(botTeam2) if team2_player4 == 'bot' else team2_player4

        newmatch = match.Match(
            _id=matchId,
            team1_player1=team1_player1,
            team1_player2=team1_player2,
            team1_player3=team1_player3,
            team1_player4=team1_player4,
            team2_player1=team2_player1,
            team2_player2=team2_player2,
            team2_player3=team2_player3,
            team2_player4=team2_player4,
            score_team1=score_team1,
            score_team2=score_team2,
            date=date_match,
            map=request.json['map'],
            game_type=request.json['game_type']
        )

        output = newmatch.save()
        logger.info(output)
        #Now we calculate the elo
        #calculator.compute_elo_by_methode_by_match(given_match = newmatch)
        
        return response(201, {'data': output})
    except KeyError:
        logger.error('Invalid request : wrong key')
        abort(400, {'error': 'Invalid request : wrong key'})
    except NotUniqueError:
        logger.error('Invalid request : duplicate _id')
        abort(400, {'error': 'Invalid request : duplicate _id'})
    except ValidationError as exception:
        logger.error('Invalid request : wrong value ' + str(exception.to_dict()))
        abort(400, {'error': 'Invalid request : wrong value'})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all matchs
# ----------
@api.route('/api/v1/matchs', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_matchs():
    """ Delete all matchs"""
    try:
        match.Match.objects.delete()
        return response(200, {'data': {'message': 'All matchs have been successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a match
# ----------


@api.route('/api/v1/matchs/<string:match_id>', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_match(match_id):
    """Delete a match"""
    try:
        todelete_match = match.Match.objects(_id=match_id)
        if not todelete_match:
            return response(404, {'error': 'Invalid request : no match found with provided _id'})
        # Delete match
        todelete_match.delete()
        return response(200, {'data': {'message': 'match successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# -------
# Joueur REST
# -------

# ----------
# Get joueurs information
# ----------


@api.route('/api/v1/joueurs', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def joueurs_information():
    """ Get joueurs information"""
    try:
        count = joueur.Joueur.objects.count()
        if count == 0:
            return response(200, {'data': {'count': count}})

        joueurs = [{'id': x._id, 'pseudo': x.pseudo, 'bot': x.bot}
                   for x in joueur.Joueur.objects()]

        # Now fill joueurs with elo of last match
        nbMatchs = match.Match.objects().count()
        if nbMatchs > 0:
            last_id_match = match.Match.objects().order_by('-_id').limit(1).first()._id
            for calc in calcul.Calcul.objects(id_match = last_id_match) :
                for j in joueurs :
                    if calc['id_joueur'] == j['id'] :
                        j['elo'] = calc.elo

        lastjoueur = joueur.Joueur.objects.only(
            'import_date').order_by("-import_date").limit(-1).first()
        return response(200, {'data': {'count': count, 'last_import_date': lastjoueur.import_date, 'joueurs': joueurs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific joueurs information
# ----------


@api.route('/api/v1/joueurs/<string:joueur_id>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def joueur_information(joueur_id):
    """ Get joueurs information"""
    try:
        currentjoueur = joueur.Joueur.objects(_id=joueur_id)
        if not currentjoueur:
            return response(404, {'error': 'Invalid request : no joueur found with provided _id'})
        return response(201, {'data': currentjoueur})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Add joueur
# ----------
@api.route('/api/v1/joueurs', methods=['POST'])
@simple_time_tracker.simple_time_tracker()
def add_joueur():
    """ Add joueur"""
    try:
        newjoueur = joueur.Joueur(
            _id=request.json['_id'],
            prenom=request.json['prenom'],
            pseudo=request.json['pseudo'],
            bot=request.json['bot'],
            comment=request.json['comment']
        )
        output = newjoueur.save()
        return response(201, {'data': output})
    except KeyError:
        abort(400, {'error': 'Invalid request : wrong key'})
    except NotUniqueError:
        abort(400, {'error': 'Invalid request : duplicate _id'})
    except ValidationError:
        abort(400, {'error': 'Invalid request : wrong value'})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all joueurs
# ----------
@api.route('/api/v1/joueurs', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_joueurs():
    """ Delete all joueurs"""
    try:
        joueur.Joueur.objects.delete()
        return response(200, {'data': {'message': 'All joueurs have been successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a joueur
# ----------


@api.route('/api/v1/joueurs/<string:joueur_id>', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_joueur(joueur_id):
    """Delete a joueur"""
    try:
        todelete_joueur = joueur.Joueur.objects(_id=joueur_id)
        if not todelete_joueur:
            return response(404, {'error': 'Invalid request : no joueur found with provided _id'})
        # Delete joueur
        todelete_joueur.delete()
        return response(200, {'data': {'message': 'joueur successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# -------
# calcul REST
# -------

# ----------
# Get calculs information
# ----------


@api.route('/api/v1/calculs', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def calculs_information():
    """ Get calculs information"""
    try:
        count = calcul.Calcul.objects.count()
        if count == 0:
            return response(200, {'data': {'count': count}})
        lastcalcul = calcul.Calcul.objects.only(
            'import_date').order_by("-import_date").limit(-1).first()
        calculs = [{'elo': x.elo, 'import_date': x.import_date, 'id_methode': x.id_methode, 'id_match': x.id_match, 'id_joueur': x.id_joueur }
                   for x in calcul.Calcul.objects()]
        return response(200, {'data': {'count': count, 'last_import_date': lastcalcul.import_date, 'calculs': calculs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific calculs information
# ----------


@api.route('/api/v1/calculs/<string:calcul_id>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def calcul_information(calcul_id):
    """ Get calculs information"""
    try:
        currentcalcul = calcul.Calcul.objects(_id=calcul_id)
        if not currentcalcul:
            return response(404, {'error': 'Invalid request : no calcul found with provided _id'})
        return response(201, {'data': currentcalcul})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Get calculs by user
# ----------
@api.route('/api/v1/calculs_by_user/<string:id_joueur>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def calcul_information_by_joueur(id_joueur):
    """ Get calculs information"""
    try:
        calculs = [{'elo': x.elo, 'import_date': x.import_date, 'id_match': x.id_match}
                   for x in calcul.Calcul.objects(id_joueur=id_joueur).order_by('-import_date')]
        if len(calculs) == 0:
            return response(404, {'error': 'Invalid request : no calcul found with provided id_joueur'})
        return response(200, {'data': {'count': len(calculs), 'calculs': calculs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Get last elo by methode
# ----------
@api.route('/api/v1/last_calculs_by_method/<string:id_methode>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def last_calculs_by_method(id_methode):
    """ Get calculs information"""
    try:
        # let's get the last id match
        last_id_match = match.Match.objects().order_by('-_id').limit(1).first()._id
        calculs = [{'elo': x.elo, 'import_date': x.import_date, 'id_match': x.id_match, 'id_joueur': x.id_joueur}
                   for x in calcul.Calcul.objects(id_match=last_id_match)]
        if len(calculs) == 0:
            return response(404, {'error': 'Invalid request : no calcul found with provided id_joueur'})
        return response(200, {'data': {'count': len(calculs), 'calculs': calculs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Get all elo by methode
# ----------


@api.route('/api/v1/all_calculs_by_method/<string:id_methode>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def all_calculs_by_method(id_methode):
    """ Get calculs information"""
    try:
        # let's get the last id match
        calculs = [{'elo': x.elo, 'import_date': x.import_date, 'id_match': x.id_match, 'id_joueur': x.id_joueur}
                   for x in calcul.Calcul.objects().order_by('+id_match')]
        if len(calculs) == 0:
            return response(404, {'error': 'Invalid request : no calcul found with provided id_joueur'})
        return response(200, {'data': {'count': len(calculs), 'calculs': calculs}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Add calcul
# ----------
@api.route('/api/v1/calculs', methods=['POST'])
@simple_time_tracker.simple_time_tracker()
def add_calcul():
    """ Add calcul"""
    try:
        newcalcul = calcul.Calcul(
            _id=request.json['_id'],
            id_match=request.json['id_match'],
            id_methode=request.json['id_methode'],
            id_joueur=request.json['id_joueur'],
            elo=request.json['elo']
        )
        output = newcalcul.save()
        return response(201, {'data': output})
    except KeyError:
        abort(400, {'error': 'Invalid request : wrong key'})
    except NotUniqueError:
        abort(400, {'error': 'Invalid request : duplicate _id'})
    except ValidationError:
        abort(400, {'error': 'Invalid request : wrong value'})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all calculs
# ----------
@api.route('/api/v1/calculs', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_calculs():
    """ Delete all calculs"""
    try:
        calcul.Calcul.objects.delete()
        return response(200, {'data': {'message': 'All calculs have been successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a calcul
# ----------


@api.route('/api/v1/calculs/<string:calcul_id>', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_calcul(calcul_id):
    """Delete a calcul"""
    try:
        todelete_calcul = calcul.Calcul.objects(_id=calcul_id)
        if not todelete_calcul:
            return response(404, {'error': 'Invalid request : no calcul found with provided _id'})
        # Delete calcul
        todelete_calcul.delete()
        return response(200, {'data': {'message': 'calcul successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# -------
# Methode de calcul REST
# -------


# ----------
# Get methode_de_calculs information
# ----------
@api.route('/api/v1/methode_de_calculs', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def methode_de_calculs_information():
    """ Get methode_de_calculs information"""
    try:
        count = methode_de_calcul.MethodeDeCalcul.objects.count()
        if count == 0:
            return response(200, {'data': {'count': count}})
        lastmethode_de_calcul = methode_de_calcul.MethodeDeCalcul.objects.only(
            'import_date').order_by("-import_date").limit(-1).first()
        return response(200, {'data': {'count': count, 'last_import_date': lastmethode_de_calcul.import_date}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific methode_de_calculs information
# ----------


@api.route('/api/v1/methode_de_calculs/<string:methode_de_calcul_id>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def methode_de_calcul_information(methode_de_calcul_id):
    """ Get methode_de_calculs information"""
    try:
        currentmethode_de_calcul = methode_de_calcul.MethodeDeCalcul.objects(
            _id=methode_de_calcul_id)
        if not currentmethode_de_calcul:
            return response(404, {'error': 'Invalid request : no methode_de_calcul found with provided _id'})
        return response(201, {'data': currentmethode_de_calcul})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Add methode_de_calcul
# ----------
@api.route('/api/v1/methode_de_calculs', methods=['POST'])
@simple_time_tracker.simple_time_tracker()
def add_methode_de_calcul():
    """ Add methode_de_calcul"""
    try:
        newmethode_de_calcul = methode_de_calcul.MethodeDeCalcul(
            _id=request.json['_id']
        )
        output = newmethode_de_calcul.save()
        return response(201, {'data': output})
    except KeyError:
        abort(400, {'error': 'Invalid request : wrong key'})
    except NotUniqueError:
        abort(400, {'error': 'Invalid request : duplicate _id'})
    except ValidationError:
        abort(400, {'error': 'Invalid request : wrong value'})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all methode_de_calculs
# ----------
@api.route('/api/v1/methode_de_calculs', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_methode_de_calculs():
    """ Delete all methode_de_calculs"""
    try:
        methode_de_calcul.MethodeDeCalcul.objects.delete()
        return response(200, {'data': {'message': 'All methode_de_calculs have been successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a methode_de_calcul
# ----------


@api.route('/api/v1/methode_de_calculs/<string:methode_de_calcul_id>', methods=['DELETE'])
@simple_time_tracker.simple_time_tracker()
def delete_methode_de_calcul(methode_de_calcul_id):
    """Delete a methode_de_calcul"""
    try:
        todelete_methode_de_calcul = methode_de_calcul.MethodeDeCalcul.objects(
            _id=methode_de_calcul_id)
        if not todelete_methode_de_calcul:
            return response(404, {'error': 'Invalid request : no methode_de_calcul found with provided _id'})
        # Delete methode_de_calcul
        todelete_methode_de_calcul.delete()
        return response(200, {'data': {'message': 'methode_de_calcul successfully deleted'}})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})



@api.route('/api/v1/calculate/<int:id_match>', methods=['GET'])
@simple_time_tracker.simple_time_tracker()
def calculate_matchid(id_match):
    """ Get methode_de_calculs information"""
    try:
        #do we have the expected match ?
        match_to_calculate = match.Match.objects(
            _id=id_match)
        if not match_to_calculate:
            return response(404, {'error': 'Invalid request : no match found found with provided id_match' + str(id_match)})

        calculator.compute_elo_by_methode_by_match(given_match = match_to_calculate.first())

        return response(201, {'data': 'calculation succesfully ran for match ' + str(id_match)})
    except Exception as exception:
        logger.error(exception)
        abort(500, {'error': 'Internal error'})

# ----------
# Gateway (NOT FOUND)
# ----------


@api.route('/api/', defaults={'invalid_path': ''}, methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
@api.route('/<path:invalid_path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def not_found_error(invalid_path):
    """Not found"""
    abort(404, {'error': 'Url not found'})

# ----------
# Error 400
# ----------


@api.errorhandler(400)
def invalid_400(error):
    """Handle 400 errors"""
    return response(400, error.description)

# ----------
# Error 404
# ----------


@api.errorhandler(404)
def invalid_404(error):
    """Handle 404 errors"""
    return response(404, error.description)

# ----------
# Error 500
# ----------


@api.errorhandler(500)
def invalid_500(error):
    """Handle 500 errors"""
    return response(500, error.description)
