""" Api routes"""
from flask import Blueprint, jsonify, request, abort, make_response
import app.bem
from app.bem import user
from app.bem import simulation
from app.bem import recoadmin
from app.bem import recoia
import app.businesslogic
from app.businesslogic import recommander
from mongoengine import ValidationError, NotUniqueError


api = Blueprint('api', __name__)

#---------
# Return JSON helper
#---------
def response(status_code, data):
    """ JSON Response helper"""
    return make_response(jsonify(data), status_code)



#####GENERAL items


# ----------
# Gateway (NOT FOUND)
# ----------
@api.route('/', defaults={'invalid_path': ''}, methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
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
