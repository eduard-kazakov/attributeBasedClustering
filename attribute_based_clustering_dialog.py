# -*- coding: utf-8 -*-
"""
Attribute based clustering: QGIS Plugin

https://github.com/eduard-kazakov/attributeBasedClustering

Eduard Kazakov | ee.kazakov@gmail.com

2024
"""

import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from qgis.core import QgsFieldProxyModel,QgsMapLayerProxyModel
from .attribute_based_clustering_algoritms import perform_clustering, draw_elbow_plot

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attribute_based_clustering_dialog_base.ui'))

class AttributeBasedClusteringDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(AttributeBasedClusteringDialog, self).__init__(parent)
        self.setupUi(self)

        # UI Preparation
        self.vectorLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.fieldsComboBox.setLayer(self.vectorLayerComboBox.currentLayer())
        self.fieldsComboBox.setFilters(QgsFieldProxyModel.Numeric)
        self.maxNumberOfClustersSpinBox.setDisabled(True)
        self.progressBar.setVisible(False)

        # Buttons
        self.vectorLayerComboBox.currentIndexChanged.connect(self.layerChanged)
        self.additionalOptionsTabWidget.currentChanged.connect(self.tabChanged)
        self.clusteringMethodComboBox.currentIndexChanged.connect(self.methodChanged)

        self.criterionComBox.currentIndexChanged.connect(self.criterionChanged)

        self.addFieldButton.clicked.connect(self.addField)
        self.deleteSelectedButton.clicked.connect(self.deleteSelectedFields)
        self.deleteAllButton.clicked.connect(self.deleteAllFields)
        self.runButton.clicked.connect(self.run)
        self.cancelButton.clicked.connect(self.cancel)

        self.elbowMethodRun.clicked.connect(self.elbow_run)

    def layerChanged(self):
        self.deleteAllFields()
        self.fieldsComboBox.setLayer(self.vectorLayerComboBox.currentLayer())
        self.fieldsComboBox.setFilters(QgsFieldProxyModel.Numeric)

    def tabChanged(self):
        if self.additionalOptionsTabWidget.currentIndex() == 3:
            self.clusteringMethodComboBox.setCurrentIndex(3)

        if self.additionalOptionsTabWidget.currentIndex() == 2:
            self.clusteringMethodComboBox.setCurrentIndex(2)

        if self.additionalOptionsTabWidget.currentIndex() == 1:
            self.clusteringMethodComboBox.setCurrentIndex(1)

        if self.additionalOptionsTabWidget.currentIndex() == 0:
            self.clusteringMethodComboBox.setCurrentIndex(0)


    def methodChanged(self):
        if self.clusteringMethodComboBox.currentIndex() == 3:
            self.additionalOptionsTabWidget.setCurrentIndex(3)
            self.numberOfClustersSpinBox.setDisabled(True)
            self.distancesRBDisabled.setChecked(True)
            self.distanceModeGroupBox.setDisabled(True)


        if self.clusteringMethodComboBox.currentIndex() == 0:
            self.additionalOptionsTabWidget.setCurrentIndex(0)
            self.numberOfClustersSpinBox.setEnabled(True)
            self.distanceModeGroupBox.setEnabled(True)

        if self.clusteringMethodComboBox.currentIndex() == 1:
            self.additionalOptionsTabWidget.setCurrentIndex(1)
            self.numberOfClustersSpinBox.setEnabled(True)
            self.distanceModeGroupBox.setEnabled(True)
        if self.clusteringMethodComboBox.currentIndex() == 2:
            self.additionalOptionsTabWidget.setCurrentIndex(2)
            self.numberOfClustersSpinBox.setEnabled(True)
            self.distanceModeGroupBox.setEnabled(True)

    def criterionChanged(self):
        if self.criterionComBox.currentIndex() == 0:
            self.maxNumberOfClustersSpinBox.setDisabled(True)
            self.clusteringThresholdLine.setEnabled(True)

        if self.criterionComBox.currentIndex() == 1:
            self.maxNumberOfClustersSpinBox.setDisabled(True)
            self.clusteringThresholdLine.setEnabled(True)

        if self.criterionComBox.currentIndex() == 2:
            self.maxNumberOfClustersSpinBox.setEnabled(True)
            self.clusteringThresholdLine.setDisabled(True)


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

    def check_and_get_inputs (self, action):
        parameters = {}

        # Common
        if not self.vectorLayerComboBox.currentText():
            QtWidgets.QMessageBox.critical(None, "Error", 'No layer specified!')
            return {}

        if not self.fieldsTable.rowCount():
            QtWidgets.QMessageBox.critical(None, "Error", 'No attributes specified!')
            return {}

        if not self.checkIfTableIsCorrect():
            QtWidgets.QMessageBox.critical(None, "Error", 'Table is incorrect! Check fields and weights')
            return {}

        parameters['vector_layer'] = self.vectorLayerComboBox.currentLayer()
        parameters['normalize'] = self.checkBox.isChecked()
        parameters['cluster_number'] = int(self.numberOfClustersSpinBox.text())
        parameters['output_field_name'] = self.outputFieldNameLine.text()

        parameters['max_clusters_elbow'] = int(self.maxClusterElbow.text())

        calculate_distances_mode = 'disabled'
        if self.distancesRBDisabled.isChecked():
            calculate_distances_mode = 'disabled'
        elif self.distancesRBOnlyObjectCluster.isChecked():
            calculate_distances_mode = 'only_object_cluster'
        elif self.distancesRBAllCentroids.isChecked():
            calculate_distances_mode = 'all_clusters'
        parameters['calculate_distances_mode'] = calculate_distances_mode

        distance_field_prefix = None
        if calculate_distances_mode != 'disabled':
            if not self.distanceFieldPrefix.text():
                QtWidgets.QMessageBox.critical(None, "Error", 'Prefix for field with distance must be set')
                return {}
            else:
                distance_field_prefix = self.distanceFieldPrefix.text()
        parameters['distance_field_prefix'] = distance_field_prefix
        
        attributes_list = []
        all_rows = self.fieldsTable.rowCount()
        for row in range(0, all_rows):
            attributes_list.append([self.fieldsTable.item(row, 0).text(), float(self.fieldsTable.item(row, 1).text())])
        parameters['attributes_list'] = attributes_list

        # Specific by algorithm
        # K-Means
        if self.clusteringMethodComboBox.currentIndex() == 0:
            parameters['algorithm'] = 'kmeans'
            try:
                kmeans_clustering_threshold = float(self.kmeansThresholdLineEdit.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Threshold must be float! %s' % str(e))
                return {}
            parameters['kmeans_clustering_threshold'] = kmeans_clustering_threshold

            try:
                kmeans_iter = int(self.kmeansIterSpinBox.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Number of iterations must be integer! %s' % str(e))
                return
            parameters['kmeans_iter'] = kmeans_iter
        
        if self.clusteringMethodComboBox.currentIndex() == 1:
            parameters['algorithm'] = 'kmeans2'
            try:
                kmeans2_iter = int(self.kmeans2IterSpinBox.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Number of iterations must be integer! %s' % str(e))
                return {}
            
            parameters['kmeans2_iter'] = kmeans2_iter
            parameters['kmeans2_method'] = self.kmeans2MethodComboBox.currentText()

        if self.clusteringMethodComboBox.currentIndex() == 2:
            parameters['algorithm'] = 'hier'

        if self.clusteringMethodComboBox.currentIndex() == 3:
            parameters['algorithm'] = 'hier2'
            try:
                hier2_threshold = float(self.clusteringThresholdLine.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Threshold must be float! %s' % str(e))
                return {}
            parameters['hier2_threshold'] = hier2_threshold

            try:
                hier2_max_clusters = int(self.maxNumberOfClustersSpinBox.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Max number of clusters must be integer! %s' % str(e))
                return {}
            parameters['hier2_max_clusters'] = hier2_max_clusters

            try:
                hier2_depth = int(self.depthSpinBox.text())
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", 'Depth must be integer! %s' % str(e))
                return {}
            parameters['hier2_depth'] = hier2_depth
            parameters['hier2_linkage_method'] = self.linkageMethodComboBox.currentText()
            parameters['hier2_criterion'] = self.criterionComBox.currentText()
            parameters['hier2_metric'] = self.metricComboBox.currentText()

        # Specific by action
        if action == 'algorithm_run':
            if not self.outputFieldNameLine.text():
                QtWidgets.QMessageBox.critical(None, "Error", 'No output field name specified!')
                return {}
            
            output_mode = 'temp'
            output_temp_layer_name=None
            if self.saveToTemporaryLayerRB.isChecked():
                output_mode = 'temp'
                if self.tempLayerName.text() is None:
                    output_temp_layer_name = 'Clusteted'
                else: 
                    output_temp_layer_name = self.tempLayerName.text()
            if self.updateSourceRB.isChecked():
                output_mode = 'source'

            parameters['output_mode'] = output_mode
            parameters['output_temp_layer_name'] = output_temp_layer_name

        elif action == 'elbow_run':
            pass

        return parameters

    def get_run_parameters(self, general_parameters):
        if general_parameters['algorithm'] == 'kmeans':
            run_parameters = {
                          'cluster_number': general_parameters['cluster_number'],
                          'iterations': general_parameters['kmeans_iter'],
                          'threshold': general_parameters['kmeans_clustering_threshold']
            }

        elif general_parameters['algorithm'] == 'kmeans2':
            run_parameters = {
                          'cluster_number': general_parameters['cluster_number'],
                          'iterations': general_parameters['kmeans2_iter'],
                          'method': general_parameters['kmeans2_method']
            }

        elif general_parameters['algorithm'] == 'hier':
            run_parameters = {'cluster_number': general_parameters['cluster_number']}

        elif general_parameters['algorithm'] == 'hier2':
            run_parameters = {'threshold': general_parameters['hier2_threshold'],
                              'max_clusters': general_parameters['hier2_max_clusters'],
                              'depth': general_parameters['hier2_depth'],
                              'linkage_method': general_parameters['hier2_linkage_method'],
                              'criterion': general_parameters['hier2_criterion'],
                              'metric': general_parameters['hier2_metric']}
        
        return run_parameters

    def run(self):

        general_parameters = self.check_and_get_inputs(action='algorithm_run')
        if not general_parameters:
            return
        
        run_parameters = self.get_run_parameters(general_parameters)

        try:
            perform_clustering(vector_layer=general_parameters['vector_layer'],
                               attributes_list=general_parameters['attributes_list'],
                               normalize=general_parameters['normalize'],
                               algorithm=general_parameters['algorithm'],
                               parameters=run_parameters,
                               output_field_name=general_parameters['output_field_name'],
                               output_mode=general_parameters['output_mode'],
                               distance_calculation_method=general_parameters['calculate_distances_mode'],
                               distance_field_prefix=general_parameters['distance_field_prefix'],
                               just_error_calculation=False,
                               temporary_file_name=general_parameters['output_temp_layer_name'])
        except ImportError:
            self.activateInterface()
            QtWidgets.QMessageBox.critical(None, "Error", 'Scipy is required to run this method')
            return
        except Exception as e:
            self.activateInterface()
            QtWidgets.QMessageBox.critical(None, "Error", 'Problems during clustering... %s' % str(e))
            return
        
        self.activateInterface()
        QtWidgets.QMessageBox.about(None, "Success", "Done!")

        return

    def elbow_run(self):
        general_parameters = self.check_and_get_inputs(action='elbow_run')
        if not general_parameters:
            return
        
        if general_parameters['algorithm'] == 'hier2':
            self.activateInterface()
            QtWidgets.QMessageBox.critical(None, "Error", 'Hierarchical 2 is not supported')
            return

        run_parameters = self.get_run_parameters(general_parameters)

        try:
            draw_elbow_plot(vector_layer=general_parameters['vector_layer'],
                            attributes_list=general_parameters['attributes_list'],
                            normalize=general_parameters['normalize'],
                            algorithm=general_parameters['algorithm'],
                            parameters=run_parameters,
                            max_clusters=general_parameters['max_clusters_elbow'])
        except ImportError:
            self.activateInterface()
            QtWidgets.QMessageBox.critical(None, "Error", 'Matplotlib is required to run this method')
            return
        except Exception as e:
            self.activateInterface()
            QtWidgets.QMessageBox.critical(None, "Error", 'Problems during elbow method... %s' % str(e))
            return

    def cancel(self):
        self.close()