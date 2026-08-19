# -*- coding: utf-8 -*-
#  create allpoints
import sqlite3 as jcbSQL
#import math

import time
from CommonModules.jcbsqlitelibv01 import *


def InsertInAllPts(parDB, parInTable1, parOutTable):
    # cette fonction prend LogIndex et Genère AllPts
    # pour chaque jour on affecte le nombre d' heures par jour pour chaque jour
    GenDBCursor = parDB.cursor()
    GenDBCursor2 = parDB.cursor()
    QStr = "DROP TABLE IF EXISTS "+ parOutTable
    GenDBCursor.execute(QStr)
    QStr = "CREATE TABLE " + parOutTable + " (Numero Integer, Jour Integer,Date Text, HPJour Real, JourdsAn Integer,TimeSt Real,IndexCum Real)"
    GenDBCursor.execute(QStr)
    GenDBCursor.execute("SELECT * FROM " + parInTable1 + " ORDER BY TimeSt ASC")

    LineLow = GenDBCursor.fetchone()
    CurNumLine = 1
    LineHigh = GenDBCursor.fetchone()
    Encore = True
    while Encore:
        DayStampLow=int(LineLow[6]/86400)
        DayStampHigh = int(LineHigh[6]/86400)
        SecondStampLow=LineLow[6]
        SecondStampHigh=LineHigh[6]
        DeltaDayStamp = (SecondStampHigh - SecondStampLow)/86400
        # on calcule l ecart D INDEX entre les bornes de l intervalle       
        DeltaReleve = LineHigh[3] - LineLow[3]
        # Heure par Jour : la moyenne horaire entre LES BORNES de l intervalle
        HeureParJour = DeltaReleve/ DeltaDayStamp  # Heure par Jour

        if HeureParJour<0: # Trap Error si négatif => erreur
            print("Delta Jour Négatif dans LogIndex")
            raise()
            
        # On va affecter cette moyenne à tous les jours >=TimeStampLow et <TimeStampHigh
        # l' index de SecondTimeStampHigh= Index de Low - moyenne * Nombre de d' heure jusqu' 0h du jour suivant
        # 00:00 du premier jour de la série en secondes:
        MidnightSec=int(SecondStampLow/86400)*86400
        # Index de ce moment=Index du premier jour- (delta time stamp  )*Moyenne
        # Delta Time stamp en secondes, il faut convertir la moyenne en /seconde
        IndexMidnight=LineLow[3]-((SecondStampLow-MidnightSec)*HeureParJour)/86400
        for r in range(DayStampLow,DayStampHigh,1): #  on s' arrete avant TimeStampHigh
            wDate=time.localtime(r*86400)           # on convertit r en date 
            Date=str(wDate[2])+"/"+str(wDate[1])+"/"+str(wDate[0])
            JourdsLan=wDate[7]
            ListOfFields = [str(CurNumLine), str(r), Date,str(HeureParJour), str(JourdsLan),str(r*86400),IndexMidnight]
            jcbUpDateTable(parOutTable,GenDBCursor2,ListOfFields)
            CurNumLine = CurNumLine + 1
            IndexMidnight=IndexMidnight+HeureParJour
            #parDB.commit()

        LineLow=LineHigh
        LineHigh = GenDBCursor.fetchone()
        if (LineHigh == None):
            Encore = False
    return 1


#
def GenerateAllPts(parDB):
    #parDB="./db/Mazout-DB.sql"
    parInTable="LogIndex"
    parOutTable="AllPts"
    db = jcbSQL.connect(parDB)
    a = InsertInAllPts(db, parInTable, parOutTable)
    db.commit()
    db.close()
    return


if __name__ == '__main__':
    GenerateAllPts()
