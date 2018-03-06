import app.bem
from app.bem import joueur
from app.bem import match
from numpy import array
import pickle


def compute_elo_by_methode_by_match(given_methode,given_match):

    #ok we retrieve all prior matchs
    matchs = match.Match.objects(_id <= given_match._id)
	#we retrieve the joueurs
	joueurs = joueur.Joueur.objects()
    N_joueurs = joueurs.count()
    N_match = matchs.count()

    #on ne gère pas l'intelligence des poids de la méthode pour l'instant

    $matrice_participants = create_matrix($nb_matchs,$nb_joueurs,0);
	$vecteur_resultats = create_matrix($nb_matchs,1,0);
	$vecteur_elo_initial = create_matrix($nb_matchs,1,1500);

	$nb_joueurs = get_nb_joueurs($objet_joueurs);
	$nb_matchs = get_nb_matchs($objet_matchs);
	