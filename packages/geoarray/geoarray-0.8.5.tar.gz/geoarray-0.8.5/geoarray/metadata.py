# -*- coding: utf-8 -*-

import os
from pprint import pformat
from copy import deepcopy
from typing import Union  # noqa F401  # flake8 issue

from geopandas import GeoDataFrame, GeoSeries
import numpy as np
try:
    from osgeo import gdal
except ImportError:
    import gdal


autohandled_meta = [
    'bands',
    'byte_order',
    'coordinate_system_string',
    'data_type',
    'file_type',
    'header_offset',
    'interleave',
    'lines',
    'samples',
]


class GDAL_Metadata(object):
    def __init__(self, filePath='', nbands=1):
        # privates
        self._global_meta = dict()
        self._band_meta = dict()

        self.bands = nbands
        self.filePath = filePath
        self.fileFormat = ''

        if filePath:
            self.read_from_file(filePath)

    @classmethod
    def from_file(cls, filePath):
        return GDAL_Metadata(filePath=filePath)

    def to_DataFrame(self):
        df = GeoDataFrame(columns=range(self.bands))

        # add global meta
        for k, v in self.global_meta.items():
            df.loc[k] = GeoSeries(dict(zip(df.columns, [v] * len(df.columns))))

        # add band meta
        for k, v in self.band_meta.items():
            df.loc[k] = GeoSeries(dict(zip(df.columns, v)))

        return df

    @property
    def global_meta(self):
        return self._global_meta

    @global_meta.setter
    def global_meta(self, meta_dict):
        if not isinstance(meta_dict, dict):
            raise TypeError("Expected type 'dict', received '%s'." % type(meta_dict))

        self._global_meta = meta_dict  # TODO convert strings to useful types

    @property
    def band_meta(self):
        return self._band_meta

    @band_meta.setter
    def band_meta(self, meta_dict):
        if not isinstance(meta_dict, dict):
            raise TypeError("Expected type 'dict', received '%s'." % type(meta_dict))

        for k, v in meta_dict.items():
            if not isinstance(v, list):
                raise TypeError('The values of the given dictionary must be lists. Received %s for %s.' % (type(v), k))
            if len(v) != self.bands:
                raise ValueError("The length of the given lists must be equal to the number of bands. "
                                 "Received a list with %d items for '%s'." % (len(v), k))

        self._band_meta = meta_dict  # TODO convert strings to useful types

    @property
    def all_meta(self):
        all_meta = self.global_meta.copy()
        all_meta.update(self.band_meta)
        return all_meta

    @staticmethod
    def _convert_param_from_str(param_value):
        try:
            try:
                return int(param_value)  # NOTE: float('0.34') causes ValueError: invalid literal for int() with base 10
            except ValueError:
                return float(param_value)
        except ValueError:
            if param_value.startswith('{'):
                param_value = param_value.split('{')[1]
            if param_value.endswith('}'):
                param_value = param_value.split('}')[0]
            return param_value.strip()

    def _convert_param_to_ENVI_str(self, param_value):
        if isinstance(param_value, (int, np.integer)):
            return str(param_value)

        elif isinstance(param_value, (float, np.floating)):
            return '%f' % param_value

        elif isinstance(param_value, list):
            return '{ ' + ',\n'.join([self._convert_param_to_ENVI_str(i) for i in param_value]) + ' }'

        else:
            return str(param_value)

    def read_from_file(self, filePath):
        assert ' ' not in filePath, "The given path contains whitespaces. This is not supported by GDAL."

        if not os.path.exists(filePath):
            raise FileNotFoundError(filePath)

        ds = gdal.Open(filePath)

        try:
            if not ds:
                raise Exception('Error reading file:  ' + gdal.GetLastErrorMsg())

            self.bands = ds.RasterCount
            self.fileFormat = ds.GetDriver().GetDescription()

            ###############
            # ENVI format #
            ###############

            if self.fileFormat == 'ENVI':
                metadict = ds.GetMetadata('ENVI')

                for k, v in metadict.items():

                    if k not in autohandled_meta:

                        if len(v.split(',')) == self.bands:
                            # band meta parameter
                            item_list = [
                                item_str.split('{')[1].strip() if item_str.strip().startswith('{') else
                                item_str.split('}')[0].strip() if item_str.strip().endswith('}') else
                                item_str.strip() for item_str in v.split(',')]

                            self.band_meta[k] = [self._convert_param_from_str(item_str) for item_str in item_list]

                        else:
                            # global meta parameter
                            self.global_meta[k] = self._convert_param_from_str(v)

            #####################
            # remaining formats #
            #####################

            else:
                # read global domain metadata
                self.global_meta = ds.GetMetadata()

                # read band domain metadata
                for b in range(self.bands):
                    band = ds.GetRasterBand(b + 1)
                    # meta_gs = GeoSeries(band.GetMetadata())
                    bandmeta_dict = band.GetMetadata()

                    for k, v in bandmeta_dict.items():
                        if k not in self.band_meta:
                            self.band_meta[k] = []

                        self.band_meta[k].append(self._convert_param_from_str(v))

                    # # fill metadata
                    # self.df[b] = meta_gs
                    del band

        finally:
            del ds

        return self.all_meta

    def __repr__(self):
        return 'Metadata: \n\n' + pformat(self.all_meta)

    def to_ENVI_metadict(self):
        return dict(zip(self.all_meta.keys(),
                        [self._convert_param_to_ENVI_str(i) for i in self.all_meta.values()]))

    def get_subset(self, bands2extract=None, keys2extract=None):
        # type: (Union[slice, list, np.ndarray], Union[str, list]) -> 'GDAL_Metadata'
        meta_sub = deepcopy(self)

        # subset bands
        if bands2extract is not None:
            if isinstance(bands2extract, list):
                bands2extract = np.array(bands2extract)
            elif isinstance(bands2extract, (np.ndarray, slice)):
                pass  # all fine
            else:
                raise TypeError(bands2extract)

            meta_sub.band_meta = self.band_meta.copy()

            for k, v in meta_sub.band_meta.items():
                meta_sub.band_meta[k] = list(np.array(v)[bands2extract])

            meta_sub.bands = len(list(range(*bands2extract.indices(bands2extract.stop)))) \
                if isinstance(bands2extract, slice) else bands2extract.size

        # subset metadata keys
        if keys2extract:
            keys2extract = [keys2extract] if isinstance(keys2extract, str) else keys2extract

            # global_meta = meta_sub.global_meta.copy()
            for k in meta_sub.global_meta.copy().keys():
                if k not in keys2extract:
                    del meta_sub.global_meta[k]

            for k in meta_sub.band_meta.copy().keys():
                if k not in keys2extract:
                    del meta_sub.band_meta[k]

            if not meta_sub.all_meta:
                raise ValueError(keys2extract, 'The given metadata keys do not exist.')

        return meta_sub

    def __getitem__(self, given):
        if isinstance(given, int):
            return self.get_subset(bands2extract=slice(given, given + 1))
        elif isinstance(given, slice):
            return self.get_subset(bands2extract=given)
        elif isinstance(given, str):
            return self.get_subset(keys2extract=given)
        elif isinstance(given, list):
            if isinstance(given[0], str):
                return self.get_subset(keys2extract=given)
            elif isinstance(given[0], int):
                return self.get_subset(bands2extract=given)
            else:
                raise TypeError(given, 'Given list must contain string or integer items.')
        elif isinstance(given, np.ndarray):
            if given.ndim != 1:
                raise TypeError(given, 'Given numpy array must be one-dimensional.')
            return self.get_subset(bands2extract=given)
        else:
            raise TypeError(given)
