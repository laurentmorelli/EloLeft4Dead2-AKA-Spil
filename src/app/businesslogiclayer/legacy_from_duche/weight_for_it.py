# -*- coding: utf-8 -*-
#importe les fonctions dont on a besoin
from numpy import *

from sys import argv,exit
import json

#recupere l'argument et le transforme en matrice 'numpy'
try:
    N = json.loads(argv[1])[1] #nombre de lignes=nombre de matchs
    id_w = json.loads(argv[1])[0] #methode utilisee
except:
    print("ERROR : python could not load arguments ")
    exit(1)


if id_w==0:
	w=ones((1,N))
elif id_w==1:
	w=zeros((1,N))
	w[0,-20:]=1
elif id_w==2:
	w=ones((1,N))*((1.+arange(N))/N)
	w=ones((1,N))*(1/sqrt(N-arange(N)))
#	$weight_matchs[$i][0]=round(1/sqrt($nb_matchs-$i),3);};
elif id_w==3:
	w=random.random((1,N))
	
# change le format pour que json puisse lire
y=array(w).tolist()

# reformatte par json et envoie sur stdout (pour php)
print(json.dumps(y))