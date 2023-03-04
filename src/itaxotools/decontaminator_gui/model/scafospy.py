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

from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copytree
from enum import Enum, auto

from ..tasks import scafospy
from ..types import Notification
from ..types.scafospy import Mode, Symbol
from ..utility import Property
from .common import TaskModel
from .input_file import InputFileModel


class Subtask(Enum):
    Initialize = auto()
    Main = auto()


class ScafospyModel(TaskModel):
    task_name = 'Scafospy'

    input = Property(Path, None)
    output = Property(Path, None)

    mode = Property(Mode, Mode.Ambiguity)
    symbol = Property(Symbol, Symbol.Nucleotide)

    def __init__(self, name=None):
        super().__init__(name)
        self.exec(Subtask.Initialize, scafospy.initialize)

    def readyTriggers(self):
        return [
            self.properties.input,
            self.properties.output,
        ]

    def isReady(self):
        if self.input is None:
            return False
        if self.output is None:
            return False
        return True

    def start(self):
        super().start()
        self.exec(
            Subtask.Main,
            scafospy.execute,
            dir=str(self.input),
            out=str(self.output),
            mode=str(self.mode),
            type=str(self.symbol),
        )

    def onDone(self, report):
        if report.id == Subtask.Initialize:
            return
        if report.id == Subtask.Main:
            self.notification.emit(Notification.Info(f'{self.name} completed successfully!'))
            self.busy = False
            # self.done = True
