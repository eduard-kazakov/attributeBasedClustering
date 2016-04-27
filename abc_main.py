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
from PyQt4.QtGui import QApplication

from ui import abc_main_ui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QVariant
import abc_lib
from qgis.core import *
from qgis.core import QgsMapLayerRegistry
import resources
import numpy as np


class ABCMainDlg(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = abc_main_ui.Ui_Dialog()
        self.ui.setupUi(self)

        # Button's handlers
        self.connect(self.ui.runButton, QtCore.SIGNAL("clicked()"), self.run)
        self.connect(self.ui.cancelButton, QtCore.SIGNAL("clicked()"), self.cancel)
        self.connect(self.ui.addFieldButton, QtCore.SIGNAL("clicked()"), self.addField)
        self.connect(self.ui.deleteSelectedButton, QtCore.SIGNAL("clicked()"), self.deleteSelectedFields)
        self.connect(self.ui.deleteAllButton, QtCore.SIGNAL("clicked()"), self.deleteAllFields)

        self.connect(self.ui.vectorLayerComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.layerChanged)

        self.activateInterface()

        # Fill vector layers combobox
        vectorLayers = [layer.name() for layer in QgsMapLayerRegistry.instance().mapLayers().values() if
                          (layer.type() == QgsMapLayer.VectorLayer)]
        self.ui.vectorLayerComboBox.addItems(vectorLayers)




    ### INTERFACE MANIPULATIONS
    def checkFieldInTable (self, fieldName):
        allRows = self.ui.fieldsTable.rowCount()
        for row in xrange(0,allRows):
            currentFieldName = self.ui.fieldsTable.item(row,0).text()
            if fieldName == currentFieldName:
                return True
        return False

    def checkIfTableIsCorrect(self):
        allRows = self.ui.fieldsTable.rowCount()
        layerName = self.ui.vectorLayerComboBox.currentText()
        layer = abc_lib.getLayerByName(layerName)
        fieldNames = abc_lib.getAttributesListOfVectorLayer(layer)
        for row in xrange(0,allRows):
            currentFieldName = self.ui.fieldsTable.item(row,0).text()
            if currentFieldName not in fieldNames:
                return False
            try:
                float(self.ui.fieldsTable.item(row,1).text())
            except:
                return False
        return True


    def activateInterface(self):
        self.ui.progressBar.hide()
        self.ui.runButton.setEnabled(True)

    def deactivateInterface(self):
        self.ui.progressBar.show()
        self.ui.runButton.setDisabled(True)

    def layerChanged(self):
        userLayer = abc_lib.getLayerByName(self.ui.vectorLayerComboBox.currentText())
        layerFields = abc_lib.getAttributesListOfVectorLayer(userLayer,['Integer', 'Real'])
        self.ui.fieldsComboBox.clear()
        self.ui.fieldsComboBox.addItems(layerFields)

    def addField(self):
        fieldName = self.ui.fieldsComboBox.currentText()
        if not fieldName:
            QtGui.QMessageBox.critical(None, "Error", 'No field specified!')
            return

        if not self.checkFieldInTable(fieldName):
            self.ui.fieldsTable.setRowCount(self.ui.fieldsTable.rowCount()+1)
            self.ui.fieldsTable.setItem(self.ui.fieldsTable.rowCount()-1, 0, QtGui.QTableWidgetItem(fieldName))
            self.ui.fieldsTable.setItem(self.ui.fieldsTable.rowCount()-1, 1, QtGui.QTableWidgetItem('1.0'))

    def deleteSelectedFields(self):
        rows = sorted(set(index.row() for index in self.ui.fieldsTable.selectedIndexes()))
        for row in rows:
            self.ui.fieldsTable.removeRow(row)

    def deleteAllFields(self):
        allRows = self.ui.fieldsTable.rowCount()
        for row in xrange(0,allRows):
            self.ui.fieldsTable.removeRow(row)

    # Main function - run process after "Run" button is pressed
    def run(self):
        if not self.ui.vectorLayerComboBox.currentText():
            QtGui.QMessageBox.critical(None, "Error", 'No layer specified!')
            return

        if not self.ui.fieldsTable.rowCount():
            QtGui.QMessageBox.critical(None, "Error", 'No attributes specified!')
            return

        if not self.checkIfTableIsCorrect():
            QtGui.QMessageBox.critical(None, "Error", 'Table is incorrect! Check fields and weights')
            return

        if not self.ui.outputFieldNameLine.text():
            QtGui.QMessageBox.critical(None, "Error", 'No output field name specified!')
            return

        vectorLayer = abc_lib.getLayerByName(self.ui.vectorLayerComboBox.currentText())
        attributesList = []
        allRows = self.ui.fieldsTable.rowCount()
        for row in xrange(0,allRows):
            attributesList.append([self.ui.fieldsTable.item(row,0).text(),float(self.ui.fieldsTable.item(row,1).text())])

        normalize = self.ui.checkBox.isChecked()
        clusterNumber = int(self.ui.numberOfClustersSpinBox.text())
        outputFieldName = self.ui.outputFieldNameLine.text()

        # Do work
        if self.ui.clusteringMethodComboBox.currentIndex() == 1:
            self.deactivateInterface()
            QApplication.processEvents()
            try:
                abc_lib.hierarchicalClustering(vectorLayer, attributesList, normalize, clusterNumber, outputFieldName)
            except:
                self.activateInterface()
                QtGui.QMessageBox.critical(None, "Error", 'Problems during clustering...')
                return

            self.activateInterface()
            QtGui.QMessageBox.about(None, "Success", "Done!")

        if self.ui.clusteringMethodComboBox.currentIndex() == 0:
            self.deactivateInterface()
            QApplication.processEvents()
            try:
                abc_lib.kmeans_clustering(vectorLayer, attributesList, normalize, clusterNumber, outputFieldName)
            except:
                self.activateInterface()
                QtGui.QMessageBox.critical(None, "Error", 'Problems during clustering...')
                return

            self.activateInterface()
            QtGui.QMessageBox.about(None, "Success", "Done!")

    # Close window by pressing "Cancel" button
    def cancel(self):
        self.close()