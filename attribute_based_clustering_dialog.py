# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 Attribute based clustering for vector layers by numeric attributes using hierarchical or k-means algorithms (known and unknown number of clusters supported).
                             -------------------
        begin                : 2019-01-01
        copyright            : (C) 2019 by Eduard Kazakov
        email                : silenteddie@gmail.com
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

import os
import math
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QVariant, Qt
from qgis.core import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attribute_based_clustering_dialog_base.ui'))

class AttributeBasedClusteringDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(AttributeBasedClusteringDialog, self).__init__(parent)
        self.setupUi(self)

        # UI Preparation
        self.clusteringThresholdLine.setDisabled(True)
        self.linkageMethodComboBox.setDisabled(True)
        self.vectorLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.fieldsComboBox.setLayer(self.vectorLayerComboBox.currentLayer())
        self.fieldsComboBox.setFilters(QgsFieldProxyModel.Numeric)
        self.progressBar.setVisible(False)

        # Buttons
        self.vectorLayerComboBox.currentIndexChanged.connect(self.layerChanged)
        self.clusteringMethodComboBox.currentIndexChanged.connect(self.methodChanged)

        self.addFieldButton.clicked.connect(self.addField)
        self.deleteSelectedButton.clicked.connect(self.deleteSelectedFields)
        self.deleteAllButton.clicked.connect(self.deleteAllFields)
        self.runButton.clicked.connect(self.run)
        self.cancelButton.clicked.connect(self.cancel)

    def layerChanged(self):
        self.deleteAllFields()
        self.fieldsComboBox.setLayer(self.vectorLayerComboBox.currentLayer())
        self.fieldsComboBox.setFilters(QgsFieldProxyModel.Numeric)

    def methodChanged(self):
        if self.clusteringMethodComboBox.currentIndex() == 0:
            self.clusteringThresholdLine.setDisabled(True)
            self.linkageMethodComboBox.setDisabled(True)
            self.numberOfClustersSpinBox.setEnabled(True)
        if self.clusteringMethodComboBox.currentIndex() == 1:
            self.clusteringThresholdLine.setDisabled(True)
            self.linkageMethodComboBox.setDisabled(True)
            self.numberOfClustersSpinBox.setEnabled(True)
        if self.clusteringMethodComboBox.currentIndex() == 2:
            self.clusteringThresholdLine.setEnabled(True)
            self.linkageMethodComboBox.setEnabled(True)
            self.numberOfClustersSpinBox.setDisabled(True)


    def checkIfTableIsCorrect(self):
        allRows = self.fieldsTable.rowCount()
        layerName = self.vectorLayerComboBox.currentText()

        for row in range(0,allRows):
            try:
                float(self.fieldsTable.item(row,1).text())
            except:
                return False
        return True

    def checkFieldInTable (self, fieldName):
        allRows = self.fieldsTable.rowCount()
        for row in range(0,allRows):
            currentFieldName = self.fieldsTable.item(row,0).text()
            if fieldName == currentFieldName:
                return True
        return False

    def addField(self):
        fieldName = self.fieldsComboBox.currentText()
        if not fieldName:
            QtWidgets.QMessageBox.critical(None, "Error", 'No field specified!')
            return

        if not self.checkFieldInTable(fieldName):
            self.fieldsTable.setRowCount(self.fieldsTable.rowCount() + 1)
            self.fieldsTable.setItem(self.fieldsTable.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(fieldName))
            self.fieldsTable.setItem(self.fieldsTable.rowCount() - 1, 1, QtWidgets.QTableWidgetItem('1.0'))

    def deleteSelectedFields(self):
        rows = sorted(set(index.row() for index in self.fieldsTable.selectedIndexes()))
        for row in rows:
            self.fieldsTable.removeRow(row)

    def deleteAllFields(self):
        allRows = self.fieldsTable.rowCount()
        for row in reversed(range(0, allRows+1)):
            self.fieldsTable.removeRow(row)

    def activateInterface(self):
        self.progressBar.hide()
        self.runButton.setEnabled(True)

    def deactivateInterface(self):
        self.progressBar.show()
        self.runButton.setDisabled(True)

    # Main function - run process after "Run" button is pressed
    def run(self):
        if not self.vectorLayerComboBox.currentText():
            QtWidgets.QMessageBox.critical(None, "Error", 'No layer specified!')
            return

        if not self.fieldsTable.rowCount():
            QtWidgets.QMessageBox.critical(None, "Error", 'No attributes specified!')
            return

        if not self.checkIfTableIsCorrect():
            QtWidgets.QMessageBox.critical(None, "Error", 'Table is incorrect! Check fields and weights')
            return

        if not self.outputFieldNameLine.text():
            QtWidgets.QMessageBox.critical(None, "Error", 'No output field name specified!')
            return

        if self.clusteringMethodComboBox.currentIndex() == 2:
            try:
                clustering_threshold = float(self.clusteringThresholdLine.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Threshold must be float! %s' % str(e))
                return

        vectorLayer = self.vectorLayerComboBox.currentLayer()
        normalize = self.checkBox.isChecked()
        clusterNumber = int(self.numberOfClustersSpinBox.text())
        linkageMethod = self.linkageMethodComboBox.currentText()
        outputFieldName = self.outputFieldNameLine.text()

        attributesList = []
        allRows = self.fieldsTable.rowCount()
        for row in range(0, allRows):
            attributesList.append([self.fieldsTable.item(row, 0).text(), float(self.fieldsTable.item(row, 1).text())])

        ### Do work

        if self.clusteringMethodComboBox.currentIndex() == 0:
           self.deactivateInterface()
           QApplication.processEvents()
           try:
               self.kmeansClustering(vectorLayer, attributesList, normalize, clusterNumber, outputFieldName)
           except Exception as e:
               self.activateInterface()
               QtWidgets.QMessageBox.critical(None, "Error", 'Problems during clustering... %s' % str(e))
               return

           self.activateInterface()
           QtWidgets.QMessageBox.about(None, "Success", "Done!")

        if self.clusteringMethodComboBox.currentIndex() == 1:
            self.deactivateInterface()
            QApplication.processEvents()
            try:
                self.hierarchicalClustering(vectorLayer, attributesList, normalize, clusterNumber,
                                               outputFieldName)
            except Exception as e:
                self.activateInterface()
                QtWidgets.QMessageBox.critical(None, "Error", 'Problems during clustering... %s' % str(e))
                return

            self.activateInterface()
            QtWidgets.QMessageBox.about(None, "Success", "Done!")

        if self.clusteringMethodComboBox.currentIndex() == 2:
            self.deactivateInterface()
            QApplication.processEvents()
            try:
                self.hierarchicalClusteringScipy(vectorLayer, attributesList, normalize, clustering_threshold, linkageMethod,
                                               outputFieldName)
            except Exception as e:
                self.activateInterface()
                QtWidgets.QMessageBox.critical(None, "Error", 'Problems during clustering... %s' % str(e))
                return

            self.activateInterface()
            QtWidgets.QMessageBox.about(None, "Success", "Done!")


    def cancel(self):
        self.close()

    # ABC Lib

    # return list of names of layer's fields. Second parameter can contain types of needed fields
    # e.g. ['Integer','Real']
    def getAttributesListOfVectorLayer(self, layer, types=None):
        names = []

        for field in layer.pendingFields():
            if not types:
                names.append(field.name())
            else:
                if str(field.typeName()) in types:
                    names.append(field.name())

        return names

    # calculates simple distance in n-dimensions
    def calculateDistance(self, a, b, weights):
        sum_sqr = 0
        k = 0

        for i, j in zip(a, b):
            sum_sqr += weights[k] * ((float(i) - float(j)) ** 2)
            k += 1
        distance = math.sqrt(sum_sqr)
        return distance

    # get average between two n-dimensional points
    def getAverageOfTwo(self, a, b):
        newObject = []
        i = 0
        while i < len(a):
            newObject.append((a[i] + b[i]) / 2.0)
            i += 1
        return newObject

    # Performs hierarchical clustering. Updates vector layer field.
    def hierarchicalClustering(self, vectorLayer, attributesList, normalize, clusterNumber, outputFieldName):
        weights = []
        # weights array
        for attribute in attributesList:
            weights.append(attribute[1])

        fullObjectsList = []
        clusterObjectList = []
        features = vectorLayer.getFeatures()

        # create full list with all characteristics
        for feature in features:
            fullObjectsList.append([])
            for attribute in attributesList:
                if feature[attribute[0]]:
                    fullObjectsList[len(fullObjectsList) - 1].append(feature[attribute[0]])
                else:
                    fullObjectsList[len(fullObjectsList) - 1].append(0)
            clusterObjectList.append([feature.id()])

        # NORMALIZING (if needed)
        if normalize:
            i = 0
            maxValues = []
            while i < len(attributesList):
                maxValues.append(max(item[i] for item in fullObjectsList))
                i += 1

            j = 0
            while j < len(fullObjectsList):
                i = 0
                while i < len(fullObjectsList[j]):
                    fullObjectsList[j][i] = (fullObjectsList[j][i] * 1.0) / (maxValues[i] * 1.0)
                    i += 1
                j += 1

        # GO CLUSTERING
        currentClusterNum = len(fullObjectsList)
        while currentClusterNum > clusterNumber:
            # Distance matrix
            distanceMatrix = []
            i = 0
            min = None
            min_i = 0
            min_j = 0
            while i < currentClusterNum:
                distanceMatrix.append([])
                j = 0
                while j < currentClusterNum:
                    if j >= i:
                        distanceMatrix[i].append(0.0)
                        j += 1
                        continue
                    currentDistance = self.calculateDistance(fullObjectsList[j], fullObjectsList[i], weights)
                    if (min == None) and (i != j):
                        min = currentDistance
                        min_i = i
                        min_j = j

                    if (currentDistance < min) and (i != j):
                        min = currentDistance
                        min_i = i
                        min_j = j

                    distanceMatrix[i].append(round(currentDistance, 2))
                    j += 1

                i += 1

            # split two objects into one
            fullObjectsList[min_i] = self.getAverageOfTwo(fullObjectsList[min_i], fullObjectsList[min_j])
            del fullObjectsList[min_j]

            # updating array with clusters id
            k = 0
            while k < len(clusterObjectList[min_j]):
                clusterObjectList[min_i].append(clusterObjectList[min_j][k])
                k += 1
            del clusterObjectList[min_j]

            currentClusterNum -= 1

        # Working with layer
        vectorLayerDataProvider = vectorLayer.dataProvider()

        # Create field of not exist
        if vectorLayer.fields().indexFromName(outputFieldName) == -1:
            vectorLayerDataProvider.addAttributes([QgsField(outputFieldName, QVariant.Int)])

        vectorLayer.updateFields()
        vectorLayer.startEditing()
        attrIdx = vectorLayer.fields().indexFromName(outputFieldName)
        features = vectorLayer.getFeatures()

        for feature in features:
            i = 0
            for idList in clusterObjectList:
                if feature.id() in idList:
                    vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(i))
                i += 1

        vectorLayer.updateFields()
        vectorLayer.commitChanges()

    # Performs K-Means clustering. Updates vector layer field.
    def kmeansClustering(self, vectorLayer, attributesList, normalize, clusterNumber, outputFieldName):
        from scipy.cluster.vq import kmeans, vq
        from numpy import array

        fullObjectsList = []
        features = vectorLayer.getFeatures()

        for feature in features:
            fullObjectsList.append([])
            for attribute in attributesList:
                if feature[attribute[0]]:
                    fullObjectsList[len(fullObjectsList) - 1].append(feature[attribute[0]])
                else:
                    fullObjectsList[len(fullObjectsList) - 1].append(0)

        # NORMALIZING
        if normalize:
            i = 0
            maxValues = []
            while i < len(attributesList):
                maxValues.append(max(abs(item[i]) for item in fullObjectsList))
                i += 1

            j = 0
            while j < len(fullObjectsList):
                i = 0
                while i < len(fullObjectsList[j]):
                    fullObjectsList[j][i] = (fullObjectsList[j][i] * 1.0) / (maxValues[i] * 1.0)
                    i += 1
                j += 1

        data = array(fullObjectsList)

        centroids, _ = kmeans(data, clusterNumber, 25)
        idx, _ = vq(data, centroids)
        idx = idx.tolist()

        vectorLayerDataProvider = vectorLayer.dataProvider()

        # Create field of not exist
        if vectorLayer.fields().indexFromName(outputFieldName) == -1:
            vectorLayerDataProvider.addAttributes([QgsField(outputFieldName, QVariant.Int)])

        vectorLayer.updateFields()
        vectorLayer.startEditing()
        attrIdx = vectorLayer.fields().indexFromName(outputFieldName)
        features = vectorLayer.getFeatures()

        i = 0
        for feature in features:
            vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(idx[i]))
            i += 1

        vectorLayer.updateFields()
        vectorLayer.commitChanges()

    # Performs Hierarchical clustering from scipy with unknown number of clusters. Updates vector layer field.
    def hierarchicalClusteringScipy(self, vectorLayer, attributesList, normalize, clusterThreshold, linkageMethod, outputFieldName):
        import scipy.cluster.hierarchy as hcluster
        from numpy import array

        fullObjectsList = []
        features = vectorLayer.getFeatures()

        for feature in features:
            fullObjectsList.append([])
            for attribute in attributesList:
                if feature[attribute[0]]:
                    fullObjectsList[len(fullObjectsList) - 1].append(feature[attribute[0]])
                else:
                    fullObjectsList[len(fullObjectsList) - 1].append(0)

        # NORMALIZING
        if normalize:
            i = 0
            maxValues = []
            while i < len(attributesList):
                maxValues.append(max(abs(item[i]) for item in fullObjectsList))
                i += 1

            j = 0
            while j < len(fullObjectsList):
                i = 0
                while i < len(fullObjectsList[j]):
                    fullObjectsList[j][i] = (fullObjectsList[j][i] * 1.0) / (maxValues[i] * 1.0)
                    i += 1
                j += 1

        data = array(fullObjectsList)

        clusters = hcluster.fclusterdata(data, clusterThreshold, criterion="distance", method=linkageMethod)

        vectorLayerDataProvider = vectorLayer.dataProvider()
#
        ## Create field of not exist
        if vectorLayer.fields().indexFromName(outputFieldName) == -1:
            vectorLayerDataProvider.addAttributes([QgsField(outputFieldName, QVariant.Int)])
#
        vectorLayer.updateFields()
        vectorLayer.startEditing()
        attrIdx = vectorLayer.fields().indexFromName(outputFieldName)
        features = vectorLayer.getFeatures()
#
        i = 0
        for feature in features:
            vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(clusters[i]))
            i += 1
#
        vectorLayer.updateFields()
        vectorLayer.commitChanges()