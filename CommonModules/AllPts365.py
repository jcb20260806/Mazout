# -*- coding: utf-8 -*-
#  create allpoints

import time

from CommonModules.jcbsqlitelibv01 import *

#from jcbPyLibraryv201903 import *
'''

Debug = 0
import sqlite3 as jcbSQL
import math

import datetime

'''
def GenerateAllPts365(parDB, parInTable, parOutTable):
    # AllPts365 est la table qui donne les index futurs sur base des myoyennes passees 
    GenDBCursor = parDB.cursor()
    GenDBCursor2 = parDB.cursor()
    QStr = "DROP TABLE IF EXISTS " + parOutTable
    GenDBCursor2.execute(QStr)

    # CREATE TABLE AllPts(Numero Integer, Date Text, Heure Text, HPJourReal, JourdsAn Integer, TimeSt Real)
    QStr = "CREATE TABLE " + parOutTable + " (Numero Integer, Jour Integer,Date Text, HPJour Real, JourdsAn Integer,TimeSt Real,CrtIndex Real)"

    GenDBCursor2.execute(QStr)
    parDB.commit()
    # Get Moyenne par Jour
    QStr = "Select * from Moyennes"

    GenDBCursor.execute(QStr)

    # Moyennes est un dictionnaire donnant les moyennes d' heure/jour pour chaque jour dans l' an
    Moyennes={r[0]:r[1] for r in GenDBCursor.fetchall()}
    # get last record of AllPts= c' est le preier jour a voir
    QStr = "Select * from "+parInTable+" Order by TimeSt Desc"
    GenDBCursor.execute(QStr)
    PrvRow = GenDBCursor.fetchone()
    Index=PrvRow[6]

    for i in range(751):
        # get Day in Year
        # convert NextTimeSt to struct_time
        NextTimeSt = PrvRow[5] + 86400
        DT=time.localtime(NextTimeSt)
        DinY=DT[7]
        MD=Moyennes[DinY]
        # create new record in AllPts365
        # CREATE TABLE AllPts(Numero Integer, Jour Integer, Date Text, HPJour Real, JourdsAn Integer, TimeSt Real)
        # put in parOutTable=Allpts365
        ListOfFields=[]
        ListOfFields.append(int(PrvRow[0])+1)
        ListOfFields.append(NextTimeSt/86400)
        CD=time.gmtime(NextTimeSt)
        CDf=time.strftime("%d/%m/%Y",CD)
        ListOfFields.append(CDf)
        ListOfFields.append(MD)
        ListOfFields.append(DinY)
        ListOfFields.append(NextTimeSt)
        Index=MD+Index
        ListOfFields.append(Index)
        PrvRow=list(ListOfFields)
        jcbUpDateTable(parOutTable,GenDBCursor,ListOfFields)


    parDB.commit()
    return
def AllPts365(db):
    
    parInTable1="AllPts"
    parOutTable="AllPts365"
    
    a = GenerateAllPts365(db, parInTable1, parOutTable)
    db.commit()
    
    return
#


if __name__ == '__main__':
    parDB = "./db/Mazout-DB.sql"
    parInTable1 = "AllPts"
    parOutTable = "AllPts365"
    db = jcbOpenDB(parDB)
    a = GenerateAllPts365(db, parInTable1, parOutTable)
    db.commit()
    db.close()



