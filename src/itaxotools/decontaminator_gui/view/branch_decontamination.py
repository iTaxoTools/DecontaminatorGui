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
from ..types.branch_decontamination import Mode, Target
from .common import (
    Card, ComparisonModeSelector, GLineEdit, GSpinBox, ObjectView, TextEditLogger, Resizer)


class TitleCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = QtWidgets.QLabel()
        title.setStyleSheet("""font-size: 18px; font-weight: bold; """)

        description = QtWidgets.QLabel(
            'Deleting sequences from .ali files.')
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

        radio_terminal = QtWidgets.QRadioButton('Terminal')
        radio_internal = QtWidgets.QRadioButton('Internal')

        group = RadioButtonGroup()
        group.add(radio_terminal, Mode.Terminal)
        group.add(radio_internal, Mode.Internal)
        group.valueChanged.connect(self.changedMode)

        head = QtWidgets.QHBoxLayout()
        head.addWidget(label)
        head.addWidget(radio_terminal)
        head.addWidget(radio_internal)
        head.addStretch(1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(head)
        layout.addWidget(description)
        layout.setSpacing(16)
        self.addLayout(layout)

        self.controls.group = group

    def setMode(self, mode):
        self.controls.group.setValue(mode)


class TargetSelector(Card):
    changedTarget = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QtWidgets.QLabel('Target:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        description = QtWidgets.QLabel(
            'Defines what type of file should be decontaminated.')
        description.setWordWrap(True)

        radio_alignment = QtWidgets.QRadioButton('Alignment')
        radio_tree = QtWidgets.QRadioButton('Tree')
        radio_both = QtWidgets.QRadioButton('Both')

        group = RadioButtonGroup()
        group.add(radio_alignment, Target.Alignment)
        group.add(radio_tree, Target.Tree)
        group.add(radio_both, Target.Both)
        group.valueChanged.connect(self.changedTarget)

        head = QtWidgets.QHBoxLayout()
        head.addWidget(label)
        head.addWidget(radio_alignment)
        head.addWidget(radio_tree)
        head.addWidget(radio_both)
        head.addStretch(1)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(head)
        layout.addWidget(description)
        layout.setSpacing(16)
        self.addLayout(layout)

        self.controls.group = group

    def setTarget(self, target):
        self.controls.group.setValue(target)


class ArgumentSelector(Card):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        title = QtWidgets.QLabel('Additional arguments:')
        title.setStyleSheet("""font-size: 16px;""")
        title.setMinimumWidth(120)

        notice = QtWidgets.QLabel(
            'At least one of these must be defined for the program to work.')
        notice.setWordWrap(True)

        options = QtWidgets.QGridLayout()
        options.setContentsMargins(0, 0, 0, 0)
        options.setColumnStretch(2, 1)
        options.setColumnMinimumWidth(1, 80)
        row = 0

        int_validator = QtGui.QIntValidator(self)
        float_validator = QtGui.QDoubleValidator(self)
        locale = QtCore.QLocale.c()
        locale.setNumberOptions(QtCore.QLocale.RejectGroupSeparator)
        float_validator.setLocale(locale)
        float_validator.setBottom(0)
        float_validator.setTop(1)
        float_validator.setDecimals(4)

        label = QtWidgets.QLabel('Absolute:')
        description = QtWidgets.QLabel('Outputs a defined number of longest branches and deletes them from target.')
        description.setWordWrap(True)
        widget = GLineEdit('')
        widget.setValidator(int_validator)

        options.addWidget(label, row, 0)
        options.addWidget(widget, row, 1)
        options.addWidget(description, row, 2)
        self.controls.absolute = widget
        row += 1

        label = QtWidgets.QLabel('Percentile:')
        description = QtWidgets.QLabel('Outputs a defined percentage (between 0.0 and 1.0) of longest branches and deletes them from target.')
        description.setWordWrap(True)
        widget = GLineEdit('')
        widget.setValidator(float_validator)

        options.addWidget(label, row, 0)
        options.addWidget(widget, row, 1)
        options.addWidget(description, row, 2)
        self.controls.percentile = widget
        row += 1

        label = QtWidgets.QLabel('Quantile:')
        description = QtWidgets.QLabel('Outputs a number of branches that are longer than the critical value of the defined quantile (between 0.0 and 1.0) and deletes them from target.')
        description.setWordWrap(True)
        widget = GLineEdit('')
        widget.setValidator(float_validator)

        options.addWidget(label, row, 0)
        options.addWidget(widget, row, 1)
        options.addWidget(description, row, 2)
        self.controls.quantile = widget
        row += 1

        label = QtWidgets.QLabel('Factor:')
        description = QtWidgets.QLabel('Outputs a number of branches that are longer by a given factor than the mean length of their sister species and deletes them from target.')
        description.setWordWrap(True)
        widget = GLineEdit('')
        widget.setValidator(float_validator)

        options.addWidget(label, row, 0)
        options.addWidget(widget, row, 1)
        options.addWidget(description, row, 2)
        self.controls.factor = widget
        row += 1

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(notice)
        layout.addLayout(options)
        layout.setSpacing(16)
        self.addLayout(layout)


class TreeSelector(Card):
    changedPath = QtCore.Signal(Path)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        label = QtWidgets.QLabel('Tree file:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        description = QtWidgets.QLabel(
            'Outputs a number of branches that are longer by a factor than their counter part in the reference tree and deletes them from target.')
        description.setWordWrap(True)

        edit = QtWidgets.QLineEdit('---')
        edit.setReadOnly(True)

        browse = QtWidgets.QPushButton('Browse')
        browse.clicked.connect(self.handleBrowse)

        head = QtWidgets.QHBoxLayout()
        head.addWidget(label)
        head.addWidget(edit, 1)
        head.addWidget(browse)
        head.setSpacing(16)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(8)
        layout.addLayout(head)
        layout.addWidget(description)
        self.addLayout(layout)

        self.controls.edit = edit

    def setPath(self, path):
        if path is None:
            path = '---'
        self.controls.edit.setText(str(path))

    def handleBrowse(self, *args):
        file = self.parent().getOpenPath('Tree file')
        if not file:
            return
        self.changedPath.emit(file)


class LoggerCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent)

        title = QtWidgets.QLabel('Progress Logs')
        title.setStyleSheet("""font-size: 16px;""")

        logger = TextEditLogger()
        resizer = Resizer(logger)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(16)
        layout.addWidget(title)
        layout.addWidget(resizer)
        self.addLayout(layout)

        self.controls.logger = logger

    def setBusy(self, busy: bool):
        self.setEnabled(True)

    def append(self, text: str):
        self.controls.logger.append(text)

    def clear(self):
        self.controls.logger.clear()


class BranchDecontaminationView(TaskView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        self.cards = AttrDict()
        self.cards.title = TitleCard(self)
        self.cards.input = InputSelector(self)
        self.cards.mode = ModeSelector(self)
        self.cards.target = TargetSelector(self)
        self.cards.args = ArgumentSelector(self)
        self.cards.tree = TreeSelector(self)
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

        self.binder.bind(self.cards.target.changedTarget, object.properties.target)
        self.binder.bind(object.properties.target, self.cards.target.setTarget)

        self.binder.bind(self.cards.args.controls.absolute.textEditedSafe, object.properties.absolute, lambda x: int(x))
        self.binder.bind(object.properties.absolute, self.cards.args.controls.absolute.setText, lambda x: str(x))

        self.binder.bind(self.cards.args.controls.percentile.textEditedSafe, object.properties.percentile, lambda x: float(x))
        self.binder.bind(object.properties.percentile, self.cards.args.controls.percentile.setText, lambda x: f'{x:.4f}')

        self.binder.bind(self.cards.args.controls.quantile.textEditedSafe, object.properties.quantile, lambda x: float(x))
        self.binder.bind(object.properties.quantile, self.cards.args.controls.quantile.setText, lambda x: f'{x:.4f}')

        self.binder.bind(self.cards.args.controls.factor.textEditedSafe, object.properties.factor, lambda x: float(x))
        self.binder.bind(object.properties.factor, self.cards.args.controls.factor.setText, lambda x: f'{x:.4f}')

        self.binder.bind(self.cards.tree.changedPath, object.properties.tree)
        self.binder.bind(object.properties.tree, self.cards.tree.setPath)

    def setEditable(self, editable: bool):
        for card in self.cards:
            card.setEnabled(editable)
        self.cards.title.setEnabled(True)
