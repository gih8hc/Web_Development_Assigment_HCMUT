from PyQt5 import QtCore      # core Qt functionality
from PyQt5 import QtWidgets       # extends QtCore with GUI functionality
from PyQt5 import QtOpenGL    # provides QGLWidget, a special OpenGL QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QAction, QMenu, QPushButton
import OpenGL.GL as gl        # python wrapping of OpenGL
from OpenGL import GLU        # OpenGL Utility Library, extends OpenGL functionality
from PyQt5.QtCore import Qt
import sys                    # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np
from Radar import *


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None, index = 0, threshold = 0):
        self.parent = parent
        super().__init__(parent)
        self.setUpRadar(index=index)
        self.setUpThreshold(threshold)
        self.setUpScale()
        self.teapot_pos = [0, 0] 
        self.zoom_center = [0, 0] 
        self.scale = 1.0
    def setUpScale(self, val=1.0):
        self.scale = val

    def setUpRadar(self, index = 0,filePath: str = DIRECTORY.FILE_PATH, radarName: str = DIRECTORY.RADAR_NAME, date: str = DIRECTORY.YEAR + DIRECTORY.MONTH + DIRECTORY.DATE, mode: str = DIRECTORY.MODE):
        self.radar = Radar(index, filePath, radarName, date, mode)

    def resetRadar(self, index = 0,filePath: str = DIRECTORY.FILE_PATH, radarName: str = DIRECTORY.RADAR_NAME, date: str = DIRECTORY.YEAR + DIRECTORY.MONTH + DIRECTORY.DATE, mode: str = DIRECTORY.MODE):
        del self.radar
        self.radar = Radar(index, filePath, radarName, date, mode)

    def setUpThreshold(self, threshold = 0):
        self.threshold = threshold

    def update(self, index=None, threshold=None, clutterFilter = None):
        if index is not None:
            self.radar.update(index)
        if threshold is not None:
            self.threshold = threshold
        if clutterFilter is not None:
            self.radar.isFilterClutter(clutterFilter)

        self.setUpVBO()

    def initializeGL(self):
        self.qglClearColor(QColor(0, 0, 0))    # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)                  # enable depth testing

        self.setUpVBO()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()    # push the current matrix to the current stack
        gl.glTranslate(self.teapot_pos[0], self.teapot_pos[1], -5.0)    # third, translate cube to specified depth
        gl.glTranslatef(self.zoom_center[0], self.zoom_center[1],  0) 

        gl.glScale(self.scale, self.scale, self.scale)       # second, scale cube
        gl.glTranslatef(-self.zoom_center[0], -self.zoom_center[1], 0)
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        self.vertVBO.bind()
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)

        self.colorVBO.bind()
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, None)

        gl.glDrawElements(gl.GL_POINTS, len(self.indexArray), gl.GL_UNSIGNED_INT, self.indexArray)

        # Unbind and disable after drawing
        self.vertVBO.unbind()
        self.colorVBO.unbind()
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        
        gl.glPopMatrix()    # restore the previous modelview matrix

    def setUpVBO(self):

        v = self.radar.get_all_vertices_by_threshold(self.threshold)
        self.vertices = v['position']
        self.vertVBO = vbo.VBO(np.reshape(self.vertices,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.color = v['color']
        self.colorVBO = vbo.VBO(np.reshape(self.color,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.indexArray = np.array(range(len(self.vertices)))

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

