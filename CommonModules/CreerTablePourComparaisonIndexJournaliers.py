# -*- coding: utf-8 -*-
#  create allpoints
'''
from jcbsqlitelibv01 import *

Debug = 0
import sqlite3 as jcbSQL
import math
import time
import datetime
from jcbPyLibraryv201903 import *
'''

def GenerateTablePourComparaisonIndexJournaliers(parDB):
    # CompIndex est la table qui donne les index futurs sur base des myoyennes passees 
    GenDBCursor = parDB.cursor()
    GenDBCursor2 = parDB.cursor()
    QStr = "DROP TABLE IF EXISTS CompIndex"
    GenDBCursor2.execute(QStr)

    # CREATE TABLE AllPts(Numero Integer, Date Text, Heure Text, HPJourReal, JourdsAn Integer, TimeSt Real)
    QStr = "CREATE TABLE CompIndex as SELECT * from AllPts INNER JOIN Moyennes on AllPts.JourdsAn =Moyennes.JourdsAn Order By TimeSt Desc"

    GenDBCursor2.execute(QStr)
    parDB.commit()
    return


if __name__ == '__main__':
    parDB = "./db/Mazout-DB.sql"
 
    db = jcbOpenDB(parDB)
    a = GenerateTablePourComparaisonIndexJournaliers(db)
    db.commit()
    db.close()



