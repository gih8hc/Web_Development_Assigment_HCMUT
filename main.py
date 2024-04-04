import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from Object3d import GLWidget
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from sidebar_ui import Ui_MainWindow
import numpy as np
import sys




class MainWindow(QMainWindow):
    """
    DashBoard contains side bar.
    We implement behaviors of dashboard here.

    Args:
        QMainWindow (QWidget): Main widget
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
        self.initGL()
        self.initHomePage()
        #! add item to drop down 3d
        self.addItemRadar()
        self.addItemFile()
        self.addItemDate()
        self.addItemMode()


        timer = QtCore.QTimer(self)
        timer.setInterval(10)   # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()
    ## Function for searching
    # def on_search_btn_clicked(self):
    #     self.ui.stackedWidget.setCurrentIndex(5)
    #     search_text = self.ui.search_input.text().strip()
    #     if search_text:
    #         self.ui.label_9.setText(search_text)

    ## Function for changing page to user page
    # def on_user_btn_clicked(self):
    #     self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.labelPage.setText("Home Page")

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.labelPage.setText("Home Page")


    def on_view3d_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.labelPage.setText("3D View")


    def on_view3d_2_toggled(self):
        self.ui.labelPage.setText("3D View")
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_view2d_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.labelPage.setText("2D View")


    def on_view2d_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.labelPage.setText("2D View")


    def on_other_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.labelPage.setText("Others Page")


    def on_other_2_toggled(self ):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.labelPage.setText("Others Page")

    def addItemRadar(self):
        self.ui.radarBox.clear()
        for i in range(0,10):
            opt = "test add item file " + str(i)
            self.ui.radarBox.addItem(opt)
        # self.ui.radarBox.setCurrentIndex(-1)

    def addItemDate(self):
        self.ui.dateBox.clear()
        for i in range(0,10):
            opt = "test add item date " + str(i)
            self.ui.dateBox.addItem(opt)

    def addItemFile(self):
        self.ui.fileBox.clear()
        self.ui.fileBox.addItem("All files") # option select all files
        for i in range(0,10):
            opt = "test add item  file" + str(i)
            self.ui.fileBox.addItem(opt)

    def addItemMode(self):
        self.ui.modeBox.clear()
        for i in range(0,10):
            opt = "test add item mode " + str(i)
            self.ui.modeBox.addItem(opt)

    def getRadar(self):
        #! get value of radar
        self.radar_index = self.ui.radarBox.currentText()
        self.ui.radarBox.itemData(self.radar_index)
    def getDate(self):
        #! get value of date
        self.date_index = self.ui.dateBox.currentText()
        self.ui.dateBox.itemData(self.date_index)
    def getFile(self):
        #! get value of file
        self.file_index = self.ui.fileBox.currentText()
        self.ui.fileBox.itemData(self.file_index)
    def getMode(self):
        #! get value of mode
        self.mode_index = self.ui.modeBox.currentText()
        self.ui.modeBox.itemData(self.mode_index)
    def getIsGrid(self):
        self.isGrid = self.ui.IsGrid.isChecked()  # -> bool
    def getThreshHold(self):
        self.threshHold = self.ui.threshHold.text() 
    # write a function get value of file

    def initGL(self):
        self.glWidget = GLWidget(self)
        self.ui.verticalLayout_6.replaceWidget(self.ui.openGLWidget, self.glWidget)
        self.ui.slider_3d_x.valueChanged.connect(lambda val: self.glWidget.setRotX(val))
        self.ui.slider_3d_x.valueChanged.connect(lambda : self.updateSlider())
        self.ui.slider_3d_x.setMaximum(115)

        self.ui.slider_3d_y.valueChanged.connect(lambda val: self.glWidget.setRotY(val))
        self.ui.slider_3d_y.valueChanged.connect(lambda : self.updateSlider())
        self.ui.slider_3d_y.setMaximum(115)

        self.ui.slider_3d_z.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        self.ui.slider_3d_z.valueChanged.connect(lambda : self.updateSlider())
        self.ui.slider_3d_z.setMaximum(115)
    def updateSlider(self):
        tmp_value = [self.ui.slider_3d_x.value() * np.pi, 
                     self.ui.slider_3d_y.value() * np.pi,
                     self.ui.slider_3d_z.value() * np.pi]
        for i in range(0,3):
            if tmp_value[i] >= 360:
                tmp_value[i] = 360 - tmp_value[i]
        self.ui.x_value.setText(str(int(tmp_value[0])) + "°")
        self.ui.y_value.setText(str(int(tmp_value[1])) + "°")
        self.ui.z_value.setText(str(int(tmp_value[2])) + "°")

    def initHomePage(self):
        self.ui.changeDirData.clicked.connect(lambda: self.chooseDir())

    def chooseDir(self):
        self.dataDir = QFileDialog.getExistingDirectory()
        self.ui.curData.setText(self.dataDir)


def loadStyle(QApplication):
    """
    load style file for application
    Args:
        QApplication (QtGui.QGuiApplication): our application
    """
    style_file = QFile("./style/style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    QApplication.setStyleSheet(style_stream.readAll())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loadStyle(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
