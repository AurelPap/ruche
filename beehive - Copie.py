
import numpy as np
import random
import math
import csv
import pandas as pd


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


def creation_premiere_generation(liste_point):
    df = pd.DataFrame(
        columns=['Instance', 'Nom', 'Generation', 'Numero', 'Trajet', 'Distance_totale'])

    for i in range(1, 101):
        trajet_copie = liste_point.copy()  # Créez une copie de la liste de points

        random.shuffle(trajet_copie)
        abeille = Abeille(trajet=trajet_copie, generation=1, numero=i)

        nom = abeille.nom
        generation = 1
        numero = i
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


def df_ajout_abeille(abeille):
    df = pd.DataFrame(
        columns=['Instance', 'Nom', 'Generation', 'Numero', 'Trajet', 'Distance_totale'])

    nom = abeille.nom
    generation = 1
    numero = i
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
