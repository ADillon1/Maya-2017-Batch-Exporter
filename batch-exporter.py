# Brief: Batch Exporter
# Author: Andrew Dillon
# Date: 9/17/2017

# See readme.md for more details on use.
# Distributed under MIT

import maya.cmds as cmds
import maya.mel
import os, sys, pprint, inspect
import pymel.core as pm
from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 328)
        self.change_btn = QtWidgets.QPushButton(Dialog)
        self.change_btn.setGeometry(QtCore.QRect(320, 10, 75, 23))
        self.change_btn.setObjectName("change_btn")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 21))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(320, 300, 71, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.textBox = QtWidgets.QLineEdit(Dialog)
        self.textBox.setEnabled(False)
        self.textBox.setGeometry(QtCore.QRect(60, 10, 251, 20))
        self.textBox.setObjectName("textBox")
        self.export_btn = QtWidgets.QPushButton(Dialog)
        self.export_btn.setGeometry(QtCore.QRect(10, 300, 75, 23))
        self.export_btn.setObjectName("export_btn")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(270, 300, 51, 21))
        self.label_2.setObjectName("label_2")
        self.output = QtWidgets.QPlainTextEdit(Dialog)
        self.output.setEnabled(True)
        self.output.setGeometry(QtCore.QRect(10, 40, 381, 251))
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("")
        self.output.setObjectName("output")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Batch Exporter", None, -1))
        self.change_btn.setText(QtWidgets.QApplication.translate("Dialog", "Browse", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Location:", None, -1))
        self.comboBox.setItemText(0, QtWidgets.QApplication.translate("Dialog", ".fbx", None, -1))
        self.comboBox.setItemText(1, QtWidgets.QApplication.translate("Dialog", ".obj", None, -1))
        self.comboBox.setItemText(2, QtWidgets.QApplication.translate("Dialog", ".mb", None, -1))
        self.comboBox.setItemText(3, QtWidgets.QApplication.translate("Dialog", ".ma", None, -1))
        self.textBox.setText(QtWidgets.QApplication.translate("Dialog", "C:", None, -1))
        self.export_btn.setText(QtWidgets.QApplication.translate("Dialog", "Export", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "File Type:", None, -1))

class Exporter(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.activeWindow()):
        super(Exporter, self).__init__(parent)
        for c in parent.children():
            if isinstance(c, QtWidgets.QDialog) and c.isVisible():
                c.close()
                
        self.ui = Ui_Dialog()

        # set up the interface from the compiled ui file
        self.ui.setupUi(self)

        # This is a lightweight Tool window       
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui.change_btn.clicked.connect(self.changeDirectory)
        self.ui.export_btn.clicked.connect(self.exportSelection)
        self.show()

    def changeDirectory(self, *arg):
        text = cmds.fileDialog2(cap='Select Target Directory',
                        fm=3,
                        okc='Accept',
                        cc='Cancel')
        if not text == None:
            self.ui.textBox.setText(text[0])

    def exportSelection(self, *arg):
        selected = cmds.ls(sl=1)
        path = self.ui.textBox.text() + '/'
        ext = self.ui.comboBox.currentText()
        self.ui.output.clear()

        if not cmds.pluginInfo('objExport', q=True, l=True):
            text = self.ui.output.toPlainText()
            self.ui.output.setPlainText(text + "Loaded OBJ plugin.\n")
            cmds.loadPlugin('objExport')

        if not cmds.pluginInfo('fbxmaya', q=True, l=True):
            text = self.ui.output.toPlainText()
            self.ui.output.setPlainText(text + "Loaded FBX plugin. \n")
            cmds.loadPlugin('fbxmaya')

        # Check for selection in outliner.
        if len(selected) == 0:
            text = self.ui.output.toPlainText()
            self.ui.output.setPlainText(text + "Error: Nothing selected in outliner! \n")
            return

        # Check for updated path.
        if self.ui.textBox.text() == "C:":
            text = self.ui.output.toPlainText()
            self.ui.output.setPlainText(text + "Error: Don't forget to set the target path! \n")
            return

        self.ui.output.clear()
        self.ui.output.setPlainText("Location: " + path + "\n")

        for selection in selected:
            text = self.ui.output.toPlainText()
            cmds.select(selection, r=True)
            
            # store object position
            x_value = cmds.getAttr("%s.translateX" % selection)
            y_value = cmds.getAttr("%s.translateY" % selection)
            z_value = cmds.getAttr("%s.translateZ" % selection)
            
            # move to origin
            cmds.setAttr("%s.translateX" % selection, 0);
            cmds.setAttr("%s.translateY" % selection, 0);
            cmds.setAttr("%s.translateZ" % selection, 0);
            
            # freeze transforms
            cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
            
            if '|' in selection:
                selection = selection.partition('|')[2]
            
            if ext == '.fbx':
                pm.mel.FBXExport(s=True, f=path + selection + ext)
            elif ext == '.obj':
                pm.mel.file(path+selection+ext,force=1, es=True, typ="OBJexport", op="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", pr=1)
            elif ext == '.mb':
                pm.mel.file(path+selection+ext,force=1, es=True, typ="mayaBinary", op="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", pr=1)
            elif ext == '.ma':
                pm.mel.file(path+selection+ext,force=1, es=True, typ="mayaAscii", op="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", pr=1)
            self.ui.output.setPlainText(text + "Exporting: " + selection + ext + "\n")
            
            # move back to origional position
            cmds.setAttr("%s.translateX" % selection, x_value);
            cmds.setAttr("%s.translateY" % selection, y_value);
            cmds.setAttr("%s.translateZ" % selection, z_value);
            
        text = self.ui.output.toPlainText()
        self.ui.output.setPlainText(text + "Finished!")

ui = Exporter()