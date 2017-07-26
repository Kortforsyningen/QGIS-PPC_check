# -*- coding: utf-8 -*-
import qgis
import psycopg2
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from PPC_check_dialog import PPC_checkDialog
import PPC_check
import os

# DB variables:
# Herunder skabes link til database
DB_name = "geodanmark"
DB_host = "c1200038"
DB_port = "5432"
DB_user = "postgres"
DB_pass = "postgres"
# Herunder opsttes tabellen der skal bruges. Findes tabellen ikke allerede opretts den
DB_schema = "public"
DB_geom = "geom"
DB_table = 'footprints2017'

def DB_ob(selection):
    # DB_table = 'oblique_2017_check_table'
    conn = psycopg2.connect(
        "dbname=" + DB_name + " user=" + DB_user + " host=" + DB_host + " password=" + DB_pass)
    cur = conn.cursor()

    cur.execute("select exists(select * from information_schema.tables where table_name=%s)",
                (DB_table,))
    if cur.fetchone()[0]:
        QMessageBox.information(None, "General Info", 'Database found - uploading')
    else:
        QMessageBox.information(None, "General Info", 'Creating database ' + DB_table)
        cur.execute(
            "CREATE TABLE " + DB_schema + "." + DB_table + "(imageid TEXT PRIMARY KEY, easting float, northing float, height real,omega real, phi real, kappa real, direction text, timeutc text, cameraid text, "
                                                           "coneid real, estacc real, height_eli text, timecet text, \"references\" text, producer text, level real, comment_co text, comment_gs text, status text, gsd text, geom geometry)")
        conn.commit()

    IDs = []
    # cur.execute('SELECT * from '+DB_table)
    # rows = cur.fetchall()
    # for row in rows:
    #    ii = row[0]
    #    IDs.append(ii)
    list = []
    coneid = []
    finallist = []
    ImageID = []
    East = []
    North = []
    Height = []
    Omega = []
    Phi = []
    Kappa = []
    Direction = []
    TimeUTC = []
    CameraID = []
    EstAcc = []
    Height_Eli = []
    TimeCET = []
    ReferenceS = []
    Producer = []
    Level = []
    Comment_co = []
    Comment_sdfe = []
    Status = []
    GSD = []
    IMupload = []
    IMreason = []
    DBY = 0
    DBN = 0
    DBOY = 0
    DBON = 0
    for feat in selection:
        # attrs = ft.attributes()
        ImageID.append(feat['ImageID'])
        East.append(feat['Easting'])
        North.append(feat['Northing'])
        Height.append(feat['Height'])
        Omega.append(feat['Omega'])
        Phi.append(feat['Phi'])
        Kappa.append(feat['Kappa'])
        Direction.append(feat['Direction'])
        TimeUTC.append(feat['TimeUTC'])
        CameraID.append(feat['CameraID'])
        EstAcc.append(feat['EstAcc'])
        Height_Eli.append(feat['Height_Eli'])
        TimeCET.append(feat['TimeCET'])
        ReferenceS.append(feat['ReferenceS'])
        Producer.append(feat['Producer'])
        Level.append(feat['Level'])
        Comment_co.append(feat['Comment_Co'])
        Comment_sdfe.append(feat['Comment_GS'])
        Status.append(feat['Status'])
        GSD.append(feat['GSD'])
        coneid.append(feat['ConeID'])
        geom = feat.geometry()
        Geometri = geom.asPolygon()
        list.append(Geometri)

    for ll in list:
        test = str(ll[0])
        test1 = test.replace("[", "")
        test2 = test1.replace("]", "")
        test3 = test2.replace(",", " ")
        test4 = test3.replace(")  (", "), (")
        test5 = test4.replace("(", "")
        test6 = test5.replace(")", "")
        finallist.append(test6)

    return finallist

def DB_overwrite():
    temp=100
    return temp