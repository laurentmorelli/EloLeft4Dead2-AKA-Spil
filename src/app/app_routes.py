""" Api routes"""
from flask import Blueprint, jsonify, request, abort, make_response
import app.bem
from app.bem import match
from app.bem import calcul
from app.bem import joueur
from app.bem import methode_de_calcul
from mongoengine import ValidationError, NotUniqueError


app_bp = Blueprint('app', __name__)