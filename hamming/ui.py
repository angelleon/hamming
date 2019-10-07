#!/usr/bin/env pyhon3

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFormLayout, QHBoxLayout, QLabel,\
                            QLineEdit, QPushButton, QComboBox, QPlainTextEdit, QRadioButton, QTextEdit
from PyQt5.QtCore import QSize, QRect, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPaintEvent, QResizeEvent, QFont, QColor, QTextFormat, QPainter, QTextBlock, QFontDatabase
from logging import basicConfig, getLogger, DEBUG

basicConfig(level=DEBUG, format="[%(levelname)-8.8s]:\t[%(name)-10.10s]:%(funcName)-20.20s:%(lineno)4d:\t%(message)s")
log = getLogger(__name__)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        log.debug("Constructor")
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        log.debug("")
        digits = 1
        max_value = max((1, self.blockCount()))
        while max_value >= 10:
            max_value //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance("9") * digits
        # print(space)
        return space

    def line_number_area_paint_event(self, event: QPaintEvent):
        log.debug("")
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        log.debug(top)
        log.debug(bottom)

        # print(block.isValid(), top <= event.rect().bottom())
        # print(block.isVisible(), bottom >= event.rect().top())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                # print(number)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(), Qt.AlignRight,
                                 number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def resizeEvent(self, event: QResizeEvent):
        log.debug("")
        # log.debug(dir(super()))
        # print(type(super()))
        # super(CodeEditor, self).resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    @pyqtSlot(int)
    def update_line_number_area_width(self, new_block_count):
        log.debug("")
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @pyqtSlot()
    def highlight_current_line(self):
        log.debug("")
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    @pyqtSlot(QRect, int)
    def update_line_number_area(self, rect: QRect, dy: int):
        log.debug("")
        if dy != 0:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)


class LineNumberArea(QWidget):
    def __init__(self, code_editor: CodeEditor):
        super().__init__(code_editor)
        log.debug("Constructor")
        self.code_editor = code_editor

    def sizeHint(self):
        log.debug("")
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event: QPaintEvent):
        log.debug("")
        print("painting")
        self.code_editor.line_number_area_paint_event(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        fnt_monospaced = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.setFont(fnt_monospaced)

        wdgt_main = QWidget()
        lyt_main = QVBoxLayout()
        wdgt_main.setLayout(lyt_main)
        self.setCentralWidget(wdgt_main)

        wdgt_form = QWidget()
        lyt_form = QFormLayout()
        wdgt_form.setLayout(lyt_form)

        txt_ip = QLineEdit()
        txt_port = QLineEdit()
        cmb_protocol = QComboBox()
        cmb_protocol.addItems(("TCP", "UDP"))

        lyt_form.addRow("IP", txt_ip)
        lyt_form.addRow("Port", txt_port)
        lyt_form.addRow("Protocol", cmb_protocol)

        lyt_main.addWidget(wdgt_form)

        wdgt_editor = CodeEditor()
        lyt_main.addWidget(wdgt_editor)
        wdgt_editor = CodeEditor()
        wdgt_editor.setEnabled(False)
        lyt_main.addWidget(wdgt_editor)

        wdgt_rdio = QWidget()
        lyt_rdio = QHBoxLayout()
        wdgt_rdio.setLayout(lyt_rdio)
        rdio_send = QRadioButton("Send")
        rdio_recv = QRadioButton("Recive")
        rdio_send.setChecked(True)
        rdio_send.toggled.connect(self.slt_rdio_change)
        lyt_rdio.addWidget(rdio_send)
        lyt_rdio.addWidget(rdio_recv)

        lyt_main.addWidget(wdgt_rdio)

        self.btn_action = QPushButton("Send msg ==>")
        lyt_main.addWidget(self.btn_action)

    @pyqtSlot(bool)
    def slt_rdio_change(self, checked):
        if checked:
            self.btn_action.setText("Send msg ==>")
        else:
            self.btn_action.setText("Recive msg <==")


class Application(QApplication):
    def __init__(self):
        super().__init__([])
        self.w = MainWindow()
        self.w.show()


def main():
    a = Application()
    return a.exec()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")

