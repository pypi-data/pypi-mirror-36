# -*- coding: utf-8 -*-
#
#  Copyright 2015-2018 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of CIMtools.
#
#  CIMtools is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from CGRtools.containers import MoleculeContainer
from CGRtools.core import CGRcore
from io import TextIOWrapper
from operator import itemgetter
from pkg_resources import resource_stream
from .chemaxon import StandardizeChemAxon
from ..common import iter2array


class StandardizeHorvat(StandardizeChemAxon):
    def __init__(self, rules=None, unwanted=None, min_ratio=2, max_ion_size=5, min_main_size=6, max_main_size=101,
                 workpath='.'):
        self.unwanted = set(unwanted) if unwanted is not None else self.__load_unwanted()
        if rules is None:
            rules = self.__load_rules()
        self.min_ratio = min_ratio
        self.max_ion_size = max_ion_size
        self.min_main_size = min_main_size
        self.max_main_size = max_main_size
        super().__init__(rules, workpath=workpath)

    def set_params(self, **params):
        if params:
            if 'rules' in params and params['rules'] is None:
                params['rules'] = self.__load_rules()
            if 'unwanted' in params:
                params['unwanted'] = self.__load_unwanted() if params['unwanted'] is None else set(params['unwanted'])

            super().set_params(**params)
        return self

    def transform(self, x):
        """
        Standardize Molecules by Dragos Horvat workflow

        step 1 (by default): dearomatize & dealkalinize, neutralize all species,
        except for FOUR-LEGGED NITROGEN, which has to be positive for else chemically incorrect
        Automatically represent N-oxides, incl. nitros, as N+-O-.
        generate major tautomer & aromatize.

        step 2: check for bizzare salts or mixtures. strip mixtures

        :param x: {array-like}, shape [n_samples] of MoleculeContainers
        :return: array of MoleculeContainers
        """

        res = []
        for s in super().transform(x):
            if s is None:
                res.append(None)
            else:
                species = sorted(((len([None for _, e in x.nodes(data='element') if e != 'H']), x)
                                  for x in CGRcore.split(s)), key=itemgetter(0))
                if species[-1][0] <= self.max_main_size and \
                        (len(species) == 1 or (species[-1][0] / species[-2][0] >= self.min_ratio and
                                               species[-2][0] <= self.max_ion_size and
                                               species[-1][0] >= self.min_main_size)) \
                        and not self.unwanted.intersection(species[-1][1]):
                    res.append(species[-1][1])
                else:
                    res.append(None)
        return iter2array(res, allow_none=True)

    @staticmethod
    def __load_rules():
        with resource_stream(__package__, 'horvat.xml') as f, TextIOWrapper(f) as s:
            out = s.read().strip()
        return out

    @staticmethod
    def __load_unwanted():
        with resource_stream(__package__, 'horvat.unwanted') as f, TextIOWrapper(f) as s:
            out = set(s.read().split())
        return out

    _dtype = MoleculeContainer
