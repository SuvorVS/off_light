import os

from MainWindowUI import Ui_MainWindow as MainWindowUI
from Game import *

from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem, QMessageBox
from PyQt5.QtCore import QModelIndex, QRectF, Qt

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self._game = Game(7, 7)
        self.game_resize(self._game)

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.gameFieldTableView.setItemDelegate(MyDelegate(self))

        def new_mouse_press_event(e: QMouseEvent) -> None:
            idx = self.gameFieldTableView.indexAt(e.pos())
            self.on_item_clicked(idx, e)

        self.gameFieldTableView.mousePressEvent = new_mouse_press_event

        self.newGamePushButton.clicked.connect(self.on_new_game)
        self.newGamePushButtonEasy.clicked.connect(self.on_new_game_easy)

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(game.row_count, game.col_count)
        self.gameFieldTableView.setModel(model)
        self.update_view()

    def update_view(self):
        self.gameFieldTableView.viewport().update()

    def on_new_game(self):
        self._game = Game(self._game.row_count, self._game.col_count)
        self.game_resize(self._game)
        self.update_view()

    def on_new_game_easy(self):
        self._game = Game(self._game.row_count, self._game.col_count)
        self._game.set_size(3,3)
        self.game_resize(self._game)
        self.update_view()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        item = self._game[e.row(), e.column()]
        if item is True:
            img = self._images['lamp']
        elif item is False:
            img = self._images['l']
        img.render(painter, QRectF(option.rect))

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton:
            self._game.left_mouse_click(e.row(), e.column())
            if self._game._state == self._game.state.WIN:
                QMessageBox.about(self, "Game", "You win")
        self.update_view()



