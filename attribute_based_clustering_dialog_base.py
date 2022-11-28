# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attribute_based_clustering_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AttributeBasedClusteringDialog(object):
    def setupUi(self, AttributeBasedClusteringDialog):
        AttributeBasedClusteringDialog.setObjectName("AttributeBasedClusteringDialog")
        AttributeBasedClusteringDialog.resize(573, 734)
        self.gridLayout_2 = QtWidgets.QGridLayout(AttributeBasedClusteringDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressBar = QtWidgets.QProgressBar(AttributeBasedClusteringDialog)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 6, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(AttributeBasedClusteringDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.fieldsComboBox = QgsFieldComboBox(AttributeBasedClusteringDialog)
        self.fieldsComboBox.setObjectName("fieldsComboBox")
        self.gridLayout_2.addWidget(self.fieldsComboBox, 1, 1, 1, 2)
        self.addFieldButton = QtWidgets.QPushButton(AttributeBasedClusteringDialog)
        self.addFieldButton.setObjectName("addFieldButton")
        self.gridLayout_2.addWidget(self.addFieldButton, 2, 1, 1, 2)
        self.deleteSelectedButton = QtWidgets.QPushButton(AttributeBasedClusteringDialog)
        self.deleteSelectedButton.setObjectName("deleteSelectedButton")
        self.gridLayout_2.addWidget(self.deleteSelectedButton, 3, 1, 1, 2)
        self.vectorLayerComboBox = QgsMapLayerComboBox(AttributeBasedClusteringDialog)
        self.vectorLayerComboBox.setObjectName("vectorLayerComboBox")
        self.gridLayout_2.addWidget(self.vectorLayerComboBox, 0, 1, 1, 2)
        self.deleteAllButton = QtWidgets.QPushButton(AttributeBasedClusteringDialog)
        self.deleteAllButton.setObjectName("deleteAllButton")
        self.gridLayout_2.addWidget(self.deleteAllButton, 4, 1, 1, 2)
        self.runButton = QtWidgets.QPushButton(AttributeBasedClusteringDialog)
        self.runButton.setObjectName("runButton")
        self.gridLayout_2.addWidget(self.runButton, 6, 4, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(AttributeBasedClusteringDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 6, 5, 1, 1)
        self.label = QtWidgets.QLabel(AttributeBasedClusteringDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.fieldsTable = QtWidgets.QTableWidget(AttributeBasedClusteringDialog)
        self.fieldsTable.setObjectName("fieldsTable")
        self.fieldsTable.setColumnCount(2)
        self.fieldsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.fieldsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.fieldsTable.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.fieldsTable, 0, 3, 5, 3)
        self.settingsGroup = QtWidgets.QGroupBox(AttributeBasedClusteringDialog)
        self.settingsGroup.setObjectName("settingsGroup")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.settingsGroup)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.MainOptionsTabWidget = QtWidgets.QTabWidget(self.settingsGroup)
        self.MainOptionsTabWidget.setObjectName("MainOptionsTabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 3, 0, 1, 1)
        self.outputFieldNameLine = QtWidgets.QLineEdit(self.tab)
        self.outputFieldNameLine.setMaxLength(10)
        self.outputFieldNameLine.setObjectName("outputFieldNameLine")
        self.gridLayout_7.addWidget(self.outputFieldNameLine, 3, 1, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem, 4, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_7.addWidget(self.checkBox, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_7.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)
        self.numberOfClustersSpinBox = QtWidgets.QSpinBox(self.tab)
        self.numberOfClustersSpinBox.setMinimum(2)
        self.numberOfClustersSpinBox.setProperty("value", 4)
        self.numberOfClustersSpinBox.setObjectName("numberOfClustersSpinBox")
        self.gridLayout_7.addWidget(self.numberOfClustersSpinBox, 1, 1, 1, 3)
        self.clusteringMethodComboBox = QtWidgets.QComboBox(self.tab)
        self.clusteringMethodComboBox.setObjectName("clusteringMethodComboBox")
        self.clusteringMethodComboBox.addItem("")
        self.clusteringMethodComboBox.addItem("")
        self.clusteringMethodComboBox.addItem("")
        self.clusteringMethodComboBox.addItem("")
        self.gridLayout_7.addWidget(self.clusteringMethodComboBox, 0, 1, 1, 3)
        self.MainOptionsTabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_9.addWidget(self.label_4, 2, 0, 1, 1)
        self.distanceFieldPrefix = QtWidgets.QLineEdit(self.tab_2)
        self.distanceFieldPrefix.setObjectName("distanceFieldPrefix")
        self.gridLayout_9.addWidget(self.distanceFieldPrefix, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem1, 3, 1, 1, 1)
        self.distanceModeGroupBox = QtWidgets.QGroupBox(self.tab_2)
        self.distanceModeGroupBox.setObjectName("distanceModeGroupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.distanceModeGroupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.distancesRBDisabled = QtWidgets.QRadioButton(self.distanceModeGroupBox)
        self.distancesRBDisabled.setChecked(True)
        self.distancesRBDisabled.setObjectName("distancesRBDisabled")
        self.gridLayout_8.addWidget(self.distancesRBDisabled, 1, 0, 1, 1)
        self.distancesRBOnlyObjectCluster = QtWidgets.QRadioButton(self.distanceModeGroupBox)
        self.distancesRBOnlyObjectCluster.setObjectName("distancesRBOnlyObjectCluster")
        self.gridLayout_8.addWidget(self.distancesRBOnlyObjectCluster, 2, 0, 1, 1)
        self.distancesRBAllCentroids = QtWidgets.QRadioButton(self.distanceModeGroupBox)
        self.distancesRBAllCentroids.setObjectName("distancesRBAllCentroids")
        self.gridLayout_8.addWidget(self.distancesRBAllCentroids, 3, 0, 1, 1)
        self.gridLayout_9.addWidget(self.distanceModeGroupBox, 1, 0, 1, 2)
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_9.addWidget(self.label_20, 0, 0, 1, 2)
        self.MainOptionsTabWidget.addTab(self.tab_2, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_19 = QtWidgets.QLabel(self.tab_7)
        self.label_19.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_19.setWordWrap(True)
        self.label_19.setObjectName("label_19")
        self.gridLayout_10.addWidget(self.label_19, 0, 0, 1, 4)
        self.label_21 = QtWidgets.QLabel(self.tab_7)
        self.label_21.setObjectName("label_21")
        self.gridLayout_10.addWidget(self.label_21, 1, 0, 1, 1)
        self.maxClusterElbow = QtWidgets.QSpinBox(self.tab_7)
        self.maxClusterElbow.setMinimum(2)
        self.maxClusterElbow.setMaximum(999)
        self.maxClusterElbow.setProperty("value", 10)
        self.maxClusterElbow.setObjectName("maxClusterElbow")
        self.gridLayout_10.addWidget(self.maxClusterElbow, 1, 1, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_10.addItem(spacerItem2, 3, 2, 1, 1)
        self.elbowMethodRun = QtWidgets.QPushButton(self.tab_7)
        self.elbowMethodRun.setObjectName("elbowMethodRun")
        self.gridLayout_10.addWidget(self.elbowMethodRun, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(372, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem3, 2, 1, 1, 3)
        self.MainOptionsTabWidget.addTab(self.tab_7, "")
        self.gridLayout_6.addWidget(self.MainOptionsTabWidget, 0, 0, 1, 2)
        self.additionalOptionsTabWidget = QtWidgets.QTabWidget(self.settingsGroup)
        self.additionalOptionsTabWidget.setEnabled(True)
        self.additionalOptionsTabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.additionalOptionsTabWidget.setDocumentMode(False)
        self.additionalOptionsTabWidget.setTabsClosable(False)
        self.additionalOptionsTabWidget.setMovable(False)
        self.additionalOptionsTabWidget.setObjectName("additionalOptionsTabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout.setObjectName("gridLayout")
        self.kmeansThresholdLineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.kmeansThresholdLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.kmeansThresholdLineEdit.setObjectName("kmeansThresholdLineEdit")
        self.gridLayout.addWidget(self.kmeansThresholdLineEdit, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.helpLink_2 = QtWidgets.QLabel(self.tab_3)
        self.helpLink_2.setAlignment(QtCore.Qt.AlignCenter)
        self.helpLink_2.setOpenExternalLinks(True)
        self.helpLink_2.setObjectName("helpLink_2")
        self.gridLayout.addWidget(self.helpLink_2, 0, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)
        self.kmeansIterSpinBox = QtWidgets.QSpinBox(self.tab_3)
        self.kmeansIterSpinBox.setMinimum(1)
        self.kmeansIterSpinBox.setMaximum(9999)
        self.kmeansIterSpinBox.setProperty("value", 20)
        self.kmeansIterSpinBox.setObjectName("kmeansIterSpinBox")
        self.gridLayout.addWidget(self.kmeansIterSpinBox, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 4, 1, 1, 1)
        self.additionalOptionsTabWidget.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.kmeans2MethodComboBox = QtWidgets.QComboBox(self.tab_5)
        self.kmeans2MethodComboBox.setObjectName("kmeans2MethodComboBox")
        self.kmeans2MethodComboBox.addItem("")
        self.kmeans2MethodComboBox.addItem("")
        self.kmeans2MethodComboBox.addItem("")
        self.gridLayout_3.addWidget(self.kmeans2MethodComboBox, 3, 1, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.tab_5)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 2, 1)
        self.helpLink_3 = QtWidgets.QLabel(self.tab_5)
        self.helpLink_3.setAlignment(QtCore.Qt.AlignCenter)
        self.helpLink_3.setOpenExternalLinks(True)
        self.helpLink_3.setObjectName("helpLink_3")
        self.gridLayout_3.addWidget(self.helpLink_3, 0, 0, 1, 3)
        self.label_12 = QtWidgets.QLabel(self.tab_5)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 3, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 4, 1, 1, 1)
        self.kmeans2IterSpinBox = QtWidgets.QSpinBox(self.tab_5)
        self.kmeans2IterSpinBox.setMinimum(1)
        self.kmeans2IterSpinBox.setMaximum(99999999)
        self.kmeans2IterSpinBox.setProperty("value", 20)
        self.kmeans2IterSpinBox.setObjectName("kmeans2IterSpinBox")
        self.gridLayout_3.addWidget(self.kmeans2IterSpinBox, 1, 1, 2, 2)
        self.additionalOptionsTabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_18 = QtWidgets.QLabel(self.tab_6)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_5.addWidget(self.label_18, 0, 0, 1, 1)
        self.additionalOptionsTabWidget.addTab(self.tab_6, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.linkageMethodComboBox = QtWidgets.QComboBox(self.tab_4)
        self.linkageMethodComboBox.setObjectName("linkageMethodComboBox")
        self.linkageMethodComboBox.addItem("")
        self.linkageMethodComboBox.addItem("")
        self.linkageMethodComboBox.addItem("")
        self.linkageMethodComboBox.addItem("")
        self.linkageMethodComboBox.addItem("")
        self.linkageMethodComboBox.addItem("")
        self.linkageMethodComboBox.addItem("")
        self.gridLayout_4.addWidget(self.linkageMethodComboBox, 6, 1, 1, 1)
        self.criterionComBox = QtWidgets.QComboBox(self.tab_4)
        self.criterionComBox.setObjectName("criterionComBox")
        self.criterionComBox.addItem("")
        self.criterionComBox.addItem("")
        self.criterionComBox.addItem("")
        self.gridLayout_4.addWidget(self.criterionComBox, 3, 1, 1, 1)
        self.clusteringThresholdLine = QtWidgets.QLineEdit(self.tab_4)
        self.clusteringThresholdLine.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.clusteringThresholdLine.setObjectName("clusteringThresholdLine")
        self.gridLayout_4.addWidget(self.clusteringThresholdLine, 1, 1, 1, 1)
        self.metricComboBox = QtWidgets.QComboBox(self.tab_4)
        self.metricComboBox.setObjectName("metricComboBox")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.metricComboBox.addItem("")
        self.gridLayout_4.addWidget(self.metricComboBox, 4, 1, 1, 1)
        self.maxNumberOfClustersSpinBox = QtWidgets.QSpinBox(self.tab_4)
        self.maxNumberOfClustersSpinBox.setObjectName("maxNumberOfClustersSpinBox")
        self.gridLayout_4.addWidget(self.maxNumberOfClustersSpinBox, 2, 1, 1, 1)
        self.depthSpinBox = QtWidgets.QSpinBox(self.tab_4)
        self.depthSpinBox.setMinimum(1)
        self.depthSpinBox.setProperty("value", 2)
        self.depthSpinBox.setObjectName("depthSpinBox")
        self.gridLayout_4.addWidget(self.depthSpinBox, 5, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tab_4)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 3, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.tab_4)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 2, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.tab_4)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_4)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.tab_4)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)
        self.helpLink_4 = QtWidgets.QLabel(self.tab_4)
        self.helpLink_4.setAlignment(QtCore.Qt.AlignCenter)
        self.helpLink_4.setOpenExternalLinks(True)
        self.helpLink_4.setObjectName("helpLink_4")
        self.gridLayout_4.addWidget(self.helpLink_4, 0, 0, 1, 2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem6, 7, 1, 1, 1)
        self.additionalOptionsTabWidget.addTab(self.tab_4, "")
        self.gridLayout_6.addWidget(self.additionalOptionsTabWidget, 3, 0, 1, 2)
        self.label_13 = QtWidgets.QLabel(self.settingsGroup)
        self.label_13.setObjectName("label_13")
        self.gridLayout_6.addWidget(self.label_13, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.settingsGroup, 5, 0, 1, 6)

        self.retranslateUi(AttributeBasedClusteringDialog)
        self.MainOptionsTabWidget.setCurrentIndex(0)
        self.additionalOptionsTabWidget.setCurrentIndex(0)
        self.linkageMethodComboBox.setCurrentIndex(0)
        self.criterionComBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(AttributeBasedClusteringDialog)

    def retranslateUi(self, AttributeBasedClusteringDialog):
        _translate = QtCore.QCoreApplication.translate
        AttributeBasedClusteringDialog.setWindowTitle(_translate("AttributeBasedClusteringDialog", "Attribute based clustering"))
        self.label_2.setText(_translate("AttributeBasedClusteringDialog", "Fields:"))
        self.addFieldButton.setText(_translate("AttributeBasedClusteringDialog", "--->"))
        self.deleteSelectedButton.setText(_translate("AttributeBasedClusteringDialog", "Delete selected"))
        self.deleteAllButton.setText(_translate("AttributeBasedClusteringDialog", "Delete all"))
        self.runButton.setText(_translate("AttributeBasedClusteringDialog", "Run"))
        self.cancelButton.setText(_translate("AttributeBasedClusteringDialog", "Cancel"))
        self.label.setText(_translate("AttributeBasedClusteringDialog", "Vector layer:"))
        item = self.fieldsTable.horizontalHeaderItem(0)
        item.setText(_translate("AttributeBasedClusteringDialog", "Field"))
        item = self.fieldsTable.horizontalHeaderItem(1)
        item.setText(_translate("AttributeBasedClusteringDialog", "Weight"))
        self.settingsGroup.setTitle(_translate("AttributeBasedClusteringDialog", "Settings"))
        self.label_5.setText(_translate("AttributeBasedClusteringDialog", "Output field name"))
        self.outputFieldNameLine.setText(_translate("AttributeBasedClusteringDialog", "class"))
        self.checkBox.setText(_translate("AttributeBasedClusteringDialog", "Normalize attributes"))
        self.label_8.setText(_translate("AttributeBasedClusteringDialog", "Number of clusters"))
        self.label_3.setText(_translate("AttributeBasedClusteringDialog", "Clusteng method"))
        self.clusteringMethodComboBox.setItemText(0, _translate("AttributeBasedClusteringDialog", "K-Means (not weighted, scipy required, fast, known number of clusters)"))
        self.clusteringMethodComboBox.setItemText(1, _translate("AttributeBasedClusteringDialog", "K-Means-2 (not weighted, scipy required, fast, known number of clusters)"))
        self.clusteringMethodComboBox.setItemText(2, _translate("AttributeBasedClusteringDialog", "Hierarchical (weighted, native, slow, known number of clusters)"))
        self.clusteringMethodComboBox.setItemText(3, _translate("AttributeBasedClusteringDialog", "Hierarchical-2 (not weighted, scipy required, fast, auto number of clusters)"))
        self.MainOptionsTabWidget.setTabText(self.MainOptionsTabWidget.indexOf(self.tab), _translate("AttributeBasedClusteringDialog", "Main settings"))
        self.label_4.setText(_translate("AttributeBasedClusteringDialog", "Prefix for fields with distance:"))
        self.distanceFieldPrefix.setText(_translate("AttributeBasedClusteringDialog", "dist_"))
        self.distanceModeGroupBox.setTitle(_translate("AttributeBasedClusteringDialog", "Mode"))
        self.distancesRBDisabled.setText(_translate("AttributeBasedClusteringDialog", "Do not calculate distances (default)"))
        self.distancesRBOnlyObjectCluster.setText(_translate("AttributeBasedClusteringDialog", "Calculate distances to centroid of object\'s cluster only"))
        self.distancesRBAllCentroids.setText(_translate("AttributeBasedClusteringDialog", "Calculate distances to all centroids"))
        self.label_20.setText(_translate("AttributeBasedClusteringDialog", "Not supported for Hierarchical-2"))
        self.MainOptionsTabWidget.setTabText(self.MainOptionsTabWidget.indexOf(self.tab_2), _translate("AttributeBasedClusteringDialog", "Distance to centroids calculations"))
        self.label_19.setText(_translate("AttributeBasedClusteringDialog", "Elbow method is a heuristic used in determining the number of clusters in a data set. This tool allows you to plot Elbow graph and figure out an optimal number of clusters. <a href=\"https://en.wikipedia.org/wiki/Elbow_method_(clustering)\">Check for more info</a>. Matplotlib is required to use this tool! Selected clustring method and it\'s setting will be used. Hierarchical-2 is not supported"))
        self.label_21.setText(_translate("AttributeBasedClusteringDialog", "Maximal number of clusters"))
        self.elbowMethodRun.setText(_translate("AttributeBasedClusteringDialog", "Draw Elbow plot"))
        self.MainOptionsTabWidget.setTabText(self.MainOptionsTabWidget.indexOf(self.tab_7), _translate("AttributeBasedClusteringDialog", "Elbow method"))
        self.kmeansThresholdLineEdit.setText(_translate("AttributeBasedClusteringDialog", "0.00001"))
        self.label_10.setText(_translate("AttributeBasedClusteringDialog", "Threshold"))
        self.helpLink_2.setText(_translate("AttributeBasedClusteringDialog", "<a href=\"https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans\">Original documentation for algorithm</a>"))
        self.label_9.setText(_translate("AttributeBasedClusteringDialog", "Number of times\n"
"to run k-means"))
        self.additionalOptionsTabWidget.setTabText(self.additionalOptionsTabWidget.indexOf(self.tab_3), _translate("AttributeBasedClusteringDialog", "K-Means"))
        self.kmeans2MethodComboBox.setItemText(0, _translate("AttributeBasedClusteringDialog", "random"))
        self.kmeans2MethodComboBox.setItemText(1, _translate("AttributeBasedClusteringDialog", "points"))
        self.kmeans2MethodComboBox.setItemText(2, _translate("AttributeBasedClusteringDialog", "++"))
        self.label_11.setText(_translate("AttributeBasedClusteringDialog", "Number of iterations\n"
"of the k-means\n"
"algorithm to run"))
        self.helpLink_3.setText(_translate("AttributeBasedClusteringDialog", "<a href=\"https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html#scipy.cluster.vq.kmeans2\">Original documentation for algorithm</a>"))
        self.label_12.setText(_translate("AttributeBasedClusteringDialog", "Method for\n"
"initialization"))
        self.additionalOptionsTabWidget.setTabText(self.additionalOptionsTabWidget.indexOf(self.tab_5), _translate("AttributeBasedClusteringDialog", "K-Means-2"))
        self.label_18.setText(_translate("AttributeBasedClusteringDialog", "Nothing to configure"))
        self.additionalOptionsTabWidget.setTabText(self.additionalOptionsTabWidget.indexOf(self.tab_6), _translate("AttributeBasedClusteringDialog", "Hierarchical"))
        self.linkageMethodComboBox.setItemText(0, _translate("AttributeBasedClusteringDialog", "single"))
        self.linkageMethodComboBox.setItemText(1, _translate("AttributeBasedClusteringDialog", "complete"))
        self.linkageMethodComboBox.setItemText(2, _translate("AttributeBasedClusteringDialog", "average"))
        self.linkageMethodComboBox.setItemText(3, _translate("AttributeBasedClusteringDialog", "median"))
        self.linkageMethodComboBox.setItemText(4, _translate("AttributeBasedClusteringDialog", "weighted"))
        self.linkageMethodComboBox.setItemText(5, _translate("AttributeBasedClusteringDialog", "ward"))
        self.linkageMethodComboBox.setItemText(6, _translate("AttributeBasedClusteringDialog", "centroid"))
        self.criterionComBox.setItemText(0, _translate("AttributeBasedClusteringDialog", "inconsistent"))
        self.criterionComBox.setItemText(1, _translate("AttributeBasedClusteringDialog", "distance"))
        self.criterionComBox.setItemText(2, _translate("AttributeBasedClusteringDialog", "maxclust"))
        self.clusteringThresholdLine.setText(_translate("AttributeBasedClusteringDialog", "0.5"))
        self.metricComboBox.setItemText(0, _translate("AttributeBasedClusteringDialog", "euclidean"))
        self.metricComboBox.setItemText(1, _translate("AttributeBasedClusteringDialog", "minkowski"))
        self.metricComboBox.setItemText(2, _translate("AttributeBasedClusteringDialog", "cityblock"))
        self.metricComboBox.setItemText(3, _translate("AttributeBasedClusteringDialog", "seuclidean"))
        self.metricComboBox.setItemText(4, _translate("AttributeBasedClusteringDialog", "sqeuclidean"))
        self.metricComboBox.setItemText(5, _translate("AttributeBasedClusteringDialog", "cosine"))
        self.metricComboBox.setItemText(6, _translate("AttributeBasedClusteringDialog", "correlation"))
        self.metricComboBox.setItemText(7, _translate("AttributeBasedClusteringDialog", "hamming"))
        self.metricComboBox.setItemText(8, _translate("AttributeBasedClusteringDialog", "jaccard"))
        self.metricComboBox.setItemText(9, _translate("AttributeBasedClusteringDialog", "chebyshev"))
        self.metricComboBox.setItemText(10, _translate("AttributeBasedClusteringDialog", "canberra"))
        self.metricComboBox.setItemText(11, _translate("AttributeBasedClusteringDialog", "braycurtis"))
        self.metricComboBox.setItemText(12, _translate("AttributeBasedClusteringDialog", "mahalanobis"))
        self.metricComboBox.setItemText(13, _translate("AttributeBasedClusteringDialog", "matching"))
        self.metricComboBox.setItemText(14, _translate("AttributeBasedClusteringDialog", "dice"))
        self.metricComboBox.setItemText(15, _translate("AttributeBasedClusteringDialog", "kulsinski"))
        self.metricComboBox.setItemText(16, _translate("AttributeBasedClusteringDialog", "rogerstanimoto"))
        self.metricComboBox.setItemText(17, _translate("AttributeBasedClusteringDialog", "russellrao"))
        self.metricComboBox.setItemText(18, _translate("AttributeBasedClusteringDialog", "sokalmichener"))
        self.metricComboBox.setItemText(19, _translate("AttributeBasedClusteringDialog", "sokalsneath"))
        self.label_15.setText(_translate("AttributeBasedClusteringDialog", "Criterion"))
        self.label_14.setText(_translate("AttributeBasedClusteringDialog", "Max number of clusters"))
        self.label_17.setText(_translate("AttributeBasedClusteringDialog", "Metric"))
        self.label_7.setText(_translate("AttributeBasedClusteringDialog", "Linkage method"))
        self.label_16.setText(_translate("AttributeBasedClusteringDialog", "Depth"))
        self.label_6.setText(_translate("AttributeBasedClusteringDialog", "Clustering threshold"))
        self.helpLink_4.setText(_translate("AttributeBasedClusteringDialog", "<a href=\"https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fclusterdata.html#scipy.cluster.hierarchy.fclusterdata\">Original documentation for algorithm</a>"))
        self.additionalOptionsTabWidget.setTabText(self.additionalOptionsTabWidget.indexOf(self.tab_4), _translate("AttributeBasedClusteringDialog", "Hierarchical-2"))
        self.label_13.setText(_translate("AttributeBasedClusteringDialog", "Additional options:"))
from qgsfieldcombobox import QgsFieldComboBox
from qgsmaplayercombobox import QgsMapLayerComboBox


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttributeBasedClusteringDialog = QtWidgets.QDialog()
    ui = Ui_AttributeBasedClusteringDialog()
    ui.setupUi(AttributeBasedClusteringDialog)
    AttributeBasedClusteringDialog.show()
    sys.exit(app.exec_())
