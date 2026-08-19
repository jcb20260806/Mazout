# -*- coding: utf-8 -*-
#  create allpoints
import time
'''
from jcbbudgetlibv01 import *

Debug = 0
import sqlite3 as jcbSQL
#import math

import datetime
'''
from CommonModules.DisplayIndexduJour import *
'''
from jcbPyLibraryv201903 import *
'''
#from CalculerNombredeLitresparJour import *
def CalculVolumeDisponible(parDB,parConso):
    if isinstance(parDB,float):
        jcb=1
    # Volume Disponible
    # Calculer Index du Moment
    # Calculer Index du dernier plein
    # en déduire la différence en heure
    # multiplier par la consommation
    # et cela donne le volume consommé, donc disponible
    # après avoir supprimé les autres remplissage
    # Calculer Index du Moment
    CrtTime = time.time()
    TT = time.ctime(CrtTime)
    # on va chercher l' IndexduMomoents dans AllPts365 qui contient les index dans le futur
    IndexDuMoment = CalculIndexatAnyTime(parDB, "AllPts365", CrtTime)
    # Calculer Index du dernier plein
    # get time stamp du dernier plein
    QStr = "Select * From LogInFill where Plein='VRAI' ORDER BY TimeSt DESC"
    dbCursor = parDB.cursor()
    dbCursor.execute(QStr)
    row = dbCursor.fetchone()
    TimeStDernierPlein = row[7]
    # get index juste avant et index juste après dans allpts or allpts365
    QStr = "Select * From AllPts where TimeSt<"+str(TimeStDernierPlein)+" Order by TimeSt Desc"
    dbCursor = parDB.cursor()
    dbCursor.execute(QStr)
    RowL = dbCursor.fetchone()
    QStr = "Select * From AllPts where TimeSt>" + str(TimeStDernierPlein) + " Order by TimeSt Asc"
    dbCursor = parDB.cursor()
    dbCursor.execute(QStr)
    RowH = dbCursor.fetchone()
    if RowH==None:
        
        QStr = "Select * From AllPts365 Order by TimeSt Asc"
        dbCursor.execute(QStr)
        RowH = dbCursor.fetchone()
        
        #jcb=sqr(RowH)
    IndexLow=RowL[6]
    TimeStL=RowL[5]
    IndexHigh=RowH[6]
    TimeStH=RowH[5]
    # index au dernier plein
    IndexDernierPlein=IndexLow+(IndexHigh-IndexLow)*(TimeStDernierPlein-TimeStL)/(TimeStH-TimeStL)
    # Consommé depuis dernier plein= deltaindex en heure * Consommation
    DeltaIndexEnHeure=(IndexDuMoment-IndexDernierPlein)
    VolumeConsommeDepuisDernierPlein=DeltaIndexEnHeure*parConso
    # calculer volume ajouté depuis dernier plein
    QStr = "Select Mvt From LogInFill where TimeSt>" + str(TimeStDernierPlein)
    dbCursor.execute(QStr)
    Rows = dbCursor.fetchall()
    V=0
    for r in Rows:
        VolumeConsommeDepuisDernierPlein=VolumeConsommeDepuisDernierPlein-r[0]
    return VolumeConsommeDepuisDernierPlein # en fzit c' est le volume disponible

def DateDeRemplissage(parConso,parDB,parCommande):
    VolumeDisponible=CalculVolumeDisponible(parDB,parConso)
    DeltaCommande=parCommande-VolumeDisponible
    # Deltacommande correspond  à
    NombredHeuresAvantCommande=DeltaCommande/parConso
    # IndexCommande = Current Index + NombredHeuresavantCommande
    CrtTime=time.time()
    TT = time.ctime(CrtTime)
    CurrentIndex = CalculIndexatAnyTime(parDB,"AllPts365",CrtTime)
    IndexCommande=CurrentIndex+NombredHeuresAvantCommande
    # trouver la date de cet index
    QStr = "Select TimeSt From AllPts365 where CrtIndex<" + str(IndexCommande)+" Order by TimeSt DEsc"
    dbCursor = parDB.cursor()
    dbCursor.execute(QStr)
    Row = dbCursor.fetchone()
    if Row==None: # cet index n' est pas dans AllPts365 car il est antérieur a la derniere prise d' index
        # on va chercher dans AllPts
        QStr = "Select TimeSt From AllPts where IndexCum<" + str(IndexCommande)+" Order by TimeSt DEsc"
        dbCursor.execute(QStr)
        Row = dbCursor.fetchone()
    TimeStCommande=Row[0]
    return TimeStCommande



