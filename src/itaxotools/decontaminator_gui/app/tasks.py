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

from typing import NamedTuple

from ..model import (
    BulkSequencesModel, DecontaminateModel, DereplicateModel, Item,
    SequenceModel, TaskModel, VersusAllModel, VersusReferenceModel)
from ..view import (
    BulkSequencesView, DecontaminateView, DereplicateView, SequenceView,
    TaskView, VersusAllView, VersusReferenceView)


class Task(NamedTuple):
    title: str
    description: str
    model: TaskModel
    view: TaskView


tasks = [
    Task('Versus All', 'Analyze distances within a dataset', VersusAllModel, VersusAllView),
    Task('Versus Reference', 'Compare distances to another dataset', VersusReferenceModel, VersusReferenceView),
    Task('Dereplicate', 'Detect similar sequences within a dataset', DereplicateModel, DereplicateView),
    Task('Decontaminate', 'Detect sequences close to another dataset', DecontaminateModel, DecontaminateView),
]
