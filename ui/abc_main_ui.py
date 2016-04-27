# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'abc_main_ui.ui'
#
# Created: Wed Apr 27 04:36:04 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(445, 322)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/attributeBasedClustering/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.helpLink = QtGui.QLabel(Dialog)
        self.helpLink.setAlignment(QtCore.Qt.AlignCenter)
        self.helpLink.setOpenExternalLinks(True)
        self.helpLink.setObjectName(_fromUtf8("helpLink"))
        self.gridLayout_2.addWidget(self.helpLink, 0, 4, 1, 1)
        self.settingsGroup = QtGui.QGroupBox(Dialog)
        self.settingsGroup.setObjectName(_fromUtf8("settingsGroup"))
        self.gridLayout = QtGui.QGridLayout(self.settingsGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.numberOfClustersSpinBox = QtGui.QSpinBox(self.settingsGroup)
        self.numberOfClustersSpinBox.setMinimum(2)
        self.numberOfClustersSpinBox.setProperty("value", 4)
        self.numberOfClustersSpinBox.setObjectName(_fromUtf8("numberOfClustersSpinBox"))
        self.gridLayout.addWidget(self.numberOfClustersSpinBox, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.settingsGroup)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.settingsGroup)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.clusteringMethodComboBox = QtGui.QComboBox(self.settingsGroup)
        self.clusteringMethodComboBox.setObjectName(_fromUtf8("clusteringMethodComboBox"))
        self.clusteringMethodComboBox.addItem(_fromUtf8(""))
        self.clusteringMethodComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.clusteringMethodComboBox, 0, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.settingsGroup)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.outputFieldNameLine = QtGui.QLineEdit(self.settingsGroup)
        self.outputFieldNameLine.setMaxLength(10)
        self.outputFieldNameLine.setObjectName(_fromUtf8("outputFieldNameLine"))
        self.gridLayout.addWidget(self.outputFieldNameLine, 2, 2, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.settingsGroup)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.settingsGroup, 5, 0, 1, 5)
        self.addFieldButton = QtGui.QPushButton(Dialog)
        self.addFieldButton.setObjectName(_fromUtf8("addFieldButton"))
        self.gridLayout_2.addWidget(self.addFieldButton, 2, 1, 1, 2)
        self.fieldsTable = QtGui.QTableWidget(Dialog)
        self.fieldsTable.setObjectName(_fromUtf8("fieldsTable"))
        self.fieldsTable.setColumnCount(2)
        self.fieldsTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.fieldsTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.fieldsTable.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.fieldsTable, 1, 3, 4, 2)
        self.deleteSelectedButton = QtGui.QPushButton(Dialog)
        self.deleteSelectedButton.setObjectName(_fromUtf8("deleteSelectedButton"))
        self.gridLayout_2.addWidget(self.deleteSelectedButton, 3, 1, 1, 2)
        self.deleteAllButton = QtGui.QPushButton(Dialog)
        self.deleteAllButton.setObjectName(_fromUtf8("deleteAllButton"))
        self.gridLayout_2.addWidget(self.deleteAllButton, 4, 1, 1, 2)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 6, 0, 1, 3)
        self.runButton = QtGui.QPushButton(Dialog)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.gridLayout_2.addWidget(self.runButton, 6, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.fieldsComboBox = QtGui.QComboBox(Dialog)
        self.fieldsComboBox.setObjectName(_fromUtf8("fieldsComboBox"))
        self.gridLayout_2.addWidget(self.fieldsComboBox, 1, 1, 1, 2)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout_2.addWidget(self.cancelButton, 6, 4, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.vectorLayerComboBox = QtGui.QComboBox(Dialog)
        self.vectorLayerComboBox.setObjectName(_fromUtf8("vectorLayerComboBox"))
        self.gridLayout_2.addWidget(self.vectorLayerComboBox, 0, 2, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Attribute based clustering", None))
        self.helpLink.setText(_translate("Dialog", "<a href=\"http://www.ekazakov.info/projects/abc_tutorial.html\">Help</a>", None))
        self.settingsGroup.setTitle(_translate("Dialog", "Settings", None))
        self.label_4.setText(_translate("Dialog", "Number of clusters", None))
        self.label_3.setText(_translate("Dialog", "Clusteng method", None))
        self.clusteringMethodComboBox.setItemText(0, _translate("Dialog", "K-Means (not weighted, scipy required, fast)", None))
        self.clusteringMethodComboBox.setItemText(1, _translate("Dialog", "Hierarchical (weighted, native, slow)", None))
        self.label_5.setText(_translate("Dialog", "Output field name", None))
        self.outputFieldNameLine.setText(_translate("Dialog", "class", None))
        self.checkBox.setText(_translate("Dialog", "Normalize attributes", None))
        self.addFieldButton.setText(_translate("Dialog", "--->", None))
        item = self.fieldsTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Field", None))
        item = self.fieldsTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Weight", None))
        self.deleteSelectedButton.setText(_translate("Dialog", "Delete selected", None))
        self.deleteAllButton.setText(_translate("Dialog", "Delete all", None))
        self.runButton.setText(_translate("Dialog", "Run", None))
        self.label_2.setText(_translate("Dialog", "Fields:", None))
        self.cancelButton.setText(_translate("Dialog", "Cancel", None))
        self.label.setText(_translate("Dialog", "Vector layer:", None))