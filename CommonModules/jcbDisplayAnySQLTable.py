#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tkinter as tk
#from tkinter import messagebox
from CommonModules.jcbsqlitelibv01 import jcbOpenDB
#from jcbLogging import jcbLogError
#from tkinter import Frame
#from tkinter import Label
#from tkinter import Entry
from tkinter import *

#from jcbLogging import jcbLogInfo,jcbLogError
class jcbDisplayAnySQLiteRecord:
    # input: un frame ou accrocher, une table, un objet db
    # output l' adresse de la liste de champs ou mettre le contenu du record
    # les libellés sont pris dans la db
    class jcbEntry:
        def __init__(self, master, parText):
            jcbFrame = Frame(master)
            jcbFrame.pack()
            self.label = Label(jcbFrame, text=parText,width='10')
            self.label.pack(side=LEFT)
            self.entry = Entry(jcbFrame,justify="right")
            self.entry.delete(0, END)
            self.entry.insert(0, "a default value")
            self.entry.pack(side=RIGHT)

    def GetListOfFieldsInTable(self, parDB, parInTable):
        '''
        Crée une liste de Champs dans une fenêtre sur base d' un record SQLIte
        :param parWdw:
        :param parDB:
        :param parInTable:
        :return:
        '''
        DBCursor = parDB.cursor()
        meta = DBCursor.execute("PRAGMA table_info('" + parInTable + "')")
        # Fields contient le nom des champs de la table InputTable
        # SELECT * FROM mytable WHERE ROWID IN ( SELECT max( ROWID ) FROM mytable )
        # SELECT * FROM SAMPLE_TABLE ORDER BY ROWID ASC LIMIT 1
        Fields = []
        for r in meta:
            Fields.append(r[1])
        return Fields


    def __init__  (self,parFrame,parDB,parInTable):

        # create window
        self.MainFrame=parFrame
        #
        # create button frame
        #
        # Create Record Frame
        RecordFrame=tk.Frame(parFrame)
        RecordFrame.pack()
        #
        # get List of fields of parInTable
        #
        ListOfF=self.GetListOfFieldsInTable(parDB, parInTable)
        i=1
        self.Entry=[]
        for f in ListOfF:
            self.Entry.append(self.jcbEntry(RecordFrame,f))
        return

if __name__ == "__main__":

    # A Tuple with 9 elements.
    SQLiteDB="./db/Mazout-DB.sql"
    root = tk.Tk()
    root.title('jcb Test Frame')
    db = jcbOpenDB(SQLiteDB)
    #parFrame, parDB, parInTable, parField
    Record=jcbDisplayAnySQLiteRecord(root,db,"LogIndex","?")
    root.mainloop()
    print("fin de traitement de " + __file__)



