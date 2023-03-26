import os
import sys
from PyQt5 import QtGui, QtCore, QtWebEngineWidgets
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPen, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QRadioButton, QMessageBox, QLabel, \
    QAbstractButton, QButtonGroup
from game import Game, CellType
from PyQt5.QtCore import Qt
from os.path import exists


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.game = Game()
        self.restart_level_button = QPushButton('Restart', self)
        # Game.load_level(r'levels\level_3.txt', self.game)
        self.current_level_name = ''
        self.human_img = QPixmap('images/man_1.png')
        self.ground_img = QPixmap('images/ground_1.png')
        self.wall_img = QPixmap('images/wall_1.png')
        self.box_img = QPixmap('images/box_1.png')
        self.target_img = QPixmap('images/target.png')
        self.box_on_target_img = QPixmap('images/box_on_target_1.png')
        self.button_rules = QPushButton('Правила', self)
        self.button_options = QPushButton('Настройки', self)
        self.button_load_level = QPushButton('Загрузка', self)
        self.steps_label = QLabel('Steps: 0', self)
        self.max_moves = 1000000
        self.init_ui()
        self.show()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.game.level_complete:
            return
        if a0.key() in (QtCore.Qt.Key_A, QtCore.Qt.Key_Left):
            self.game.command_left()
            self.update()
        elif a0.key() in (QtCore.Qt.Key_D, QtCore.Qt.Key_Right):
            self.game.command_right()
            self.update()
        elif a0.key() in (QtCore.Qt.Key_W, QtCore.Qt.Key_Up):
            # print('up')
            self.game.command_up()
            self.update()
        elif a0.key() in (QtCore.Qt.Key_S, QtCore.Qt.Key_Down):
            self.game.command_down()
            self.update()
        self.steps_label.setText('Steps: ' + str(self.game.n_steps))
        if self.game.check_level_victory():
            m_box = QMessageBox()
            m_box.setText('  ...Уровень завершён!!!...  ')
            m_box.setWindowTitle('Сообщение от игры')
            m_box.exec()
            self.game.level_complete = True
        else:
            if self.game.n_steps >= self.max_moves:
                m_box = QMessageBox()
                m_box.setText('        ...!!!Game over!!!...       ')
                m_box.setWindowTitle('Сообщение от игры')
                m_box.exec()
                exit()

    def init_ui(self):
        self.button_rules.move(100, 0)
        self.button_load_level.move(200, 0)
        self.steps_label.setGeometry(350, 0, 250, 50)
        self.steps_label.setFont(QFont('Arial', 16))
        self.button_rules.clicked.connect(self.on_rules_button_clicked)
        self.button_options.clicked.connect(self.on_options_button_clicked)
        self.button_load_level.clicked.connect(self.on_load_level_button_clicked)
        self.restart_level_button.clicked.connect(self.on_restart_level_button_clicked)
        self.setWindowTitle('Sokoban')
        self.setGeometry(100, 100, 700, 700)
        self.restart_level_button.setFixedWidth(150)
        self.restart_level_button.setFixedHeight(25)
        self.restart_level_button.move(self.width() - 160, self.height() - 30)
        self.restart_level_button.setVisible(False)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if len(self.game.field) == 0:
            return

        # wall_color = QColor(100, 100, 100)
        # ground_color = QColor(200, 50, 50)
        # box_color = QColor(100, 100, 200)
        # box_on_target_color = QColor(100, 200, 100)
        # man_color = QColor(0, 0, 0)
        # target_color = QColor(255, 255, 255)

        qp = QPainter()
        qp.begin(self)

        for k in range(len(self.game.field)):
            for k2 in range(len(self.game.field[k])):
                x = self.game.field[k][k2]
                # print(x)
                if x == CellType.EMPTY.value:
                    continue
                elif x == CellType.GROUND.value:
                    # print('ground')
                    qp.drawPixmap(10 + k2 * 56, 100 + k * 56, self.ground_img)
                    # qp.fillRect(10 + k2 * 50, 100 + k * 50, 50, 50, ground_color)
                else:
                    qp.drawPixmap(10 + k2 * 56, 100 + k * 56, self.wall_img)
                    # qp.fillRect(10 + k2 * 50, 100 + k * 50, 50, 50, wall_color)
        qp.setPen(QPen(Qt.green, 3))
        for i in self.game.targets:
            qp.drawPixmap(10 + i[0] * 56, 100 + i[1] * 56, self.target_img)
            # qp.drawLine(20 + i[0] * 56, 110 + i[1] * 56, 10 + i[0] * 56 + 40, 100 + i[1] * 56 + 40)
            # qp.drawLine(20 + i[0] * 56, 100 + i[1] * 56 + 40, 10 + i[0] * 56 + 40, 110 + i[1] * 56)
        for i in self.game.boxes:
            if i in self.game.targets:
                qp.drawPixmap(10 + i[0] * 56, 100 + i[1] * 56, self.box_on_target_img)
                # qp.fillRect(15 + i[0] * 50, 105 + i[1] * 50, 40, 40, box_on_target_color)
            else:
                # qp.fillRect(15 + i[0] * 50, 105 + i[1] * 50, 40, 40, box_color)
                qp.drawPixmap(10 + i[0] * 56, 100 + i[1] * 56, self.box_img)
        qp.drawPixmap(10 + self.game.x * 56, 100 + self.game.y * 56, self.human_img)
        # qp.setBrush(man_color)
        # qp.drawEllipse(20 + self.game.x * 50, 110 + self.game.y * 50, 30, 30)
        qp.end()

    def on_rules_button_clicked(self):
        rules = RulesWindow(self)
        rules.show()

    def on_options_button_clicked(self):
        options = OptionsWindow(self)
        options.show()

    def on_load_level_button_clicked(self):
        load = LoadWindow(self)
        load.show()

    def on_restart_level_button_clicked(self):
        # print(self.current_level_name)
        Game.load_level(self.current_level_name, self.game)
        self.steps_label.setText('Steps: 0')
        self.game.level_complete = False
        self.update()


class RulesWindow(QMainWindow):
    def __init__(self, parent=None):
        super(RulesWindow, self).__init__(parent)
        self.web_info = QtWebEngineWidgets.QWebEngineView(self)
        self.web_info.setGeometry(0, 0, 800, 800)
        self.web_info.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0] + r'\data.html'))
        self.setWindowTitle('Правила')
        self.setGeometry(200, 200, 800, 800)


class OptionsWindow(QMainWindow):
    def __init__(self, parent=None):
        super(OptionsWindow, self).__init__(parent)
        layout = QHBoxLayout()
        self.master = parent
        self.setWindowTitle('Выберите свою сложность')
        self.rb1 = QRadioButton('Новичок (без ограничений)', self)
        self.rb1.setFixedWidth(500)
        self.rb2 = QRadioButton('Средний (до 100 шагов)', self)
        self.rb2.setFixedWidth(500)
        self.rb3 = QRadioButton('Эксперт (до 50 шагов)', self)
        self.rb3.setFixedWidth(500)
        self.rb1.setChecked(True)
        self.save_button = QPushButton('Сохранить настройки', self)
        # self.save_button.setFixedWidth(100)
        layout.addWidget(self.rb1)
        layout.addWidget(self.rb2)
        layout.addWidget(self.rb3)
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.setLayout(layout)
        self.rb1.move(100, 50)
        self.rb2.move(100, 100)
        self.rb3.move(100, 150)
        # self.save_button.move(150, 200)
        self.setGeometry(200, 200, 400, 400)
        self.save_button.setGeometry(self.width() // 2 - 100, 220, 200,
                                     self.save_button.geometry().height())

    def on_save_button_clicked(self):
        if self.rb1.isChecked():
            # print('red')
            self.master.max_moves = 1000000
        elif self.rb2.isChecked():
            # print('blue')
            self.master.max_moves = 100
        else:
            self.master.max_moves = 50
            # print('green')
        self.close()


class LoadWindow(QMainWindow):
    def __init__(self, parent=None):
        super(LoadWindow, self).__init__(parent)
        self.master = parent
        self.setWindowTitle('Уровни')
        self.setGeometry(200, 200, 400, 400)
        # self.cur_mouse_x = 0
        # self.cur_mouse_y = 0
        # self.level_1_button = QPushButton('Уровень 1', self)
        # self.level_1_button.setCheckable(True)
        # self.level_2_button = QPushButton('Уровень 2', self)
        # self.level_2_button.setCheckable(True)
        # self.level_3_button = QPushButton('Уровень 3', self)
        # self.level_3_button.setCheckable(True)
        # self.level_4_button = QPushButton('Уровень 4', self)
        # self.level_5_button = QPushButton('Уровень 5', self)
        # self.level_2_button.move(100, 0)
        # self.level_3_button.move(200, 0)
        # self.level_4_button.move(300, 0)
        # self.level_5_button.move(0, 30)
        self.level_group = QButtonGroup(self)
        self.level_buttons = []
        for i in range(100):
            s = f'levels\\level_{i + 1}.txt'
            if not exists(s):
                break
            b = QPushButton('Уровень ' + str(i + 1), self)
            b.setFixedWidth(96)
            b.setFixedHeight(25)
            b.move((i % 4) * 100 + 2, (i // 4) * 30 + 2)
            self.level_buttons.append(b)
            self.level_group.addButton(b)
            b.setCheckable(True)
        self.level_launch = QPushButton('Начать уровень', self)
        self.level_launch.setGeometry(100, 300, 200, 32)
        self.level_launch.clicked.connect(self.on_level_button_clicked)
        # self.level_group.addButton(self.level_1_button)
        # self.level_group.addButton(self.level_2_button)
        # self.level_group.addButton(self.level_3_button)
        # self.level_1_button.clicked.connect(self.on_level_button_clicked)
        # self.level_2_button.clicked.connect(self.on_level_button_clicked)
        # self.setMouseTracking(True)

    def on_level_button_clicked(self):
        level_index = -1
        for k in range(len(self.level_buttons)):
            if self.level_buttons[k].isChecked():
                level_index = k
                break
        if level_index == -1:
            m_box = QMessageBox()
            m_box.setText('     Вы не выбрали уровень      ')
            m_box.setWindowTitle('Сообщение от игры')
            m_box.exec()
        else:
            s = f'levels\\level_{level_index + 1}.txt'
            self.master.current_level_name = s
            Game.load_level(s, self.master.game)
            self.master.restart_level_button.setVisible(True)
            self.close()

    # def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
    #     self.cur_mouse_x = a0.x()
    #     self.cur_mouse_y = a0.y()

    # def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
    #     self.cur_mouse_x = a0.x()
    #     self.cur_mouse_y = a0.y()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
