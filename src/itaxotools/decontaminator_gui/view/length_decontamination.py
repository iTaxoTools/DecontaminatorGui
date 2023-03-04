# -----------------------------------------------------------------------------
# DecontaminatorGui - GUI for Decontaminator
# Copyright (C) 2023  Patmanidis Stefanos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from PySide6 import QtCore, QtGui, QtWidgets

from pathlib import Path

from itaxotools.common.utility import AttrDict, override

from .. import app
from ..utility import Guard, Binder, type_convert, human_readable_size
from ..model.common import Item, ItemModel
from ..types import ColumnFilter, Notification, AlignmentMode, PairwiseComparisonConfig, StatisticsGroup, AlignmentMode, PairwiseScore, DistanceMetric
from .common import Card, CardCustom, NoWheelRadioButton, NoWheelComboBox, GLineEdit, ObjectView, TaskView, RadioButtonGroup, RichRadioButton, MinimumStackedWidget, VerticalRollAnimation

from ..types import ComparisonMode, DecontaminateMode, Notification, DecontaminateMode
from ..types.length_decontamination import Mode, Symbol
from .common import (
    Card, ComparisonModeSelector, GLineEdit, GSpinBox, ObjectView, TextEditLogger)


class TitleCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = QtWidgets.QLabel()
        title.setStyleSheet("""font-size: 18px; font-weight: bold; """)

        description = QtWidgets.QLabel(
            'Deleting sequences that have too much noninformation data.')
        description.setWordWrap(True)

        contents = QtWidgets.QVBoxLayout()
        contents.addWidget(title)
        contents.addWidget(description)
        contents.addStretch(1)
        contents.setSpacing(6)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.addLayout(contents, 1)
        self.addLayout(layout)

        self.controls.title = title

    def setTitle(self, text):
        self.controls.title.setText(text)

    def setBusy(self, busy: bool):
        self.setEnabled(True)


class InputSelector(Card):
    changedPath = QtCore.Signal(Path)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QtWidgets.QLabel('Input directory:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        edit = QtWidgets.QLineEdit('---')
        edit.setReadOnly(True)

        browse = QtWidgets.QPushButton('Browse')
        browse.clicked.connect(self.handleBrowse)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit, 1)
        layout.addWidget(browse)
        layout.setSpacing(16)
        self.addLayout(layout)

        self.controls.edit = edit

    def setPath(self, path):
        if path is None:
            path = '---'
        self.controls.edit.setText(str(path))

    def handleBrowse(self, *args):
        dir = self.parent().getExistingDirectory('Browse Directory')
        if not dir:
            return
        self.changedPath.emit(Path(dir))


class ModeSelector(Card):
    changedMode = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QtWidgets.QLabel('Mode:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        description = QtWidgets.QLabel(
            'Defines if internal branches or terminal branches are analyzed.')
        description.setWordWrap(True)

        radio_percentage = QtWidgets.QRadioButton('Percentage')
        radio_absolute = QtWidgets.QRadioButton('Absolute')

        group = RadioButtonGroup()
        group.add(radio_percentage, Mode.Percentage)
        group.add(radio_absolute, Mode.Absolute)
        group.valueChanged.connect(self.changedMode)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(radio_percentage)
        layout.addWidget(radio_absolute)
        layout.addStretch(1)
        self.addLayout(layout)

        self.controls.group = group

    def setMode(self, mode):
        self.controls.group.setValue(mode)


class SymbolSelector(Card):
    changedSymbol = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QtWidgets.QLabel('Target:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        radio_nucleotide = QtWidgets.QRadioButton('Nucleotide')
        radio_protein = QtWidgets.QRadioButton('Protein')

        group = RadioButtonGroup()
        group.add(radio_nucleotide, Symbol.Nucleotide)
        group.add(radio_protein, Symbol.Protein)
        group.valueChanged.connect(self.changedSymbol)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(radio_nucleotide)
        layout.addWidget(radio_protein)
        layout.addStretch(1)
        self.addLayout(layout)

        self.controls.group = group

    def setSymbol(self, symbol):
        self.controls.group.setValue(symbol)


class ThresholdSelector(Card):
    changedSymbol = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QtWidgets.QLabel('Threshold:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        float_validator = QtGui.QDoubleValidator(self)
        locale = QtCore.QLocale.c()
        locale.setNumberOptions(QtCore.QLocale.RejectGroupSeparator)
        float_validator.setLocale(locale)
        float_validator.setDecimals(4)

        edit = GLineEdit('')
        edit.setValidator(float_validator)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(edit)
        layout.addStretch(1)
        self.addLayout(layout)

        self.controls.edit = edit


class LoggerCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = QtWidgets.QLabel('Progress Logs')
        title.setStyleSheet("""font-size: 16px;""")

        logger = TextEditLogger()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(16)
        layout.addWidget(title)
        layout.addWidget(logger)
        self.addLayout(layout)

        self.controls.logger = logger

    def setBusy(self, busy: bool):
        self.setEnabled(True)

    def append(self, text: str):
        self.controls.logger.append(text)

    def clear(self):
        self.controls.logger.clear()


class LengthDecontaminationView(TaskView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        self.cards = AttrDict()
        self.cards.title = TitleCard(self)
        self.cards.input = InputSelector(self)
        self.cards.mode = ModeSelector(self)
        self.cards.symbol = SymbolSelector(self)
        self.cards.threshold = ThresholdSelector(self)
        self.cards.logger = LoggerCard(self)

        layout = QtWidgets.QVBoxLayout()
        for card in self.cards:
            layout.addWidget(card)
        layout.addStretch(1)
        layout.setSpacing(6)
        layout.setContentsMargins(6, 6, 6, 6)
        self.setLayout(layout)

    def setObject(self, object):
        self.object = object
        self.binder.unbind_all()

        self.binder.bind(object.notification, self.showNotification)
        self.binder.bind(object.logLine, self.cards.logger.append)
        self.binder.bind(object.logClear, self.cards.logger.clear)

        self.binder.bind(object.properties.name, self.cards.title.setTitle)
        self.binder.bind(object.properties.busy, self.cards.title.setBusy)

        self.binder.bind(object.properties.editable, self.setEditable)

        self.binder.bind(self.cards.input.changedPath, object.properties.input)
        self.binder.bind(object.properties.input, self.cards.input.setPath)

        self.binder.bind(self.cards.mode.changedMode, object.properties.mode)
        self.binder.bind(object.properties.mode, self.cards.mode.setMode)

        self.binder.bind(self.cards.symbol.changedSymbol, object.properties.symbol)
        self.binder.bind(object.properties.symbol, self.cards.symbol.setSymbol)

        self.binder.bind(self.cards.threshold.controls.edit.textEditedSafe, object.properties.threshold, lambda x: float(x))
        self.binder.bind(object.properties.threshold, self.cards.threshold.controls.edit.setText, lambda x: f'{x:.4f}')


    def setEditable(self, editable: bool):
        for card in self.cards:
            card.setEnabled(editable)
        self.cards.title.setEnabled(True)
