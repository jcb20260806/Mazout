# -*- coding: utf-8 -*-
#  create allpoints
#from jcbbudgetlibv01 import *
'''
Debug = 0
import sqlite3 as jcbSQL
import math
import time
import datetime
from jcbPyLibraryv201903 import *
'''
def CalculerMoyennes(parDB, parInTable1, parOutTable):
    GenDBCursor = parDB.cursor()
    GenDBCursor2 = parDB.cursor()
    QStr = "DROP TABLE IF EXISTS "+ parOutTable
    GenDBCursor.execute(QStr)
    QStr = "CREATE TABLE " + parOutTable + " (JourdsAn Integer, HPJour Real)"
    GenDBCursor.execute(QStr)

    GenDBCursor.execute("SELECT JourdsAn,HPJour FROM " + parInTable1+" Order by HPJour Desc")
    LineLow = GenDBCursor.fetchone()
    # Collect Moyenne par Jour
    DictOfDay={}
    Rows = GenDBCursor.fetchall()
    Encore = True
    for r in Rows:
        d=DictOfDay.get(r[0])
        if d==None:
            DictOfDay[r[0]]=[r[1]]
        else:
            d.append(float(r[1]))
            DictOfDay[r[0]]=d
        
    # Calculons les moyennes en supprimant les extremes
    for k in DictOfDay.keys():
        
        d=DictOfDay.get(k)
        '''
        d.sort()
        d.pop(0)
        d.pop(-1)
        '''
        s=0
        l=len(d)
        for h in d:
            s=s+h
        h=s/l
        DictOfDay[k]=h
    jcb=1
    for i in DictOfDay.items():
        QueryLst = []
        QueryLst.append("INSERT INTO ")
        QueryLst.append(parOutTable)
        QueryLst.append(" VALUES (")
        QueryLst.append('"' + str(i[0]) + '",')
        QueryLst.append('"' + str(i[1]) + '",')

        QStr = ''.join(QueryLst)
        QStr = QStr[0:-1] + ")"
        GenDBCursor.execute(QStr)

    parDB.commit()
    return 1


#
def Main():
    parDB="./db/Eau-DB.sql"
    parInTable="AllPts"
    parOutTable="Moyennes"
    db = jcbOpenDB(parDB)
    a = CalculerMoyennes(db, parInTable, parOutTable)
    db.commit()
    db.close()
    return


if __name__ == '__main__':
    Main()
