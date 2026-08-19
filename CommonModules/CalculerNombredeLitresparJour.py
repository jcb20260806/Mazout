# -*- coding: utf-8 -*-
#  create allpoints

'''
Debug = 0
import sqlite3 as jcbSQL
import math
import time
import datetime
from jcbPyLibraryv201903 import *
'''
from CommonModules.DisplayIndexduJour import *

def CalculerLitresParHeureDepuisDernierPlein(parDB, parIndexTable, parInFilltable):
    GenDBCursor = parDB.cursor()
    GenDBCursor2 = parDB.cursor()
    # Get Time Stamp of avant dernier and dernier Plein
    QStr = "Select TimeSt,* from LogInFill where Plein='VRAI' Order by TimeSt ASC"
    GenDBCursor.execute(QStr)
    Row = GenDBCursor.fetchall()
    AvantDernierPlainTimeSt = Row[-2][0]
    LastPleinTimeSt = Row[-1][0]

    # aller chercher les mvt relevants
    QStr = "Select Mvt,TimeSt from LogInFill where TimeSt>'" + str(AvantDernierPlainTimeSt) + "' and TimeSt<='" + str(
        LastPleinTimeSt) + "' Order by TimeSt ASC"
    GenDBCursor.execute(QStr)
    Row = GenDBCursor.fetchall()
    Mazout = 0
    for m in Row:
        Mazout = Mazout + m[0]
    # index entre FirstPleinTimeStamp et LastPleinTimeStamp
    QStr = "Select IndexCum,TimeSt from AllPts where TimeSt>'" + str(AvantDernierPlainTimeSt) + "' and TimeSt<='" + str(
        LastPleinTimeSt) + "' Order by TimeSt ASC"
    GenDBCursor.execute(QStr)
    Row = GenDBCursor.fetchall()
    FirstIndex = Row[0][0]
    LastIndex = Row[-1][0]
    DeltaIndex = LastIndex - FirstIndex

    Consommation = Mazout / DeltaIndex

    return Consommation


def CalculerLitresParHeure(parDB, parIndexTable, parInFilltable):
    GenDBCursor = parDB.cursor()
    GenDBCursor2 = parDB.cursor()
    # Get Time Stamp of First and Last Plein
    QStr = "Select TimeSt,* from LogInFill where Plein='VRAI' Order by TimeSt ASC"
    GenDBCursor.execute(QStr)
    Row = GenDBCursor.fetchall()
    FirstPleinTimeSt=Row[0][0]
    LastPleinTimeSt=Row[-1][0]

    # aller chercher les mvt relevants
    QStr = "Select Mvt,TimeSt from LogInFill where TimeSt>'"+str(FirstPleinTimeSt)+"' and TimeSt<='"+ str(LastPleinTimeSt)+"' Order by TimeSt ASC"
    GenDBCursor.execute(QStr)
    Row = GenDBCursor.fetchall()
    Mazout=0
    for m in Row:
        Mazout=Mazout+m[0]
    # index entre FirstPleinTimeStamp et LastPleinTimeStamp
    QStr = "Select IndexCum,TimeSt from AllPts where TimeSt>'" + str(FirstPleinTimeSt) + "' and TimeSt<='" + str(LastPleinTimeSt) + "' Order by TimeSt ASC"
    GenDBCursor.execute(QStr)
    Row = GenDBCursor.fetchall()
    FirstIndex=Row[0][0]
    LastIndex=Row[-1][0]
    DeltaIndex=LastIndex-FirstIndex

    Consommation=Mazout/DeltaIndex

    return Consommation
#
def Main():
    parDB="./db/Mazout-DB.sql"
    parInTable1="LogIndex"
    parInTable2="LogInFill"
    db = jcbOpenDB(parDB)
    a = CalculerLitresParJour(db, parInTable1, parInTable2)
    db.commit()
    db.close()
    return


if __name__ == '__main__':
    Main()
