# import pdb;pdb.set_trace()
# !/usr/bin/python3.5
# !/usr/bin/env python
SQLiteDB = "./db/Mazout-DB.sql"

#-*- coding: utf-8 -*-

#import jcbHeaderPy3v01
import sqlite3 as jcbSQL
from datetime import  *

'''
from CommonModules.jcbLogging import jcbLogInfo,jcbLogError
'''
from CommonModules.DisplayLogIndex import *
from CommonModules.DisplayLogInFill import *

from CommonModules.GenerateAllPoints import *

from CommonModules.CalculerNombredeLitresparJour import *

from CommonModules.AllPts365 import  *

from CommonModules.CalculerMoyenneparJour import *

#from CommonModules.DisplayIndexduJour import *

from CommonModules.CalculerVolumeDisponible import *

from CommonModules.CreerTablePourComparaisonIndexJournaliers import *
import time

import tkinter as tk
from tkinter import *

class jcbEntry:
    def __init__(self, master,parText):
        jcbFrame=Frame(master)
        jcbFrame.pack()
        self.label = Label(jcbFrame, text=parText)
        self.label.pack(side=LEFT)
        self.entry=Entry(jcbFrame)
        self.entry.delete(0, END)
        self.entry.insert(0, "a default value")
        self.entry.pack(side=RIGHT)
class jcbLabel:


    def __init__(self, master, parText):
        jcbFrame = Frame(master)
        jcbFrame.pack()
        self.label = Label(jcbFrame, text=parText)
        self.label.pack(side=LEFT)
def SetCurrentDate(parEntry):
    now = datetime.now()
    #now2=time.time()
    print("Current date and time: ")
    print(str(now))
    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0, now.strftime('%Y-%m-%d %H:%M:%S'))
def SetVolumeDisponible(parConso,parEntry,parDB):
    a = CalculVolumeDisponible(parDB,parConso)
    s1="{:10.2f}".format(a)
    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0, s1)
    return


def DisplayDateduDernierPlein(parEntry,parDB):
    QStr="Select * From LogInFill where Plein='VRAI' ORDER BY TimeSt DESC"
    dbCursor = parDB.cursor()
    dbCursor.execute(QStr)
    row=dbCursor.fetchone()
    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0, row[1])
    return

def DisplayConsommationGlobale(parEntry,parDB,parLogIndex,parLogInFill):
    a = CalculerLitresParHeure(parDB, parLogIndex, parLogInFill)
    s1 = "{:10.2f}".format(a)
    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0, s1)
    return
def DisplayConsommationGlobaleDepuisDernierPlein(parEntry,parDB,parLogIndex,parLogInFill):
    a = CalculerLitresParHeureDepuisDernierPlein(parDB, parLogIndex, parLogInFill)
    s1 = "{:10.2f}".format(a)
    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0, s1)
    return
def DisplayDateCommandeXLitres(parConso,parEntry,parDB,parCommande):
    TimeSt = DateDeRemplissage(parConso,parDB,parCommande)
    tt=time.gmtime(TimeSt)
    Date=time.strftime('%d-%m-%Y',tt)

    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0, Date)
    return
def SetIndexEstime(parConso,parEntry,parDB):
    CrtTime=time.time()
    TT = time.ctime(CrtTime)
    a = CalculIndexatAnyTime(parDB,"AllPts365",CrtTime)
    na="{:10.2f}".format(a)
    parEntry.entry.delete(0, END)
    parEntry.entry.insert(0,na)
    return
def Refresh():
    root.destroy
    BuildWindow()
    '''
    GenerateAllPts(SQLiteDB)
    CalculerMoyennes(db, "AllPts", "Moyennes")
    #GenerateAllPts_Interpol(SQLiteDB)
    AllPts365()
    #SetCurrentDate(Date_du_Jour)
    ConsoA = CalculerLitresParHeure(db, "LogIndex", "LogInfill")
    ConsoB = CalculerLitresParHeureDepuisDernierPlein(db, "LogIndex", "LogInFill")
    SetVolumeDisponible(ConsoA,Volume_Disponible, db)
    SetIndexEstime(ConsoA,Index_Estime, db)
    DisplayDateCommandeXLitres(ConsoA,a1000_Litres, db, 1000)
    DisplayDateCommandeXLitres(ConsoA,a2000_Litres, db, 2000)
    DisplayDateCommandeXLitres(ConsoA,a3000_Litres, db, 3000)
    DisplayDateCommandeXLitres(ConsoA,a4000_Litres, db, 4000)

    DisplayConsommationGlobale(Consommation_Moyenne_Globale, db, "LogIndex", "LogInFill")

    DisplayDateduDernierPlein(Date_du_Dernier_Plein, db)
    SetVolumeDisponible(ConsoB,Volume_Disponibleb, db)
    DisplayDateCommandeXLitres(ConsoB,a1000_Litresb, db, 1000)
    DisplayDateCommandeXLitres(ConsoB,a2000_Litresb, db, 2000)
    DisplayDateCommandeXLitres(ConsoB,a3000_Litresb, db, 3000)
    DisplayDateCommandeXLitres(ConsoB,a4000_Litresb, db, 4000)
    '''
    return

def BuildWindow():
    global Date_du_Jour
    global Volume_Disponible
    global db
    global Index_Estime
    global a1000_Litres
    global a2000_Litres
    global a3000_Litres
    global a4000_Litres
    global Consommation_Moyenne_Globale
    global Date_du_Dernier_Plein
    global Volume_Disponibleb
    global a1000_Litresb
    global a2000_Litresb
    global a3000_Litresb
    global a4000_Litresb
    #global Consommation_Moyenne_Globale_Depuis_Dernier_Plein

    db = jcbSQL.connect(SQLiteDB)
    # restore AllPts Tables
    GenerateAllPts(SQLiteDB)
    # creer la table des moyennes par jour dans l' année
    CalculerMoyennes(db,"AllPts","Moyennes")
    AllPts365(db)
    GenerateTablePourComparaisonIndexJournaliers(db)
    # Build Window
    root = tk.Tk()
    root.title('jcb Mazout Management')
    root.geometry('{}x{}'.format(900, 900))
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(2, weight=1)

    # create all of the main containers
    Info_frame = Frame(root,bg='cyan', width=450, height=50, pady=3,bd=5,relief=RAISED)
    Info_frame.grid(column=1, row=0, sticky="W")
    jcbLabel(Info_frame, "Info_Frame")
    #
    Date_du_Jour = jcbEntry(Info_frame, "Date_du_Jour")
    SetCurrentDate(Date_du_Jour)
    Date_du_Dernier_Plein = jcbEntry(Info_frame, "Date_du_Dernier_Plein")
    DisplayDateduDernierPlein(Date_du_Dernier_Plein,db)
    ConsoA = CalculerLitresParHeure(db, "LogIndex", "LogInfill")
    ConsoB = CalculerLitresParHeureDepuisDernierPlein(db, "LogIndex", "LogInFill")

    Consommation_Moyenne_Globale = jcbEntry(Info_frame, "Consommation_Moyenne_Globale")
    DisplayConsommationGlobale(Consommation_Moyenne_Globale,db,"LogIndex","LogInFill")
    Volume_Disponible = jcbEntry(Info_frame, "Volume_Disponible")
    SetVolumeDisponible(ConsoA,Volume_Disponible, db)
    Index_Estime = jcbEntry(Info_frame, "Index Estimé")
    SetIndexEstime(ConsoA,Index_Estime, db)
    a1000_Litres = jcbEntry(Info_frame, "1000 Litres")
    DisplayDateCommandeXLitres(ConsoA,a1000_Litres, db, 1000)
    a2000_Litres = jcbEntry(Info_frame, "2000 Litres")
    DisplayDateCommandeXLitres(ConsoA,a2000_Litres, db, 2000)
    a3000_Litres = jcbEntry(Info_frame, "3000 Litres")
    DisplayDateCommandeXLitres(ConsoA,a3000_Litres, db, 3000)
    a4000_Litres = jcbEntry(Info_frame, "4000 Litres")
    DisplayDateCommandeXLitres(ConsoA,a4000_Litres, db, 4000)
    Consommation_Moyenne_Globale_Depuis_Dernier_Plein = jcbEntry(Info_frame,"Consommation_Moyenne_Globale_Depuis Dernier Plein")
    DisplayConsommationGlobaleDepuisDernierPlein(Consommation_Moyenne_Globale_Depuis_Dernier_Plein, db, "LogIndex", "LogInFill")

    Volume_Disponibleb = jcbEntry(Info_frame, "Volume_Disponible")
    SetVolumeDisponible(ConsoB,Volume_Disponibleb, db)
    a1000_Litresb = jcbEntry(Info_frame, "1000 Litres")
    DisplayDateCommandeXLitres(ConsoB,a1000_Litresb, db, 1000)
    a2000_Litresb = jcbEntry(Info_frame, "2000 Litres")
    DisplayDateCommandeXLitres(ConsoB,a2000_Litresb, db, 2000)
    a3000_Litresb = jcbEntry(Info_frame, "3000 Litres")
    DisplayDateCommandeXLitres(ConsoB,a3000_Litresb, db, 3000)
    a4000_Litresb = jcbEntry(Info_frame, "4000 Litres")
    DisplayDateCommandeXLitres(ConsoB,a4000_Litresb, db, 4000)

    Index_frame = Frame(root, bg='white', width=450, height=45, pady=3,bd=5,relief=RAISED)
    Index_frame.grid(column=0, row=0, sticky="NW")
    jcbLabel(Index_frame, "Index_Frame")
    Record = jcbDisplayLogIndexRecord(Index_frame, db)

    Fill_frame = Frame(root, bg='lavender', width=450, height=60, pady=3,bd=5,relief=RAISED)
    Fill_frame.grid(column=0, row=1, sticky="E")
    jcbLabel(Fill_frame, "Fill_Frame")
    Record = jcbDisplayLogInFillRecord(Fill_frame, db)

    Button_frame = Frame(root, bg='lavender', width=450, height=60, pady=3,bd=5,relief=RAISED)
    Button_frame.grid(column=1, row=1, sticky="NW")
    jcbLabel(Button_frame, "Button_Frame")

    AllPointsButton = Button(Button_frame, text="Generate AllPoints", command=GenerateAllPts)
    AllPointsButton.pack()
    AllPoints365Button = Button(Button_frame, text="Generate AllPts365", command=AllPts365)
    AllPoints365Button.pack()
    RefreshButton = Button(Button_frame, text="Refresh Window", command=Refresh)
    RefreshButton.pack()

    return root
if __name__ == "__main__":
    print("Start Appli")
    root=BuildWindow() # create window
    root.mainloop()




