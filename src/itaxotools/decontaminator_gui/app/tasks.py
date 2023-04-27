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

from ..model.common import TaskModel
from ..view.common import TaskView

from ..model.decontamination import DecontaminationModel
from ..view.decontamination import DecontaminationView

from ..model.branch_decontamination import BranchDecontaminationModel
from ..view.branch_decontamination import BranchDecontaminationView

from ..model.length_decontamination import LengthDecontaminationModel
from ..view.length_decontamination import LengthDecontaminationView

from ..model.scafospy import ScafospyModel
from ..view.scafospy import ScafospyView

from ..model.gene_subset_selector import GeneSubsetSelectorModel
from ..view.gene_subset_selector import GeneSubsetSelectorView

from ..model.remove_rename import RemoveRenameModel
from ..view.remove_rename import RemoveRenameView

class Task(NamedTuple):
    title: str
    description: str
    model: TaskModel
    view: TaskView


tasks = [
    Task('Decontamination', 'Delete sequences from .ali files', DecontaminationModel, DecontaminationView),
    Task('Remove-Rename', 'Delete/rename sequences', RemoveRenameModel, RemoveRenameView),
    Task('Branch Decontamination', 'Delete sequences based on tree branch length', BranchDecontaminationModel, BranchDecontaminationView),
    Task('Length Decontamination', 'Delete sequences with too much noninformation data', LengthDecontaminationModel, LengthDecontaminationView),
    Task('Gene Subset Selector', 'Selecting subset(s) of genes through different methods', GeneSubsetSelectorModel, GeneSubsetSelectorView),
    Task('SCaFoSpy', 'Fuses multiple sequences from same sample', ScafospyModel, ScafospyView),
]
