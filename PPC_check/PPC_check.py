# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PPC_check
                                 A QGIS plugin
 Tool for checking PPC files
                              -------------------
        begin                : 2016-03-08
        git sha              : $Format:%H$
        copyright            : (C) 2016 by www.sdfe.dk
        email                : anfla@sdfe.dk, mafal@sdfe.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
import ntpath
import psycopg2
import sqlite3
import urllib2
import time
from datetime import datetime
from processing.core.Processing import Processing
from processing.tools import *
from osgeo import gdal, osr
import re, os
# Initialize Qt resources from file resources.py
import resources, DBConnect
# Import the code for the dialog
from PPC_check_dialog import PPC_checkDialog, PPC_checkDialogII
import os.path

class PPC_check:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PPC_check_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PPC_checkDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SDFE-tools')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PPC_check')
        self.toolbar.setObjectName(u'PPC_check')
        #self.dlg.pushButton_Input.clicked.connect(self.showFileSelectDialogInput)

        self.ProjectLog,self.MainLog,self.PPC_GSD,self.Sun,self.Tilt,self.CamCal,self.ImageDir,self.DBImageDir,self.DBname,self.DBhost,self.DBport,self.DBuser,self.DBpass = self.readSettings

        #if self.CamCal == "-":
            #self.dlg.lineEditCamDir.setText(os.path.dirname(__file__)+"\\CameraCalibrations\\")
        #if self.ImageDir == "-":
        #    self.dlg.lineEditImageDir.setText("C:\Users\B020736\Documents\Test_Oblique_2017\Image_TIF")
        #if self.DBImageDir == "-":
        #    self.dlg.lineEditDBImageDir.setText("C:\Users\B020736\Documents\Test_GeoDK_2017\TIF_GeoDK")

        self.dlg.pushButton_InputPPC.clicked.connect(self.showFileSelectDialogInputPPC)
        self.dlg.radioButtonPPC_ob.toggled.connect(self.radio1_ob_clicked)
        self.dlg.radioButtonPPC_Nadir.toggled.connect(self.radio1_Nadir_clicked)
        QObject.connect(self.dlg.inShapeAPPC, SIGNAL("currentIndexChanged(QString)" ), self.checkA )

        self.dlg.checkBoxPic.setChecked(True)
        self.dlg.checkBoxGSD.setChecked(True)
        self.dlg.lineEditGSD.setText(self.PPC_GSD)
        self.dlg.checkBoxSun.setChecked(True)
        self.dlg.lineEditSUN.setText(self.Sun)
        self.dlg.checkBoxFile.setChecked(True)
        self.dlg.checkBoxFormat.setChecked(True)
        self.dlg.checkBoxTilt.setChecked(True)
        self.dlg.lineEditTilt.setText(self.Tilt)
        self.dlg.checkBoxRef.setChecked(True)
        self.dlg.lineEditRef.setText('ETRS89,UTM32N,DVR90')
        self.dlg.checkBoxVoids.setChecked(True)
        self.dlg.radioButtonPPC_Nadir.setChecked(True)

        self.pgr = PPC_checkDialogII()
        # add funcionallity to pushbutton
        #self.dlg.pushButton_run.clicked.connect(self.progress)


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PPC_check', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            #self.menu = QMenu( "&SDFE-tools", self.iface.mainWindow().menuBar() )
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/PPC_check/icon.png'
        #self.menu = QMenu( "&SDFE-tools", self.iface.mainWindow().menuBar() )
        #actions = self.iface.mainWindow().menuBar().actions()
        #lastAction = actions[-1]
        #self.iface.mainWindow().menuBar().insertMenu( lastAction, self.menu )
        #self.menu.add_action(self.action)
        self.add_action(
            icon_path,
            text=self.tr(u'Check PPC shp file'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PPC_check'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def showFileSelectDialogInputPPC(self):
       fname = QFileDialog.getExistingDirectory( None, 'Open camera calibration directory', os.path.dirname(__file__)+"\\CameraCalibrations\\")
       self.dlg.lineEditCamDir.setText(fname)

    def radio1_ob_clicked(self, enabled):
        if enabled:
            self.dlg.lineEditGSD.setText('0.10')
            self.dlg.lineEditSUN.setText('15')
            self.dlg.checkBoxVoids.setChecked(True)
    def radio1_Nadir_clicked(self,enabled):
        if enabled:
            self.dlg.lineEditGSD.setText('0.15')
            self.dlg.lineEditSUN.setText('25')
            self.dlg.checkBoxVoids.setChecked(False)

    def checkA( self ):
        inputFilNavnPPC = unicode( self.dlg.inShapeAPPC.currentText() )
        canvas = self.iface.mapCanvas()
        allLayers = canvas.layers()

        for i in allLayers:
            if(i.name() == inputFilNavnPPC):
                if i.selectedFeatureCount() != 0:
                    self.dlg.useSelectedAPPC.setCheckState( Qt.Checked )
                else:
                    self.dlg.useSelectedAPPC.setCheckState( Qt.Unchecked )


    def changed(self, inputLayer):
        changedLayer = self.dlg.getVectorLayerByNam(inputLayer)
        changedProvider = changedLayer.dataProvider()
        upperVal = changedProvider.featureCount()
        self.spnNumber.setMaximum(upperVal)

    @property
    def readSettings(self):
        settingsFile = os.path.dirname(__file__)+"\\settings.txt"
        with open(settingsFile) as openfileobject:
            for line in openfileobject:
                SplitLine = line.split(" ")
                if SplitLine[0] == "UserID:":
                    UserID = SplitLine[1].rstrip('\r\n')
                elif SplitLine[0] == "Project:":
                    Project = SplitLine[1].rstrip('\r\n')
                elif SplitLine[0] == "ProjectLog:":
                    ProjectLog = SplitLine[1].rstrip('\r\n')
                elif SplitLine[0] == "MainLog:":
                    MainLog = SplitLine[1].rstrip('\r\n')
                elif SplitLine[0] == "GSD:":
                    PPC_GSD = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "Sun:":
                    Sun = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "Tilt:":
                    Tilt = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "CamCal:":
                    CamCal = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "ImageDir:":
                    ImageDir = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "DBImageDir:":
                    DBImageDir = SplitLine[1].rstrip('\r\n')
                elif SplitLine[0] == "DB_n:":
                    DBname = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "DB_h:":
                    DBhost = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "DB_po:":
                    DBport = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "DB_u:":
                    DBuser = SplitLine[1].rstrip('\r\n')
                elif SplitLine [0] == "DB_pa:":
                    DBpass = SplitLine[1].rstrip('\r\n')
        return (ProjectLog,MainLog,PPC_GSD,Sun,Tilt,CamCal,ImageDir,DBImageDir,DBname,DBhost,DBport,DBuser,DBpass)

    def readCameras(self,camdir):
        caminfo=[]
        for camfile in os.listdir(camdir):
            if camfile.endswith(".cam"):
                with open(camdir+'\\'+camfile) as openfileobject:
                    try:
                        for line in openfileobject:
                            SplitLine = line.split(" ")
                            if SplitLine[0] == "CAM_ID:":
                                CAM_ID = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "PIXEL_SIZE:":
                                PIXEL_SIZE = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "PRINCIPAL_DISTANCE:":
                                PRINCIPAL_DISTANCE = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "PRINCIPAL_POINT_X:":
                                PRINCIPAL_POINT_X = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "PRINCIPAL_POINT_Y:":
                                PRINCIPAL_POINT_Y = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "SENSOR_AREA_WIDTH:":
                                SENSOR_AREA_WIDTH = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "SENSOR_AREA_WIDTH_PIX:":
                                SENSOR_AREA_WIDTH = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "SENSOR_AREA_HEIGHT:":
                                SENSOR_AREA_HEIGHT = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "SENSOR_AREA_HEIGHT_PIX:":
                                SENSOR_AREA_HEIGHT = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "ROTATION:":
                                ROTATION = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "CALIBRATIONDATE:":
                                CALIBRATIONDATE = SplitLine[1].rstrip('\r\n')
                            elif SplitLine[0] == "OWNER:":
                                OWNER = SplitLine[1].rstrip('\r\n')
                    except (RuntimeError, TypeError, NameError, IndexError):
                        QMessageBox.information(None, "General Error", "General runtime error - Check camfile: "+str(CAM_ID)+".cam")
                        return
                caminfo.append([CAM_ID,PIXEL_SIZE,PRINCIPAL_DISTANCE,PRINCIPAL_POINT_X,PRINCIPAL_POINT_Y,SENSOR_AREA_WIDTH,SENSOR_AREA_HEIGHT,ROTATION,CALIBRATIONDATE,OWNER])
            else:
                continue
        return caminfo


    def utmToLatLng(self, zone, easting, northing, northernHemisphere=True):
        import math
        if not northernHemisphere:
            northing = 10000000 - northing

        a = 6378137
        e = 0.081819191
        e1sq = 0.006739497
        k0 = 0.9996

        arc = northing / k0
        mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

        ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

        ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

        cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
        cc = 151 * math.pow(ei, 3) / 96
        cd = 1097 * math.pow(ei, 4) / 512
        phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

        n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

        r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
        fact1 = n0 * math.tan(phi1) / r0

        _a1 = 500000 - easting
        dd0 = _a1 / (n0 * k0)
        fact2 = dd0 * dd0 / 2

        t0 = math.pow(math.tan(phi1), 2)
        Q0 = e1sq * math.pow(math.cos(phi1), 2)
        fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

        fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

        lof1 = _a1 / (n0 * k0)
        lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
        lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
        _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
        _a3 = _a2 * 180 / math.pi

        latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

        if not northernHemisphere:
            latitude = -latitude

        longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

        if (zone > 29):
            longitude = longitude*(-1)

        return (latitude, longitude)

    def sunAngle(self,datotiden, lati, longi):
        import math
        import datetime
        datotiden = datotiden.replace('-',':')
        patterndatetime1 = re.compile("[0-9]{4}:[0-9]{2}:[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{0,3}")
        if  patterndatetime1.match(datotiden):
            DateTime = datetime.datetime.strptime(datotiden,'%Y:%m:%d %H:%M:%S.%f')
        else:
            DateTime = datetime.datetime.strptime(datotiden,'%Y:%m:%d %H:%M:%S')

        dayOfYear = DateTime.timetuple().tm_yday
        hour = DateTime.hour
        mins = DateTime.minute
        sec =  DateTime.second
        timeZone = 0
        #lat = 56
        #long = -12

        gamma = (2*math.pi/365)*((dayOfYear+1)+(hour-12)/24)
        eqtime = 229.18*(0.000075+0.001868*math.cos(gamma)-0.032077*math.sin(gamma)-0.014615*math.cos(2*gamma)-0.040849*math.sin(2*gamma))
        declin = 0.006918-(0.399912*math.cos(gamma))+ 0.070257*math.sin(gamma)-0.006758*math.cos(2*gamma)+0.000907*math.sin(2*gamma)-0.002697*math.cos(3*gamma)+0.00148*math.sin(3*gamma)
        tOffset = eqtime-4*longi+60*timeZone
        tst = hour*60+mins+sec/60+tOffset
        sh = (tst/4)-180
        zenit = math.degrees(math.acos(((math.sin(math.radians(lati))*math.sin(declin))+(math.cos(math.radians(lati))*math.cos(declin)*math.cos(math.radians(sh))))))
        sunVinkel = 90-zenit

        return sunVinkel

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        self.dlg.setWindowTitle(self.tr("Check PPC"))
        # populate layer list


        mapCanvas = self.iface.mapCanvas()
        lyrs = self.iface.legendInterface().layers()
        DB_list = ['ppc2017', 'footprint2017']
        lyr_list = []
        for layer in lyrs:
            lyr_list.append(layer.name())
        self.dlg.inShapeAPPC.clear()
        self.dlg.inShapeAPPC.addItems(lyr_list)

        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            import subprocess
            inputLayer = unicode(self.dlg.inShapeAPPC.currentText())
            WantedCamPath = str(self.dlg.lineEditCamDir.text())

            caminfo = self.readCameras(WantedCamPath)

            inputFilNavn = self.dlg.inShapeAPPC.currentText()

            canvas = self.iface.mapCanvas()
            allLayers = canvas.layers()

            try:
                count = 0
                for i in allLayers:
                    #QMessageBox.information(None, "status",i.name())
                    if(i.name() == inputFilNavn):
                        layer=i

                        # Check fileformat conformity
                        if self.dlg.checkBoxFile.isChecked():
                            n=0
                            features = layer.getFeatures()
                            f = features.next()
                            AttributesList = [c.name() for c in f.fields().toList()]
                            if self.dlg.radioButtonPPC_ob.isChecked():
                                PossibleValues = ['ImageID','Easting','Northing','Height','Omega','Phi','Kappa','Direction','TimeUTC','CameraID','ConeID','EstAcc','Height_Eli','TimeCET','ReferenceS','Producer','Level','Comment_Co','Comment_GS','Status','GSD']
                            elif self.dlg.radioButtonPPC_Nadir.isChecked():
                                PossibleValues = ['ImageID','Easting','Northing','Height','Omega','Phi','Kappa','TimeUTC','CameraID','Height_Eli','TimeCET','ReferenceS','Producer','Level','Comment_Co','Comment_GS','Status','GSD']

                            for s in PossibleValues:
                                if s in AttributesList:
                                    n = n + 1
                            ld1 = len(AttributesList)-n
                            ld2 = n-len(AttributesList)
                            if ld1 >= 0:
                                NameFailCount = 0
                                #QMessageBox.information(None, "status", "File conforms to SDFE standard!")
                            elif len(AttributesList) < n:
                                if self.dlg.radioButtonPPC_ob.isChecked():
                                    QMessageBox.information(None, "status", "Files is missing some attributes. \n Check that the following fields are pressent in the attributes table header: \n 'ImageID','Easting','Northing','Height','Omega','Phi','Kappa','Direction','TimeUTC','CameraID','ConeID','EstAcc','Height_Eli',\n'TimeCET','ReferenceS','Producer','Level','Comment_Co','Comment_GS','Status','GSD'" )
                                elif self.dlg.radioButtonPPC_Nadir.isChecked():
                                    QMessageBox.information(None, "status", "Files is missing some attributes. \n Check that the following fields are pressent in the attributes table header: \n 'ImageID','Easting','Northing','Height','Omega','Phi','Kappa','TimeUTC','CameraID','Height_Eli',\n'TimeCET','ReferenceS','Producer','Level','Comment_Co','Comment_GS','Status'")
                                return
                            else:
                                NameFailCount = len(ld1)
                                whatfailed = "The following attributes did not conrform to standard: \n"
                                for x in range(0, NameFailCount):
                                     whatfailed = whatfailed + "Value in File:\t \t" + ld2[x]  + "\n SDFE Standard:\t" + ld1[x] + "\n \n"
                                QMessageBox.information(None, "status", "File does not conforms to SDFE standard! PPC Check aborted \n \n" + whatfailed)
                                return

                        # create virtual layer
                        vl = QgsVectorLayer("Point", "PPC-check: "+str(inputFilNavn), "memory")
                        pr = vl.dataProvider()
                        commentCount = 0
                        GSDfailCount = 0
                        SUNfailCount = 0
                        TILTfailCount = 0
                        REFfailCount = 0
                        FeatFailCount = 0
                        #vl.startEditing()
                        # add fields
                        pr.addAttributes([ QgsField("ImageID", QVariant.String),
                                            QgsField("GSD",  QVariant.String),
                                            QgsField("SunAngle", QVariant.String),
                                            QgsField("SunCheck", QVariant.String),
                                            QgsField("Overlap", QVariant.String),
                                            QgsField("Tilt", QVariant.String),
                                            QgsField("RefSys", QVariant.String),
                                            QgsField("NameFormat", QVariant.String),
                                            QgsField("Orientation", QVariant.String)])

                        if self.dlg.useSelectedAPPC.isChecked():
                            selection = layer.selectedFeatures()
                        else:
                            selection = layer.getFeatures()
                        cc=0
                        for feat in selection:
                            cc+=1

                        if self.dlg.useSelectedAPPC.isChecked():
                            selection = layer.selectedFeatures()
                            QMessageBox.information(None, "status", "checking selected features")
                        else:
                            selection = layer.getFeatures()
                            QMessageBox.information(None, "status", "checking all features")

                        # Define features for name-format checker
                        FeatIIDFailCount = 0
                        FeatTimeFailCount = 0
                        FeatCamFailCount = 0
                        FeatOrientationFail = 0
                        kappacount = 0
                        fiveinarow = 0
                        nn=0
                        for feat in selection:
                            nn+=1
                            geom = feat.geometry().centroid()
                            Geometri = geom.asPoint()
                            ImageID = feat['ImageID']

                            # General checks
                            producent = str(feat['Producer'])
                            kommentar = str(feat['COMMENT_CO'])
                            Kamera = feat['CameraID']
                            fundet = False
                            for kam in caminfo:
                                if kam[0] == Kamera:
                                    CAM_ID = kam[0]
                                    PIXEL_SIZE = kam[1]
                                    PRINCIPAL_DISTANCE = kam[2]
                                    fundet = True
                            if fundet == False:
                                QMessageBox.information(None, "General Error", "Camera ["+Kamera+"] not found in calibration folder, exiting!")
                                return

                            if (len(kommentar)>4):
                            # if (kommentar != '' and kommentar!='NULL'):
                                commentCount = commentCount + 1

                            # Check GSD
                            GSDpass = 'Not validated'
                            if self.dlg.checkBoxGSD.isChecked():
                                try:
                                    Ele = float(feat['Height'])
                                    WantedGSD = float(self.dlg.lineEditGSD.text())
                                    calculatedGSD = ((float(Ele)*float(PIXEL_SIZE))/float(PRINCIPAL_DISTANCE)/1000)-0.01

                                    if WantedGSD<calculatedGSD:
                                        GSDpass = 'Failed'
                                        GSDfailCount = GSDfailCount + 1
                                    else:
                                        GSDpass = "OK"
                                except (RuntimeError, TypeError, NameError, ValueError):
                                    QMessageBox.information(None, "General Error", "Error in elevation format, exiting!")
                                    return

                            #check sun angle
                            SUNpass = 'Not validated'
                            solVinkelen = []
                            if (self.dlg.checkBoxSun.isChecked()):
                                try:
                                    Zon = 32
                                    posX = feat['Easting']
                                    posY = feat['Northing']
                                    datotiden = feat['TimeUTC'].replace('T',' ').replace('60','59')

                                    lati = self.utmToLatLng(Zon,posX,posY, True)[0]
                                    longi = self.utmToLatLng(Zon,posX,posY, True)[1]

                                    solVinkelen = self.sunAngle(datotiden,lati,longi)
                                    WantedSUN = float(self.dlg.lineEditSUN.text())

                                    if (solVinkelen<WantedSUN):
                                        SUNpass = 'Failed'
                                        SUNfailCount = SUNfailCount+1
                                    else:
                                        SUNpass = 'OK'
                                except (RuntimeError, TypeError, NameError, ValueError):
                                    QMessageBox.information(None, "General Error", "Error in Time format. \n  Time read: "+feat['TimeUTC']+"\n  Should be: YYYY-MM-DDTHH:MM:SS.SSS \n \nExiting!")
                                    return

                            #check name format
                            NameFormat = 'Not Checked'
                            Orientation = ''
                            if (self.dlg.checkBoxFormat.isChecked()):
                                try:
                                    patternImageIDGeoDK = re.compile("\w{0,1}[0-9]{4}_[0-9]{2}_[0-9]{2}_\d+_[0-9]{4}")
                                    patternImageIDoblique = re.compile("[0-9]{4}_[0-9]{2}_[0-9]{2}_\d+_[0-9]{4}_[0-9]{8}")
                                    patternTime = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.{0,1}[0-9]{0,3}")
                                    patternKappa = re.compile("-?[\d]+.[0-9]{3}[0]")

                                    kappa = feat['Kappa']
                                    Time1 = feat['TimeUTC']
                                    Time2 = feat['TimeCET']
                                    ImageID = feat['ImageID']
                                    if self.dlg.radioButtonPPC_Nadir.isChecked():
                                        patternImageID=patternImageIDGeoDK
                                    elif self.dlg.radioButtonPPC_ob.isChecked():
                                        patternImageID=patternImageIDoblique
                                    if self.dlg.checkBoxPic.isChecked():
                                        if patternImageID.match(ImageID):
                                            FeatIIDFailCount = 0
                                            NameFormat1 = '  ImageID-OK  '
                                        else:
                                            FeatIIDFailCount = FeatIIDFailCount+1
                                            NameFormat1 = '  ImageID-Fail  '
                                    else:
                                        NameFormat1 = '  ImageID-not checked  '
                                    if patternTime.match(str(Time1)):
                                        FeatTimeFailCount = 0
                                        if patternTime.match(str(Time2)):
                                            FeatTimeFailCount = 0
                                            NameFormat2 = '  TimeCET,TimeUTC-OK  '
                                        else:
                                            FeatTimeFailCount = FeatTimeFailCount+1
                                            NameFormat2 = '  TimeCET-Fail,TimeUTC-OK  '
                                    else:
                                        if patternTime.match(Time2):
                                            FeatTimeFailCount = FeatTimeFailCount+1
                                            NameFormat2 = '  TimeCET-OK,TimeUTC-Fail  '
                                        else:
                                            FeatTimeFailCount = FeatTimeFailCount+2
                                            NameFormat2 = '  TimeCET,TimeUTC-Fail  '

                                    if CAM_ID == feat['CameraID']:
                                        FeatCamFailCount = 0
                                        NameFormat3 = '  CameraID-OK  '
                                    else:
                                        FeatCamFailCount = FeatCamFailCount+1
                                        NameFormat3 = '  CameraID-Fail  '

                                    if kappacount > 5:
                                        fiveinarow = 1
                                    else: pass

                                    if ((str(kappa) == "NULL") or (str(kappa) == "")):
                                        #QMessageBox.information(None, "General Error", "1")
                                        NameFormat4 = ' '
                                        kappacount = 0
                                        pass
                                    elif len(str(kappa)) >= 9:
                                        kappa = "%.4f" % float(kappa)
                                        if patternKappa.match(kappa):
                                            FeatOrientationFail = FeatOrientationFail+1
                                            kappacount = kappacount + 1
                                            NameFormat4 = '  Kappa - suspicious length:  '
                                        else:
                                            NameFormat4 = 'Kappa '
                                            kappacount = 0
                                    else:
                                        kappa = "%.4f" % float(kappa)
                                        if patternKappa.match(kappa):
                                            FeatOrientationFail = FeatOrientationFail+1
                                            kappacount = kappacount +1
                                            NameFormat4 = '  Kappa - maybe truncated:  '
                                        else:
                                            NameFormat4 = 'Kappa '
                                            kappacount = 0


                                except (RuntimeError, TypeError, NameError, ValueError):
                                    QMessageBox.information(None, "General Error", "Error in name format!")
                                    return
                                FeatFailCount = FeatIIDFailCount + FeatTimeFailCount + FeatCamFailCount
                                NameFormat = NameFormat1+NameFormat2 + NameFormat3
                                Orientation = NameFormat4

                            #Check Overlap
                            #if (self.dlg.checkBoxOverlap.isChecked()):
                                #doo something
                            #    OLAPfailCount = 0

                            #Check Tilt angles
                            TILTpass = 'Not validated'
                            if (self.dlg.checkBoxTilt.isChecked()):
                                if (self.dlg.radioButtonPPC_ob.isChecked()):
                                    Dir = str(feat['Direction'])
                                    if Dir=="T":
                                        try:
                                            Omega = feat['Omega']
                                            Phi = feat['Phi']
                                            MaxAcceptedTilt = float(self.dlg.lineEditTilt.text())

                                            Level = int(feat['Level'])
                                            MaxAcceptedTilt = float(self.dlg.lineEditTilt.text())
                                            if ((str(Omega) == "NULL") or (str(Phi)=="NULL")):
                                                TILTpass = 'no info'
                                                if ( Level > 1):
                                                    TILTfailCount = TILTfailCount+1

                                            elif ((Omega > MaxAcceptedTilt) or (Phi > MaxAcceptedTilt)):
                                                TILTpass = 'Failed'
                                                TILTfailCount = TILTfailCount+1
                                            else:
                                                TILTpass = 'Nadir - OK'
                                        except (RuntimeError, TypeError, NameError, ValueError):
                                            QMessageBox.information(None, "General Error", "Error in tilt angles, exiting!")
                                            return
                                    else:
                                        pass
                                elif (self.dlg.radioButtonPPC_Nadir.isChecked()):
                                    try:
                                        Omega = feat['Omega']
                                        Phi = feat['Phi']
                                        MaxAcceptedTilt = float(self.dlg.lineEditTilt.text())

                                        Level = int(feat['Level'])
                                        MaxAcceptedTilt = float(self.dlg.lineEditTilt.text())
                                        if ((str(Omega) == "NULL") or (str(Phi) == "NULL")):
                                            TILTpass = 'no info'
                                            if (Level > 1):
                                                TILTfailCount = TILTfailCount + 1

                                        elif ((Omega > MaxAcceptedTilt) or (Phi > MaxAcceptedTilt)):
                                            TILTpass = 'Failed'
                                            TILTfailCount = TILTfailCount + 1
                                        else:
                                            TILTpass = 'OK'
                                    except (RuntimeError, TypeError, NameError, ValueError):
                                        QMessageBox.information(None, "General Error", "Error in tilt angles, exiting!")
                                        return

                            #Check Reference system
                            REFpass = 'Not validated'
                            if (self.dlg.checkBoxRef.isChecked()):
                                try:
                                    RefS = feat['ReferenceS']
                                    WantedREF1 = self.dlg.lineEditRef.text()
                                    if (RefS != WantedREF1):
                                        REFpass = 'Failed'
                                        REFfailCount = REFfailCount+1
                                    else:
                                        REFpass = 'OK'
                                except (RuntimeError, TypeError, NameError, ValueError):
                                    QMessageBox.information(None, "General Error", "Error in Reference format, exiting!")
                                    return

                            # Check for voids
                            if (self.dlg.checkBoxVoids.isChecked()):
                                if self.dlg.radioButtonPPC_Nadir.isChecked():
                                    QMessageBox.information(None, "General Error", "Void-check option is only for Oblique!")
                                    break
                                elif self.dlg.radioButtonPPC_ob.isChecked():
                                    if nn==cc:
                                        fname=inputLayer
                                        try:
                                            fname
                                        except NameError:
                                            self.dlg.close()
                                        else:
                                            pass
                                        localpath = os.getcwd()
                                        if os.path.exists(localpath + '\\dissolved_lyr.shp'):
                                            try:
                                                QgsMapLayerRegistry.instance().removeMapLayer(lyr1)
                                            except:
                                                pass
                                            QgsVectorFileWriter.deleteShapeFile(localpath + '\\dissolved_lyr.shp')
                                        if os.path.exists(localpath + '\\err_lyr.shp'):
                                            try:
                                                QgsMapLayerRegistry.instance().removeMapLayer(err_layer)
                                            except:
                                                pass
                                            QgsVectorFileWriter.deleteShapeFile(localpath + '\\err_lyr.shp')

                                        lyr = QgsVectorLayer(fname, 'Footprints', 'ogr')
                                        general.runalg("qgis:dissolve", lyr, "False", "Direction",
                                                       localpath + '\\dissolved_lyr.shp')
                                        lyr1 = QgsVectorLayer(localpath + '\\dissolved_lyr.shp', 'dissolved_layer', 'ogr')
                                        landuse = {"N": ("yellow", "North"), "S": ("darkcyan", "South"),
                                                   "E": ("green", "East"),
                                                   "W": ("blue", "West"), "T": ("red", "Nadir")}

                                        categories = []
                                        for NSEW, (color, label) in landuse.items():
                                            sym = QgsSymbolV2.defaultSymbol(lyr1.geometryType())
                                            sym.setColor(QColor(color))
                                            category = QgsRendererCategoryV2(NSEW, sym, label)
                                            categories.append(category)

                                        field = "Direction"
                                        renderer = QgsCategorizedSymbolRendererV2(field, categories)
                                        lyr1.setRendererV2(renderer)
                                        crs = lyr1.crs()
                                        crs.createFromId(25832)
                                        lyr1.setCrs(crs)
                                        QgsMapLayerRegistry.instance().addMapLayer(lyr1)
                                        #            crs = self.utils.iface.activeLayer().crs().authid()
                                        features = lyr1.getFeatures()
                                        layer1 = QgsVectorLayer('Polygon', 'poly1', "memory")
                                        layer2 = QgsVectorLayer('Polygon', 'poly2', "memory")
                                        pr1 = layer1.dataProvider()
                                        pr2 = layer2.dataProvider()
                                        poly1 = QgsFeature()
                                        poly2 = QgsFeature()
                                        for f in features:
                                            vertices = f.geometry().asPolygon()
                                            dir = f.attribute("Direction")
                                            n = len(vertices)
                                            if n == 2:
                                                poly1.setGeometry(QgsGeometry.fromPolygon([vertices[0]]))
                                                poly2.setGeometry(QgsGeometry.fromPolygon([vertices[1]]))
                                                pr1.addFeatures([poly1])
                                                pr2.addFeatures([poly2])
                                                layer1.updateExtents()
                                                layer2.updateExtents()
                                                QgsMapLayerRegistry.instance().addMapLayers([layer2])

                                        general.runalg('qgis:addfieldtoattributestable', layer2, 'Direction', 2, 10, 7,
                                                       'err_lyr.shp')
                                        err_layer = QgsVectorLayer('C:\\OSGeo4W64\\bin\\err_lyr.shp', 'Error_layer', 'ogr')
                                        # --------------------------------------------------------------------------
                                        # only applicable for test case footprint file should be in crs 25832
                                        # crs = err_layer.crs()
                                        # crs.createFromId(4326)
                                        # err_layer.setCrs(crs)
                                        #
                                        # ------------------------------------------------------------------------------
                                        QgsMapLayerRegistry.instance().addMapLayers([err_layer])
                                        QgsMapLayerRegistry.instance().removeMapLayer(layer2)

                                        num = 0
                                        features = lyr1.getFeatures()
                                        for f in features:
                                            vertices = f.geometry().asPolygon()
                                            dir = f.attribute("Direction")
                                            n = len(vertices)
                                            if n == 2:
                                                num = num + 1
                                                # print dir,n,num
                                                err_layer.startEditing()
                                                err_layer.changeAttributeValue((num - 1), 0, dir)
                                                err_layer.commitChanges()
                                        rapp = "<center>Check Complete:<center>\n" + "\n Errors, if there are any, are in the \"Error_layer\"\n with their layer orientation in the attribute table\n"

                                        QMessageBox.information(self.iface.mainWindow(), 'Footprint_Void_Check', rapp)


                            # add a feature
                            newfeat = QgsFeature()
                            newfeat.setGeometry(QgsGeometry.fromPoint(Geometri))
                            try:
                                newfeat.setAttributes([ImageID, GSDpass, solVinkelen, SUNpass,"",TILTpass,REFpass,NameFormat,Orientation+" : "+kappa])
                            except (RuntimeError, TypeError, NameError, ValueError):
                                QMessageBox.information(None, "General Error", "PPC Format errors found, exiting!")
                                return

                            pr.addFeatures([newfeat])

                        # update layer's extent when new features have been added
                        # because change of extent in provider is not propagated to the layer
                        vl.updateExtents()
                        vl.updateFields()
                        QgsMapLayerRegistry.instance().addMapLayer(vl)

                        rapporten = "Check of: \n"+ inputFilNavn +"\n \nThere was found: \n"
                        if (self.dlg.checkBoxGSD.isChecked()):
                            rapporten = rapporten + str(GSDfailCount) + " GSD errors, \n"
                        else:
                            rapporten = rapporten + "GSD not checked \n"

                        if (self.dlg.checkBoxSun.isChecked()):
                            rapporten = rapporten + str(SUNfailCount) + " sun angle errors \n"
                        else:
                            rapporten = rapporten + "sun angle not checked \n"

                        #if (self.dlg.checkBoxOverlap.isChecked()):
                        #    rapporten = rapporten + "overlap check not available \n"
                        #else:
                        #    rapporten = rapporten + "overlap check not available \n"

                        if (self.dlg.checkBoxTilt.isChecked()):
                            rapporten = rapporten + str(TILTfailCount) + " tilt angle errors \n"
                        else:
                            rapporten = rapporten + "tilt angle not checked \n"

                        if (self.dlg.checkBoxRef.isChecked()):
                            rapporten = rapporten + str(REFfailCount) + " reference errors \n"
                        else:
                            rapporten = rapporten + "reference system not checked \n"

                        if (self.dlg.checkBoxFormat.isChecked()):
                            rapporten = rapporten + str(FeatFailCount) + " name format errors \n"
                        else:
                            rapporten = rapporten + "name format not checked \n"

                        if (self.dlg.checkBoxFormat.isChecked()):
                            if fiveinarow == 1:
                                rapporten = rapporten + str(FeatOrientationFail) + " suspect orientation formats \n OBS - 5 suspect kappa formats in a row \n"
                            else:
                                rapporten = rapporten + str(FeatOrientationFail) + " suspect orientation formats \n"
                        else:
                            rapporten = rapporten + "name format not checked \n"

                        rapporten = rapporten + str(commentCount) +" comments from " + producent

                        if GSDfailCount+SUNfailCount+TILTfailCount+REFfailCount+FeatFailCount == 0:
                            QMessageBox.information(self.iface.mainWindow(),'PPC check',rapporten)
                        else:
                            QMessageBox.critical(self.iface.mainWindow(),'PPC check',rapporten)
                        self.dlg.close()
                        return
            except (RuntimeError, TypeError, NameError): #, ValueError): #
                QMessageBox.information(None, "General Error", "General file error V2.1, please check that you have choosen the correct PPC file")
                return
