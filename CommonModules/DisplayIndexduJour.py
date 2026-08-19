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
def CalculIndexatAnyTime(parDB, parInTable,parTimeStamp):
    GenDBCursor = parDB.cursor()

    QStr = "Select * from "+parInTable+" where TimeSt<"+str(parTimeStamp)+" Order by TimeSt Desc"
    #try:
    GenDBCursor.execute(QStr)
    #except:
    #jcbLogError(QStr)
    Row = GenDBCursor.fetchone()

    Index=Row[6]
    CrtTimeSt=Row[5]
    DeltaTimeSt=parTimeStamp-CrtTimeSt
    HpJour=Row[3]
    DeltaIndex=(HpJour*DeltaTimeSt)/86400
    NewIndex=Index+DeltaIndex
    GenDBCursor.close()
    return NewIndex


if __name__ == '__main__':
    parDB = "./db/Mazout-DB.sql"
    parInTable = "AllPts365"
    # getcurrent time
    TimeSt= time.time()
    db = jcbOpenDB(parDB)
    a = CalculIndexatAnyTime(db, parInTable,TimeSt)
    db.close()



