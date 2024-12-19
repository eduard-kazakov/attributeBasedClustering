# -*- coding: utf-8 -*-
"""
Attribute based clustering: QGIS Plugin

https://github.com/eduard-kazakov/attributeBasedClustering

Eduard Kazakov | ee.kazakov@gmail.com
"""

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from .processing.provider import AttributeBasedClusteringProvider
from qgis.core import QgsApplication

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .attribute_based_clustering_dialog import AttributeBasedClusteringDialog
import os.path

class AttributeBasedClustering:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AttributeBasedClustering_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&Attribute based clustering')

        self.first_start = None

        self.provider = None


    def tr(self, message):
        return QCoreApplication.translate('AttributeBasedClustering', message)

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
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):

        icon_path = ':/plugins/attribute_based_clustering/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Attribute based clustering'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

        self.provider = AttributeBasedClusteringProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)


    def unload(self):
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Attribute based clustering'),
                action)
            self.iface.removeToolBarIcon(action)

        QgsApplication.processingRegistry().removeProvider(self.provider)


    def run(self):
        if self.first_start == True:
            self.first_start = False
            self.dlg = AttributeBasedClusteringDialog()

        self.dlg.show()
        result = self.dlg.exec_()
