""" Api routes"""
from flask import Blueprint, jsonify, request, abort, make_response
import app.bem
from app.bem import match
from app.bem import calcul
from app.bem import joueur
from app.bem import methode_de_calcul
from mongoengine import ValidationError, NotUniqueError


api = Blueprint('api', __name__)

#---------
# Return JSON helper
#---------
def response(status_code, data):
    """ JSON Response helper"""
    return make_response(jsonify(data), status_code)



#####GENERAL items

# -------
# Match REST
# -------

# ----------
# Get matchs information
# ----------
@api.route('/api/v1/matchs', methods=['GET'])
def matchs_information():
    """ Get matchs information"""
    try:
        count = match.Match.objects.count()
        if count == 0:
            return response(200, {'data' : {'count': count}})
        lastmatch = match.Match.objects.only('import_date').order_by("-import_date").limit(-1).first()
        return response(200, {'data' : {'count': count, 'last_import_date': lastmatch.import_date}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific matchs information
# ----------
@api.route('/api/v1/matchs/<string:match_id>', methods=['GET'])
def match_information(match_id):
    """ Get matchs information"""
    try:
        currentmatch = match.Match.objects(_id=match_id)
        if not currentmatch:
            return response(404, {'error': 'Invalid request : no match found with provided _id'})
        return response(201, {'data': currentmatch})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Add match
# ----------
@api.route('/api/v1/matchs', methods=['POST'])
def add_match():
    """ Add match"""
    try:
        newmatch = match.Match(
            _id=request.json['_id'],
            team1_player1=request.json['team1_player1'],
            team1_player2=request.json['team1_player2'],
            team1_player3=request.json['team1_player3'],
            team1_player4=request.json['team1_player4'],
            team2_player1=request.json['team2_player1'],
            team2_player2=request.json['team2_player2'],
            team2_player3=request.json['team2_player3'],
            team2_player4=request.json['team2_player4'],
            score_team1=request.json['score_team1'],
            score_team2=request.json['score_team2'],
            date=request.json['date'],
            #date=datetime.strptime(request.json['date'],"%d/%m/%Y"),
            map=request.json['map'],
            game_type=request.json['game_type']
        )
        output = newmatch.save()
        return response(201, {'data': output})
    except KeyError:
        abort(400, {'error': 'Invalid request : wrong key'})
    except NotUniqueError:
        abort(400, {'error': 'Invalid request : duplicate _id'})
    except ValidationError:
        abort(400, {'error': 'Invalid request : wrong value'})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all matchs
# ----------
@api.route('/api/v1/matchs', methods=['DELETE'])
def delete_matchs():
    """ Delete all matchs"""
    try:
        match.Match.objects.delete()
        return response(200, {'data' : {'message': 'All matchs have been successfully deleted'}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a match
# ----------

@api.route('/api/v1/matchs/<string:match_id>', methods=['DELETE'])
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
        print exception
        abort(500, {'error': 'Internal error'})


# -------
# Joueur REST
# -------

# ----------
# Get joueurs information
# ----------
@api.route('/api/v1/joueurs', methods=['GET'])
def joueurs_information():
    """ Get joueurs information"""
    try:
        count = joueur.Joueur.objects.count()
        if count == 0:
            return response(200, {'data' : {'count': count}})
        lastjoueur = joueur.Joueur.objects.only('import_date').order_by("-import_date").limit(-1).first()
        return response(200, {'data' : {'count': count, 'last_import_date': lastjoueur.import_date}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific joueurs information
# ----------
@api.route('/api/v1/joueurs/<string:joueur_id>', methods=['GET'])
def joueur_information(joueur_id):
    """ Get joueurs information"""
    try:
        currentjoueur = joueur.Joueur.objects(_id=joueur_id)
        if not currentjoueur:
            return response(404, {'error': 'Invalid request : no joueur found with provided _id'})
        return response(201, {'data': currentjoueur})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Add joueur
# ----------
@api.route('/api/v1/joueurs', methods=['POST'])
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
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all joueurs
# ----------
@api.route('/api/v1/joueurs', methods=['DELETE'])
def delete_joueurs():
    """ Delete all joueurs"""
    try:
        joueur.Joueur.objects.delete()
        return response(200, {'data' : {'message': 'All joueurs have been successfully deleted'}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a joueur
# ----------

@api.route('/api/v1/joueurs/<string:joueur_id>', methods=['DELETE'])
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
        print exception
        abort(500, {'error': 'Internal error'})

# -------
# calcul REST
# -------

# ----------
# Get calculs information
# ----------
@api.route('/api/v1/calculs', methods=['GET'])
def calculs_information():
    """ Get calculs information"""
    try:
        count = calcul.Calcul.objects.count()
        if count == 0:
            return response(200, {'data' : {'count': count}})
        lastcalcul = calcul.Calcul.objects.only('import_date').order_by("-import_date").limit(-1).first()
        return response(200, {'data' : {'count': count, 'last_import_date': lastcalcul.import_date}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific calculs information
# ----------
@api.route('/api/v1/calculs/<string:calcul_id>', methods=['GET'])
def calcul_information(calcul_id):
    """ Get calculs information"""
    try:
        currentcalcul = calcul.Calcul.objects(_id=calcul_id)
        if not currentcalcul:
            return response(404, {'error': 'Invalid request : no calcul found with provided _id'})
        return response(201, {'data': currentcalcul})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Add calcul
# ----------
@api.route('/api/v1/calculs', methods=['POST'])
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
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all calculs
# ----------
@api.route('/api/v1/calculs', methods=['DELETE'])
def delete_calculs():
    """ Delete all calculs"""
    try:
        calcul.Calcul.objects.delete()
        return response(200, {'data' : {'message': 'All calculs have been successfully deleted'}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a calcul
# ----------

@api.route('/api/v1/calculs/<string:calcul_id>', methods=['DELETE'])
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
        print exception
        abort(500, {'error': 'Internal error'})


# -------
# Methode de calcul REST
# -------


# ----------
# Get methode_de_calculs information
# ----------
@api.route('/api/v1/methode_de_calculs', methods=['GET'])
def methode_de_calculs_information():
    """ Get methode_de_calculs information"""
    try:
        count = methode_de_calcul.MethodeDeCalcul.objects.count()
        if count == 0:
            return response(200, {'data' : {'count': count}})
        lastmethode_de_calcul = methode_de_calcul.MethodeDeCalcul.objects.only('import_date').order_by("-import_date").limit(-1).first()
        return response(200, {'data' : {'count': count, 'last_import_date': lastmethode_de_calcul.import_date}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Get specific methode_de_calculs information
# ----------
@api.route('/api/v1/methode_de_calculs/<string:methode_de_calcul_id>', methods=['GET'])
def methode_de_calcul_information(methode_de_calcul_id):
    """ Get methode_de_calculs information"""
    try:
        currentmethode_de_calcul = methode_de_calcul.MethodeDeCalcul.objects(_id=methode_de_calcul_id)
        if not currentmethode_de_calcul:
            return response(404, {'error': 'Invalid request : no methode_de_calcul found with provided _id'})
        return response(201, {'data': currentmethode_de_calcul})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Add methode_de_calcul
# ----------
@api.route('/api/v1/methode_de_calculs', methods=['POST'])
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
        print exception
        abort(500, {'error': 'Internal error'})


# ----------
# Delete all methode_de_calculs
# ----------
@api.route('/api/v1/methode_de_calculs', methods=['DELETE'])
def delete_methode_de_calculs():
    """ Delete all methode_de_calculs"""
    try:
        methode_de_calcul.MethodeDeCalcul.objects.delete()
        return response(200, {'data' : {'message': 'All methode_de_calculs have been successfully deleted'}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Delete a methode_de_calcul
# ----------

@api.route('/api/v1/methode_de_calculs/<string:methode_de_calcul_id>', methods=['DELETE'])
def delete_methode_de_calcul(methode_de_calcul_id):
    """Delete a methode_de_calcul"""
    try:
        todelete_methode_de_calcul = methode_de_calcul.MethodeDeCalcul.objects(_id=methode_de_calcul_id)
        if not todelete_methode_de_calcul:
            return response(404, {'error': 'Invalid request : no methode_de_calcul found with provided _id'})
        # Delete methode_de_calcul
        todelete_methode_de_calcul.delete()
        return response(200, {'data': {'message': 'methode_de_calcul successfully deleted'}})
    except Exception as exception:
        print exception
        abort(500, {'error': 'Internal error'})

# ----------
# Gateway (NOT FOUND)
# ----------
@api.route('/api/', defaults={'invalid_path': ''}, methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
@api.route('/<path:invalid_path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def not_found_error(invalid_path):
    """Not found"""
    abort(404, {'error': 'Url not found'})

#----------
# Error 400
#----------
@api.errorhandler(400)
def invalid_400(error):
    """Handle 400 errors"""
    return response(400, error.description)

#----------
# Error 404
#----------
@api.errorhandler(404)
def invalid_404(error):
    """Handle 404 errors"""
    return response(404, error.description)

#----------
# Error 500
#----------
@api.errorhandler(500)
def invalid_500(error):
    """Handle 500 errors"""
    return response(500, error.description)