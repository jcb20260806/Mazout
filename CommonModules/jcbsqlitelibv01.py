#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os
import sqlite3 as jcbSQL
#from  jcbLogging import *


def jcbCreateTableIfNotExist(parDB, parTableName, parListOfFields):
    dbCursor = parDB.cursor()
    # Check if Table Exists"
    SQLStr = "SELECT * FROM sqlite_master WHERE name ='" + parTableName + "' and type='table'"
    row = jcbGetManyRowsFromTable(parDB, SQLStr)
    if len(row) == 0:
        jcbCreateTable(parDB, parTableName, parListOfFields)
    return


#from jcbLogging import jcbLogInfo, jcbLogError


def jcbCreateTableAfterDrop(parDB, parTableName, parListOfFields):
    # delete table
    dbCursor = parDB.cursor()
    try:
        dbCursor.execute("DROP TABLE IF EXISTS " + parTableName)
    except:
        jcbLogError("Unable to delete Table " + parTableName)
    jcbCreateTable(parDB, parTableName, parListOfFields)

    return


def jcbCreateTable(parDB, parTableName, parListOfFields):
    # create a table Dictionnaire des ContreParties
    dbCursor = parDB.cursor()
    SQLLst = []
    SQLLst.append('CREATE TABLE ')
    SQLLst.append(parTableName)
    SQLLst.append(' (')
    for f in parListOfFields:
        SQLLst.append(f[0] + ' ' + f[1] + ',')
    SQLStr = "".join(SQLLst)
    SQLStr = SQLStr[0:-1] + ')'
    print(SQLStr)
    success = True
    # try:
    dbCursor.execute(SQLStr)
    # except :
    # print ("Table "+parTableName+" Erreur à la Création")
    # success=False
    parDB.commit()
    return success


def jcbOpenDB(parDB):
    # appelant donne le full path !!!
    # cwd = os.getcwd()
    db = parDB
    try:
        DB = jcbSQL.connect(db)
    except:
        jcbLogError("Connect DB Error")
    return DB


def jcbGetManyRowsFromTable(parDB, parQStr):
    # print parQStr
    dbCursor = parDB.cursor()
    try:
        dbCursor.execute(parQStr)
    except:
        jcbLogError(parQStr)
    Row = dbCursor.fetchall()
    return Row
def jcbUpDateTable(parTableName, parCursor, parRow):
    # exemple: c.execute("INSERT INTO test VALUES (?, 'bar')", (testfield,)
    QueryLst = []
    QueryLst.append("INSERT INTO ")
    QueryLst.append(parTableName)
    QueryLst.append(" VALUES (")
    for field in parRow:
        if type(field)=='str':
            QueryLst.append('"' + field + '",')
        else:
            QueryLst.append('"' + str(field) + '",')
    QStr = ''.join(QueryLst)
    QStr = QStr[0:-1] + ")"
    try:
        parCursor.execute(QStr)
    except:
        jcbLogError(QStr)
    return 1
