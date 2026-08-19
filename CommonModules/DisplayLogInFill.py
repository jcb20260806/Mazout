#!/usr/bin/env python
#-*- coding: utf-8 -*-
from tkinter import *
#import tkinter as tk
#from tkinter import messagebox
#from jcbsqlitelibv01 import jcbOpenDB
#from jcbLogging import jcbLogError
#from tkinter import Frame
#from tkinter import Label
#from tkinter import Entry
#from Tkinter import *
from CommonModules.jcbDisplayAnySQLTable import *

from datetime import datetime,time
import time

#from jcbLogging import jcbLogInfo,jcbLogError
def jcbDate(parValue):
    # date sous la forme yyyy/mm/dd
    y=parValue[0:4]
    sl=parValue[4]+parValue[7]
    m=parValue[5:7]
    d=parValue[8:]
    if int(y)<2000 or int(y)>2050:
        return False
    if sl!='//':
        return False
    if int(m)<1 or int(m)>12:
        return False
    if int(d)<0 or int(d)>31:
        return False
    return True

def jcbHeure(parValue):
    y = parValue[0:2]
    sl = parValue[2]
    m = parValue[3:]

    if int(y) < 0 or int(y) > 24:
        return False
    if sl != ':':
        return False
    if int(m) < 0 or int(m) > 59:
        return False
    return True

    return
def jcbMvt(parValue):
    try:
        i = float(parValue)
    except:
        return False
    return True


def CreateButtonList(parFrame,parGui,parTable,parCursor,parDB):
    def BtFirst():

        DisplayRecordByNumber(0, parGui.Entry, parTable)

    def BtPrevious():
        # current keyfield
        crtk = parGui.Entry[0].entry.get()
        for index, item in enumerate(parTable):
            s=item[0]
            if str(s)==crtk:
                break
        if index<1 or index==None:
            index=0
        else:
            index=index-1
        DisplayRecordByNumber(index, parGui.Entry, parTable)

    def BtNext():
        crtk = parGui.Entry[0].entry.get()
        for index, item in enumerate(parTable):
            s = item[0]
            if str(s) == crtk:
                break
        if index==len(parTable)-1:
            index = len(parTable)-1
        else:
            index = index + 1
        DisplayRecordByNumber(index, parGui.Entry, parTable)
    def BtLast():
        DisplayRecordByNumber(len(parTable)-1, parGui.Entry, parTable)

    def BtUpDate():
        global db
        
        # validate entries
        retype=FALSE
        J = parGui.Entry[1].entry.get()
        H = parGui.Entry[2].entry.get()
        Mvt = parGui.Entry[3].entry.get()

        if not jcbDate(J):
            retype=TRUE
        if not jcbHeure(H):
            retype=TRUE
        if not jcbMvt(Mvt):

            retype=True
        if retype:
            return
        # update display and create record
        # si update de record existant on ne touche pas a key
        key=parGui.Entry[0].entry.get()
        if key=='':
            # get a new key; parTable est triee par key on prend la derniere et on ajoute 1
            key=str(int(parTable[len(parTable)-1][0])+1)
            parGui.Entry[0].entry.insert(0,key)
        #Tst=time.mktime(datetime.datetime.strptime(7, "%Y/%m/%d").timetuple())
        #timestamp = time.mktime(time.strptime('2015-10-20 22:24:46', '%Y-%m-%d %H:%M:%S'))
        JH=J+' '+H
        timestamp = time.mktime(time.strptime(JH, '%Y/%m/%d %H:%M'))
        try:
            timestamp = time.mktime(time.strptime(JH, '%Y/%m/%d %H:%M'))
        except:
            parGui.Entry[7].entry.delete(0, 'end')
            parGui.Entry[7].entry.insert(0, 'erreur de date')
            return
        parGui.Entry[7].entry.delete(0, 'end')
        parGui.Entry[7].entry.insert(0, str(timestamp))
        parGui.Entry[6].entry.delete(0, 'end')
        parGui.Entry[6].entry.insert(0, 'no W10 TimeStamp')

        if parGui.Entry[5].entry.get()=="":
            parGui.Entry[5].entry.delete(0, 'end')
            parGui.Entry[5].entry.insert(0, 'FAUX')
        else:
            parGui.Entry[5].entry.delete(0, 'end')
            parGui.Entry[5].entry.insert(0, 'VRAI')

        # build record and update parTable
        # suppress already existing line if any
        crtk = parGui.Entry[0].entry.get()
        for index, item in enumerate(parTable):
            s = item[0]
            if str(s) == crtk:
                parTable.pop((index))
        # update parTable
        r=[]
        for field in parGui.Entry:
            r.append(field.entry.get())
        done=False
        for i,item in enumerate(parTable):
            ii=item[0]
            rr=r[0]
            if int(item[0])>int(r[0]):
                parTable.insert(i,r)
                done=True
                break
        if done==False:
            parTable.append(r)


        # update LogInFill
        QueryLst = []
        QueryLst.append("INSERT INTO LogInFill VALUES (")
        for field in r:
            QueryLst.append('"' + field + '",')
            QStr = ''.join(QueryLst)
        QStr = QStr[0:-1] + ")"
        try:
            parCursor.execute(QStr)
        except:
            jcbLogError(QStr)
        # commit
        parDB.commit()
        # display last record
        DisplayRecordByKey(r[0], parGui, parTable)
        return

    def BtNew():
        for e in parGui.Entry:
            e.entry.delete(0, 'end')
        # display empty template

        return



    ButtonList = ["First", "Previous", "Next", "Last","New","UpDate"]
    ButtonActions = [BtFirst, BtPrevious, BtNext, BtLast,BtNew,BtUpDate]

    i = 0
    for b in ButtonList:
        a = ButtonActions[i]
        tk.Button(parFrame, text=b, command=a).grid(row=0, column=i)
        i = i + 1
    return

def DisplayRecordByKey(parKey,parGuiFields,parTable):
    for index, item in enumerate(parTable):
        s = item[0]
        if str(s) == parKey:
            DisplayRecordByNumber(index, parGuiFields.Entry, parTable)

def DisplayRecordByNumber(parNumber,parGuiFields,parTable):
    # pour chacun des champs il faut le bon format d' affichage et donc une conversion
    # Display`Key` INTEGER,
    #
    f1=parGuiFields[0]
    f1.entry.delete(0, 'end')
    f1.entry.insert(0, parTable[parNumber][0])

    # Display `Date`TEXT',
    #
    f1=parGuiFields[1]
    f1.entry.delete(0, 'end')
    v=parTable[parNumber][1]
    f1.entry.insert(0, v)
    # Display Heure TEXT,
    #
    f1 = parGuiFields[2]
    f1.entry.delete(0, 'end')
    v = parTable[parNumber][2]
    f1.entry.insert(0, v)
    # Display `Mvt` Int,
    #
    f1 = parGuiFields[3]
    f1.entry.delete(0, 'end')
    v = parTable[parNumber][3]
    f1.entry.insert(0, v)
    # Dispaly Plein1 Text,
    f1 = parGuiFields[4]
    f1.entry.delete(0, 'end')
    v = parTable[parNumber][4]
    f1.entry.insert(0, v)
    # Display Plein Text,
    f1 = parGuiFields[5]
    f1.entry.delete(0, 'end')
    v = parTable[parNumber][5]
    f1.entry.insert(1, v)
    # Display `Instant`REAL
    f1 = parGuiFields[6]
    f1.entry.delete(0, 'end')
    v = parTable[parNumber][6]
    #dt_object = datetime.fromtimestamp(v)
    f1.entry.insert(0, v)
    # Display `TimeSt Real
    f1 = parGuiFields[7]
    f1.entry.delete(0, 'end')
    v = parTable[parNumber][7]
    # dt_object = datetime.fromtimestamp(v)
    f1.entry.insert(0, v)


    return

def  jcbDisplayLogInFillRecord(parFrame,parDB):
    dbCursor = parDB.cursor()
    QStr = "SELECT COUNT(*) FROM LogInFill"
    dbCursor.execute(QStr)
    NombredeRecord=dbCursor.fetchone()[0]
    # Get List of Records
    dbCursor.execute("SELECT * FROM LogInFill ORDER BY TimeSt ASC")
    Table = dbCursor.fetchall()
    #
    # Create Button List
    #

    #CreateButtonList(BtFrame)
    #
    #
    RecFrame=Frame(parFrame)
    GuiFields=jcbDisplayAnySQLiteRecord(RecFrame,parDB,"LogInFill")
    BtFrame=Frame(parFrame)
    CreateButtonList(BtFrame,GuiFields,Table,dbCursor,parDB)
    BtFrame.pack()
    RecFrame.pack()
    # il faut maintenant initialiser les champss
    #
    DisplayRecordByNumber(NombredeRecord-1, GuiFields.Entry,Table)
    return

    '''
    #parWdw.protocol("WM_DELETE_WINDOW", on_closing)
    RecordWdw = jcbDisplaySQLiteRecord(parWdw, parDB, parInTable,parField)

    # CheckTypeWdw.destroy()
    return
    '''



if __name__ == "__main__":
    global db
    # A Tuple with 9 elements.
    SQLiteDB="./db/Mazout-DB.sql"
    root = tk.Tk()
    root.title('jcb Test Frame')
    db = jcbOpenDB(SQLiteDB)
    #parFrame, parDB, parInTable, parField
    Record=jcbDisplayLogInFillRecord(root,db)
    root.mainloop()
    db.close()

    print("fin de traitement de " + __file__)



