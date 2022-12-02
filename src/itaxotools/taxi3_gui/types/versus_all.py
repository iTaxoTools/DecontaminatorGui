# -----------------------------------------------------------------------------
# Taxi3Gui - GUI for Taxi3
# Copyright (C) 2022  Patmanidis Stefanos
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
from typing import NamedTuple

from ._type import Type


class Entry(NamedTuple):
    label: str
    key: str
    default: int


class PropertyEnum(Enum):
    property_type = lambda: object

    def __init__(self, label, key, default):
        self.label = label
        self.key = key
        self.default = default
        self.type = object

    def __repr__(self):
        return f'<{self.__class__.__name__}.{self._name_}>'


class PairwiseScore(PropertyEnum):
    Match = Entry('Match', 'match_score', 1)
    Mismatch = Entry('Mismatch', 'mismatch_score', -1)
    InternalOpenGap = Entry('Open inner gap', 'internal_open_gap_score', -8)
    InternalExtendGap = Entry('Extend inner gap', 'internal_extend_gap_score', -1)
    EndOpenGap = Entry('Open outer gap', 'end_open_gap_score', -1)
    EndExtendGap = Entry('Extend outer gap', 'end_extend_gap_score', -1)


class DistanceMetric(PropertyEnum):
    property_type = lambda: bool
    Uncorrected = Entry('Uncorrected (p-distance)', 'p', True)
    UncorrectedWithGaps = Entry('Uncorrected with gaps', 'pg', True)
    JukesCantor = Entry('Jukes Cantor (jc)', 'jc', True)
    Kimura2Parameter = Entry('Kimura 2-Parameter (k2p)', 'k2p', True)
    NCD = Entry('Normalized Compression Distance (NCD)', 'ncd', False)
    BBC = Entry('Base-Base Correlation (BBC)', 'bbc', False)


class StatisticsGroup(PropertyEnum):
    property_type = lambda: bool
    All = Entry('For all sequences', 'for_all', True)
    Species = Entry('Per species', 'per_species', True)
    Genus = Entry('Per genus', 'per_genus', True)


class AlignmentMode(Enum):
    NoAlignment = ('No alignment', 'for already aligned sequences or alignment-free metrics')
    PairwiseAlignment = ('Pairwise Alignment', 'align each pair of sequences just before calculating distances')
    MSA = ('Multiple Sequence Alignment', 'uses MAFFT to align all sequences in advance')

    def __init__(self, label, description):
        self.label = label
        self.description = description
