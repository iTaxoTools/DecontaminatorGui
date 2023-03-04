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

from enum import Enum


class Mode(Enum):
    Ambiguity = 'ambiguity'
    LongestSequence = 'longest_sequence'
    LowestDiversion = 'lowest_diversion'

    def __str__(self):
        return self.value


class Symbol(Enum):
    Nucleotide = 'nucleotide'
    Protein = 'protein'

    def __str__(self):
        return self.value
