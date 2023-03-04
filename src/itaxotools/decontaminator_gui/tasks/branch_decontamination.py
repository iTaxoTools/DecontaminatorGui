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


def initialize():
    from itaxotools.decontaminator.decontamination import __Main__


def execute(**kwargs):
    from itaxotools.decontaminator.decontamination import __Main__
    print(' Arguments '.center(60, '-'))
    print()

    argv = ['decontamination']
    for k, v in kwargs.items():
        print(f'--{k} {v}')
        argv.append('--' + k)
        argv.append(v)
    print()

    print(' Decontamination '.center(60, '-'))
    print()

    __Main__(argv)

    print()
    print(' End '.center(60, '-'))
    return 42
