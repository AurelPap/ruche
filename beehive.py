##########
# Import #
##########

import numpy as np
import random
import math
import csv
import pandas as pd

####################
# Variable globale #
####################

df_liste_moyenne = pd.DataFrame(columns=["generation", "min", "moyenne", "max"])

##########
# Classe #
##########



class Abeille:
    point_depart = (500, 500)
    distance = 0

    def __init__(self, trajet, generation, numero):
        self.trajet = trajet
        self.generation = generation
        self.numero = numero
        self.nom = f"abeille_g{self.generation}_n{self.numero}"

    def calcul_distance(self):
        for i, point in enumerate(self.trajet):
            if i == 0:
                point_precedent = self.point_depart
            else:
                point_precedent = self.trajet[i - 1]
            self.distance += distance_entre_2_points(point_precedent, point)
        return self.distance


#####################
# Fonctions de base #
#####################


def afficher_liste_moyenne():
    return df_liste_moyenne

def distance_entre_2_points(point_1, point_2):
    # On definit les coordonnées des points
    x1, y1 = point_1
    x2, y2 = point_2

    # On calcule et on retourne la valeur de la distance entre les 2 points
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance


def lecture_csv_points(fichier):
    liste_point = []

    with open(fichier, 'r') as f:
        lecteur_csv = csv.reader(f)

        # Ignorer l'en-tête
        next(lecteur_csv)

        for ligne in lecteur_csv:
            x, y = map(int, ligne)
            point = (x, y)
            liste_point.append(point)
    return liste_point


def df_ajout_abeille(abeille, df):

    nom = abeille.nom
    generation = abeille.generation
    numero = abeille.numero
    trajet = abeille.trajet
    distance = abeille.calcul_distance()

    nouvelle_ligne = pd.DataFrame({
        'Instance': [abeille],
        'Nom': [nom],
        'Generation': [generation],
        'Numero': [numero],
        'Trajet': [trajet],
        'Distance_totale': [distance]
    })

    df = pd.concat([df, nouvelle_ligne], ignore_index=True)
    return df


#######################################
# Fonctions de création de génération #
#######################################


def creation_premiere_generation(liste_point):
    global df_liste_moyenne
    df = pd.DataFrame(
        columns=['Instance', 'Nom', 'Generation', 'Numero', 'Trajet', 'Distance_totale'])


    for i in range(1, 101):
        trajet_copie = liste_point.copy()  # Créez une copie de la liste de points
        random.shuffle(trajet_copie)
        abeille = Abeille(trajet=trajet_copie, generation=1, numero=i)
        df = df_ajout_abeille(abeille=abeille, df=df)

    
    
    df_liste_moyenne = pd.concat([df_liste_moyenne, pd.DataFrame({
        "generation": [1],
        "min" : [df['Distance_totale'].min()],
        "moyenne" : [df['Distance_totale'].mean()],
        "max" : [df['Distance_totale'].max()],
        })], ignore_index=True)
    return df


def creation_nouvelle_generation(df_init, nb_generation):
    global df_liste_moyenne
    df_init.sort_values('Distance_totale', inplace=True)
    df_init_cut = df_init.reset_index(drop=True).loc[:49]
    df_final_cut = df_init_cut.copy()

    for i in range(1, 51):
        methode = random.randrange(3)
        if methode == 0:
            trajet_enfant = croisement(df_init_cut)
        elif methode == 1:
            trajet_enfant = mutation(df_init_cut)
        elif methode == 2:
            trajet_enfant = mutation_2(df_init_cut)
        else:
            trajet_enfant = aleatoire(df_init_cut)
        abeille = Abeille(trajet=trajet_enfant,
                          generation=nb_generation, numero=i)
        df_final_cut = df_ajout_abeille(abeille=abeille, df=df_final_cut)
        
        
        
    df_liste_moyenne = pd.concat([df_liste_moyenne, pd.DataFrame({
        "generation": [nb_generation], 
        "min" : [df_final_cut['Distance_totale'].min()],
        "moyenne" : [df_final_cut['Distance_totale'].mean()],
        "max" : [df_final_cut['Distance_totale'].max()]
        })], ignore_index=True)
    return df_final_cut


##################################
# Fonctions Algorithme génétique #
##################################


def croisement(df_init_cut):

    # Prendre 2 chiffres au hasard entre 0 et 49
    nombre1, nombre2 = random.sample(range(50), 2)

    # Extraire le trajet de parent1 et parent2 du dataframe
    trajet_parent_1 = df_init_cut.iloc[nombre1]['Trajet']
    trajet_parent_2 = df_init_cut.iloc[nombre2]['Trajet']

    # Determiner une zone de pivot
    pivot = random.randrange(50)

    # Créer l'enfant
    trajet_enfant = [-1] * 50

    # La partie avant le pivot de l'enfant devient la partie avant le pivot du parent 1
    trajet_enfant[:pivot] = trajet_parent_1[:pivot]

    # On cherche les fleurs qui ne sont pas encore dans la liste enfant
    fleurs_restantes = [
        point for point in trajet_parent_2 if point not in trajet_enfant]

    # La partie de l'enfant après le pivot devient la liste des fleurs restantes
    trajet_enfant[pivot:] = fleurs_restantes
    return trajet_enfant


def mutation(df_init_cut):
    num_mute = random.randrange(50)
    trajet_mute = df_init_cut.loc[num_mute]['Trajet']

    indice_1 = random.randrange(50)
    indice_2 = random.randrange(50)

    trajet_mute[indice_1], trajet_mute[indice_2] = trajet_mute[indice_2], trajet_mute[indice_1]
    return trajet_mute


def mutation_2(df_init_cut):
    index_1 = random.randrange(50)
    trajet_mute = df_init_cut.loc[index_1]['Trajet']
    nouveau_trajet = trajet_mute[1:] + [trajet_mute[0]]
    return nouveau_trajet


def aleatoire(df_init_cut):
    trajet_aleatoire = df_init_cut.loc[1]['Trajet']
    random.shuffle(trajet_aleatoire)
    
    return trajet_aleatoire