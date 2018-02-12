#importe les fonctions dont on a besoin
from numpy.linalg import pinv
from numpy import *

from sys import argv,exit
import json

#recupere l'argument et le transforme en matrice 'numpy'
try:
    M = matrix(json.loads(argv[1]))
except:
    print "ERROR : python could not load arguments "
    exit(1)

# # # Calculs
# extrait matrice de poids
w = M[:,:1]
# print w

# extrait matrice des joueurs (convertie en entiers)
J = M[:,1:-2].astype(int)
# print J


# construit matrice des participants
max_id = ma.max(J)
nb_matchs = shape(J)[0]

A=zeros((nb_matchs,max_id+1))

for i in range(nb_matchs):
	for j in range(4):
		A[i,J[i,j]]+=w[i]
		A[i,J[i,j+4]]-=w[i]

# print A

# extrait et calcule les resultats des matchs
b = multiply(500*w,log(M[:,-2])-log(M[:,-1]))
#$w*500*(log($data['score_team1'])-log($data['score_team2']))
# print b

# calcule vecteur des elos
x=1500+pinv(A)*b
# print x

# change le format pour que json puisse lire
y=array(x).tolist()
# print y

# reformatte par json et envoie sur stdout (pour php)
print json.dumps(y)