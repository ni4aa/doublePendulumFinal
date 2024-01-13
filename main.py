import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QSlider, QLabel, QCheckBox
from PyQt6.QtGui import QPainter, QPen, QBrush, QIcon, QPixmap
from PyQt6.QtCore import Qt


m1 = 10
m2 = 10
x = 0
l = 100
phi = 0
dphi = 0
dx = 0
g = 9.8067
tau = 0.05
flag_human = True
flag_trajectory = True


def d2x(m1, m2, l, phi, dphi):
    return -m2 * (g * cos(phi) * sin(phi) + l * sin(phi) * dphi**2) / (m2 * cos(phi)**2 - m2 - m1)


def d2phi(m1, m2, l, phi, dphi):
    return -((-g * m1 * sin(phi) - g * m2 * sin(phi) - l * m2 * cos(phi) * sin(phi) * dphi**2) /
             (l * (m2 * cos(phi)**2 - m2 - m1)))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon("icons.ico"))
        self.setWindowTitle('Menu')
        self.setMinimumWidth(300)
        self.setMinimumHeight(350)


        self.simulation = QPushButton(self)
        self.simulation.setGeometry(QtCore.QRect(50, 30, 200, 70))
        self.simulation.setToolTip("Запуск симуляции")
        self.simulation_label = QLabel(self.simulation)
        self.simulation_label.setPixmap(QPixmap("play.png"))
        self.simulation_label.setGeometry(QtCore.QRect(85, 20, 30, 30))
        #self.simulation.setText("simulation")
        self.simulation.clicked.connect(self.show_simulation)

        self.phase = QPushButton(self)
        self.phase.setGeometry(QtCore.QRect(50, 120, 200, 70))
        self.phase.setToolTip("Фазовые портреты")
        self.phase_label = QLabel(self.phase)
        self.phase_label.setPixmap(QPixmap("маятник.png"))
        self.phase_label.setGeometry(QtCore.QRect(85, 20, 30, 30))
        #self.phase.setText("Фазовые портреты")
        self.phase.clicked.connect(self.show_phase)

        self.settings = QPushButton(self)
        self.settings.setGeometry(QtCore.QRect(50, 210, 200, 70))
        self.settings.setToolTip("Настройка параметров маятника")
        self.settings_label = QLabel(self.settings)
        self.settings_label.setPixmap(QPixmap("settings.png"))
        self.settings_label.setGeometry(QtCore.QRect(85, 20, 30, 30))
        #self.settings.setText("settings")
        self.settings.clicked.connect(self.show_setting)

    def show_simulation(self):
        self.w_simulation = SimulationWindow()
        self.w_simulation.show()

    def show_phase(self):
        fig, ax = plt.subplots(1, 3, figsize=(15.5, 7.5))
        phi_matrix = np.linspace(0, radians(180), 18)
        for phi_now in phi_matrix:
            phi = [phi_now]
            dphi = [0]
            x = [0]
            dx = [0]
            for time in np.arange(0, 3.14, 0.01):
                dphi.append(dphi[-1] + 0.01 * d2phi(1, 1, 1, phi[-1], dphi[-1]))
                dx.append(dx[-1] + 0.01 * d2x(1, 1, 1, phi[-1], dphi[-1]))
                x.append(x[-1] + 0.01 * dx[-1])
                phi.append(phi[-1] + 0.01 * dphi[-1])

            ax[0].plot(phi, dphi)
            ax[0].set_title("Зависимость dphi от phi")
            ax[1].plot(phi, x)
            ax[1].set_title("Зависимость x от phi")
            ax[2].plot(phi, dx)
            ax[2].set_title("Зависимость dx от phi")
            plt.xlim(-15, 15)

        plt.show()

        fig, ax = plt.subplots(1, 3, figsize=(15.5, 7.5))
        dphi_matrix = np.linspace(0, radians(400), 20)
        for dphi_now in dphi_matrix:
            dphi = [dphi_now]
            phi = [0]
            x = [0]
            dx = [0]
            for time in np.arange(0, 3.14, 0.01):
                dphi.append(dphi[-1] + 0.01 * d2phi(1, 1, 1, phi[-1], dphi[-1]))
                dx.append(dx[-1] + 0.01 * d2x(1, 1, 1, phi[-1], dphi[-1]))
                x.append(x[-1] + 0.01 * dx[-1])
                phi.append(phi[-1] + 0.01 * dphi[-1])

            ax[0].plot(dphi, phi)
            ax[0].set_title("Зависимость phi от dphi")
            ax[1].plot(dphi, x)
            ax[1].set_title("Зависимость x от dphi")
            ax[2].plot(dphi, dx)
            ax[2].set_title("Зависимость dx от dphi")
            plt.xlim(-15, 15)

        plt.show()

    def show_setting(self):
        self.w_settings = SettingsWindow()
        self.w_settings.show()


class SimulationWindow(QWidget):
    def __init__(self):
        super(SimulationWindow, self).__init__()
        self.setWindowTitle('Simulation')
        self.showMaximized()
        self.setWindowIcon(QIcon('play.png'))
        self.timer = QtCore.QTimer(self)  #cоздаем таймер
        self.timer.timeout.connect(self.update)  #говорим что будет происходит, когда таймер закончится, self.update обновляет экран => вызывает paintEvent еще раз
        self.timer.start(20)  #задаем что милисекунды для таймера
        self.m1 = m1
        self.m2 = m2
        self.x = x
        self.l = l
        self.phi = phi
        self.dphi = dphi
        self.dx = dx
        self.phi_matrix = [phi]
        self.x_matrix = [x]

    def paintEvent(self, e): #в конце создания окошка рисует на нем
        #расчеты
        self.dphi = self.dphi + tau * d2phi(self.m1, self.m2, self.l, self.phi, self.dphi)  # dphi - скорость угла поворта
        self.dx = self.dx + tau * d2x(self.m1, self.m2, self.l, self.phi, self.dphi)  # dx - скорость x
        self.x = self.x + self.dx * tau  # координата в этот момент времени
        self.phi = self.phi + self.dphi * tau
        self.phi_matrix.append(self.phi)
        self.x_matrix.append(self.x)
        #рисуем, потом точно объясню как рисует
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))

        if flag_trajectory:
            self.draw_trajectory(painter)

        u1, v1 = self.uv(self.x, 0)
        u2, v2 = self.uv(self.x + self.l * sin(self.phi), -l * cos(self.phi))
        r1 = int(15 + m1 * 30 / 100)
        r2 = int(15 + m2 * 30 / 100)

        painter.drawLine(u1, v1, u2, v2)
        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.red, Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(int(u1 - r1 / 2), int(v1 - r1 / 2), r1, r1)
        painter.setBrush(QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.SolidPattern))

        if flag_human:
            self.draw_human(painter, u2, v2, self.x, self.l, self.phi)
        else:
            painter.drawEllipse(int(u2 - r2 / 2), int(v2 - r2 / 2), r2, r2)

    def draw_trajectory(self, painter):
        for i in range(1, len(self.phi_matrix)):
            u1, v1 = self.uv(self.x_matrix[i-1] + self.l * sin(self.phi_matrix[i-1]), -l * cos(self.phi_matrix[i-1]))
            u2, v2 = self.uv(self.x_matrix[i] + self.l * sin(self.phi_matrix[i]), -l * cos(self.phi_matrix[i]))

            painter.drawLine(u1, v1, u2, v2)

    def draw_human(self, painter, u2, v2, x, l, phi):
        u, v = self.uv(x + (l+60) * sin(phi), -(l+60) * cos(phi))

        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))
        painter.drawLine(u2, v2, u, v)

        u, v = self.uv(x + (l + 20) * sin(phi), -(l + 20) * cos(phi))
        u_hand, v_hand = self.uv(x + (l+20) * sin(phi) - 30 * sin(radians(45) - phi),
                                 -(l+20) * cos(phi) - 30 * cos(radians(45)-phi))

        painter.drawLine(u, v, u_hand, v_hand)
        u_hand, v_hand = self.uv(x + (l+20) * sin(phi) + 30 * sin(radians(45) + phi),
                                 -(l+20) * cos(phi) - 30 * cos(radians(45)+phi))

        painter.drawLine(u, v, u_hand, v_hand)

        u, v = self.uv(x + (l + 60) * sin(phi), -(l + 60) * cos(phi))
        u_leg, v_leg = self.uv(x + (l + 60) * sin(phi) - 30 * sin(radians(30) - phi),
                               -(l + 60) * cos(phi) - 30 * cos(radians(30) - phi))

        painter.drawLine(u, v, u_leg, v_leg)

        u_leg, v_leg = self.uv(x + (l + 60) * sin(phi) + 30 * sin(radians(30) + phi),
                               -(l + 60) * cos(phi) - 30 * cos(radians(30) + phi))

        painter.drawLine(u, v, u_leg, v_leg)
        painter.drawEllipse(int(u2 - 12), int(v2 - 12), 25, 25)

    def uv(self, x, y):
        u = int(self.size().width()/2 + x)
        v = int(self.size().height()/2 - y)
        return u, v


class SettingsWindow(QWidget):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.setWindowTitle('Settings')
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        self.setWindowIcon(QIcon('settings.png'))

        self.m1_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.m1_slider.setGeometry(QtCore.QRect(100, 30, 200, 25))
        self.m1_slider.setMinimum(1)
        self.m1_slider.setMaximum(100)
        self.m1_slider.setValue(m1)
        self.m1_slider.valueChanged.connect(self.m1_value_change)

        self.m1_text = QLabel("m1", self)
        self.m1_text.move(50, 30)
        self.m1_value = QLabel(str(m1), self)
        self.m1_value.move(320, 30)
        self.m1_value.adjustSize()

        self.m2_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.m2_slider.setGeometry(QtCore.QRect(100, 80, 200, 25))
        self.m2_slider.setMinimum(1)
        self.m2_slider.setMaximum(100)
        self.m2_slider.setValue(m2)
        self.m2_slider.valueChanged.connect(self.m2_value_change)

        self.m2_text = QLabel("m2", self)
        self.m2_text.move(50, 80)
        self.m2_value = QLabel(str(m2), self)
        self.m2_value.move(320, 80)
        self.m2_value.adjustSize()

        self.l_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.l_slider.setGeometry(QtCore.QRect(100, 130, 200, 25))
        self.l_slider.setMinimum(20)
        self.l_slider.setMaximum(200)
        self.l_slider.setValue(l)
        self.l_slider.valueChanged.connect(self.l_value_change)

        self.l_text = QLabel("l", self)
        self.l_text.move(50, 130)
        self.l_value = QLabel(str(l), self)
        self.l_value.move(320, 130)
        self.l_value.adjustSize()

        self.phi_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.phi_slider.setGeometry(QtCore.QRect(100, 180, 200, 25))
        self.phi_slider.setMinimum(-180)
        self.phi_slider.setMaximum(180)
        phi_degrees = int(round(degrees(phi)))
        self.phi_slider.setValue(phi_degrees)
        self.phi_slider.valueChanged.connect(self.phi_value_change)

        self.phi_text = QLabel("phi", self)
        self.phi_text.move(50, 180)
        self.phi_value = QLabel(str(phi_degrees), self)
        self.phi_value.move(320, 180)
        self.phi_value.adjustSize()

        self.dphi_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.dphi_slider.setGeometry(QtCore.QRect(100, 230, 200, 25))
        self.dphi_slider.setMinimum(-400)
        self.dphi_slider.setMaximum(400)
        dphi_degrees = int(round(degrees(dphi)))
        self.dphi_slider.setValue(dphi_degrees)
        self.dphi_slider.valueChanged.connect(self.dphi_value_change)

        self.dphi_text = QLabel("dphi", self)
        self.dphi_text.move(50, 230)
        self.dphi_value = QLabel(str(dphi_degrees), self)
        self.dphi_value.move(320, 230)
        self.dphi_value.adjustSize()

        self.checker_human = QCheckBox("Human", self)
        self.checker_human.stateChanged.connect(self.check_human)
        self.checker_human.setGeometry(QtCore.QRect(50, 280, 100, 20))
        if flag_human:
            self.checker_human.toggle()

        self.checker_trajectory = QCheckBox("Trajectory", self)
        self.checker_trajectory.stateChanged.connect(self.check_trajectory)
        self.checker_trajectory.setGeometry(QtCore.QRect(50, 300, 100, 20))
        if flag_trajectory:
            self.checker_trajectory.toggle()

        self.reset_button = QPushButton(self)
        self.reset_button.setGeometry(QtCore.QRect(250, 280, 100, 40))
        self.reset_button.setText("Reset")
        self.reset_button.clicked.connect(self.reset)

    def reset(self):
        global m1, m2, l, phi, dphi
        m1 = 10
        m2 = 10
        l = 100
        phi = 0
        dphi = 0
        self.m1_slider.setValue(m1)
        self.m2_slider.setValue(m2)
        self.l_slider.setValue(l)
        self.phi_slider.setValue(phi)
        self.dphi_slider.setValue(dphi)

    @staticmethod
    def check_human(value):
        state = Qt.CheckState(value)
        global flag_human
        flag_human = (state == Qt.CheckState.Checked)

    @staticmethod
    def check_trajectory(value):
        state = Qt.CheckState(value)
        global flag_trajectory
        flag_trajectory = (state == Qt.CheckState.Checked)

    def m1_value_change(self):
        global m1
        m1 = self.m1_slider.value()
        self.m1_value.setNum(m1)
        self.m1_value.adjustSize()

    def m2_value_change(self):
        global m2
        m2 = self.m2_slider.value()
        self.m2_value.setNum(m2)
        self.m2_value.adjustSize()

    def l_value_change(self):
        global l
        l = self.l_slider.value()
        self.l_value.setNum(l)
        self.l_value.adjustSize()

    def phi_value_change(self):
        global phi
        phi_angle = self.phi_slider.value()
        self.phi_value.setNum(phi_angle)
        phi = radians(phi_angle)
        self.phi_value.adjustSize()

    def dphi_value_change(self):
        global dphi
        dphi_angle = self.dphi_slider.value()
        self.dphi_value.setNum(dphi_angle)
        dphi = radians(dphi_angle)
        self.dphi_value.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
