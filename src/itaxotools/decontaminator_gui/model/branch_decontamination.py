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

from ..tasks import branch_decontamination
from ..types import Notification
from ..types.branch_decontamination import Mode, Target
from ..utility import Property
from .common import TaskModel
from .input_file import InputFileModel


class Subtask(Enum):
    Initialize = auto()
    Main = auto()


class BranchDecontaminationModel(TaskModel):
    task_name = 'Branch Decontamination'

    input = Property(Path, None)

    mode = Property(Mode, Mode.Terminal)
    target = Property(Target, Target.Alignment)

    absolute = Property(int, 0)
    percentile = Property(float, 0.0)
    quantile = Property(float, 0.0)
    factor = Property(float, 0.0)
    tree = Property(Path, None)

    def __init__(self, name=None):
        super().__init__(name)
        self.exec(Subtask.Initialize, branch_decontamination.initialize)

    def readyTriggers(self):
        return [
            self.properties.input,
        ]

    def isReady(self):
        if self.input is None:
            return False
        return True

    def start(self):
        super().start()
        self.exec(
            Subtask.Main,
            branch_decontamination.execute,
            dir=str(self.input),
            mode=str(self.mode),
            target=str(self.target),
            perc=str(self.percentile),
            absolute=str(self.absolute),
            quantile=str(self.quantile),
            factor=str(self.factor),
            referencetree=str(self.tree) if self.tree else '',
        )

    def onDone(self, report):
        if report.id == Subtask.Initialize:
            return
        if report.id == Subtask.Main:
            self.notification.emit(Notification.Info(f'{self.name} completed successfully!'))
            self.busy = False
            # self.done = True
