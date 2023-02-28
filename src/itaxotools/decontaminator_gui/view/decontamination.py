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
from .common import (
    Card, ComparisonModeSelector, GLineEdit, GSpinBox, ObjectView)


class ItemProxyModel(QtCore.QAbstractProxyModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = None
        self.unselected = '---'

    def sourceDataChanged(self, topLeft, bottomRight):
        self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(bottomRight))

    @override
    def setSourceModel(self, model, root):
        super().setSourceModel(model)
        self.root = root
        model.dataChanged.connect(self.sourceDataChanged)

    @override
    def mapFromSource(self, sourceIndex):
        item = sourceIndex.internalPointer()
        if not item or item.parent != self.root:
            return QtCore.QModelIndex()
        return self.createIndex(item.row + 1, 0, item)

    @override
    def mapToSource(self, proxyIndex):
        if not proxyIndex.isValid():
            return QtCore.QModelIndex()
        if proxyIndex.row() == 0:
            return QtCore.QModelIndex()
        item = proxyIndex.internalPointer()
        source = self.sourceModel()
        return source.createIndex(item.row, 0, item)

    @override
    def index(self, row: int, column: int, parent=QtCore.QModelIndex()) -> QtCore.QModelIndex:
        if parent.isValid() or column != 0:
            return QtCore.QModelIndex()
        if row < 0 or row > len(self.root.children):
            return QtCore.QModelIndex()
        if row == 0:
            return self.createIndex(0, 0)
        return self.createIndex(row, 0, self.root.children[row - 1])

    @override
    def parent(self, index=QtCore.QModelIndex()) -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    @override
    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self.root.children) + 1

    @override
    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        return 1

    @override
    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt.ItemDataRole):
        if not index.isValid():
            return None
        if index.row() == 0:
            if role == QtCore.Qt.DisplayRole:
                return self.unselected
            return None
        return super().data(index, role)

    @override
    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        if index.row() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return super().flags(index)


class TitleCard(Card):
    run = QtCore.Signal()
    cancel = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        title = QtWidgets.QLabel('Decontamination')
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
    itemChanged = QtCore.Signal(Item)
    addInputFile = QtCore.Signal(Path)

    def __init__(self, text, parent=None, model=app.model.items):
        super().__init__(parent)
        self.binder = Binder()
        self._guard = Guard()
        self.draw(model)

    def draw(self, model):
        label = QtWidgets.QLabel('Input directory:')
        label.setStyleSheet("""font-size: 16px;""")
        label.setMinimumWidth(120)

        combo = NoWheelComboBox()
        combo.currentIndexChanged.connect(self.handleItemChanged)
        self.set_model(combo, model)

        wait = NoWheelComboBox()
        wait.addItem('Scanning file, please wait...')
        wait.setEnabled(False)
        wait.setVisible(False)

        browse = QtWidgets.QPushButton('Import')
        browse.clicked.connect(self.handleBrowse)

        loading = QtWidgets.QPushButton('Loading')
        loading.setEnabled(False)
        loading.setVisible(False)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(combo, 1)
        layout.addWidget(wait, 1)
        layout.addWidget(browse)
        layout.addWidget(loading)
        layout.setSpacing(16)
        self.addLayout(layout)

        self.controls.label = label
        self.controls.combo = combo
        self.controls.wait = wait
        self.controls.browse = browse
        self.controls.loading = loading

    def set_model(self, combo, model):
        proxy_model = ItemProxyModel()
        proxy_model.setSourceModel(model, model.files)
        combo.setModel(proxy_model)

    def handleItemChanged(self, row):
        if self._guard:
            return
        if row > 0:
            item = self.controls.combo.itemData(row, ItemModel.ItemRole)
        else:
            item = None
        self.itemChanged.emit(item)

    def handleBrowse(self, *args):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window(), f'{app.title} - Import Sequence File')
        if not filename:
            return
        self.addInputFile.emit(Path(filename))

    def setObject(self, object):
        # Workaround to repaint bugged card line
        QtCore.QTimer.singleShot(10, self.update)

        if object is None:
            row = 0
        else:
            file_item = object.file_item
            row = file_item.row + 1 if file_item else 0
        with self._guard:
            self.controls.combo.setCurrentIndex(row)

        self.binder.unbind_all()

    def setBusy(self, busy: bool):
        self.setEnabled(True)
        self.controls.combo.setVisible(not busy)
        self.controls.wait.setVisible(busy)
        self.controls.browse.setVisible(not busy)
        self.controls.loading.setVisible(busy)
        self.controls.label.setEnabled(not busy)
        self.controls.config.setEnabled(not busy)


class DecontaminationView(TaskView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw()

    def draw(self):
        self.cards = AttrDict()
        self.cards.title = TitleCard(self)
        self.cards.input = InputSelector(self)

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

        self.binder.bind(object.properties.name, self.cards.title.setTitle)
        self.binder.bind(object.properties.busy, self.cards.title.setBusy)

        self.binder.bind(object.properties.editable, self.setEditable)

    def setEditable(self, editable: bool):
        for card in self.cards:
            card.setEnabled(editable)
        self.cards.title.setEnabled(True)
