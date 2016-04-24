# -*- coding: utf-8 -*-
"""
/***************************************************************************
Atrribute based clustering
                                 A QGIS plugin
Plugin produces clustering for features of vector layer based on unlimited number of attributes using hierarchical or k-means algorithms.
Hierarchical algorithm is native, k-means requieres scipy. You can define weight for every attribute, if hierarchical clustering used.

                              -------------------
        begin                : 2016-04-23
        copyright            : (C) 2016 by Eduard Kazakov
        email                : silenteddie@gmail.com
        homepage             : http://ekazakov.info
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from abc_main import ABCMainDlg

import os

class ABC:

    def __init__(self,iface):
        self.iface=iface
        self.dlg = ABCMainDlg()

    def initGui(self):

        dirPath = os.path.dirname(os.path.abspath(__file__))
        self.action = QAction(u"Attribute based clustering", self.iface.mainWindow())
        self.action.setIcon(QIcon(dirPath + "/icon.png"))
        self.iface.addPluginToVectorMenu(u"Attribute based clustering",self.action)
        self.action.setStatusTip(u"Attribute based clustering")
        self.iface.addVectorToolBarIcon(self.action)
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)


    def unload(self):
        self.iface.removeVectorToolBarIcon(self.action)
        self.iface.removePluginVectorMenu(u"Attribute based clustering",self.action)

    def run(self):
        self.MDCFeaturesDlg = ABCMainDlg()
        self.MDCFeaturesDlg.show()
