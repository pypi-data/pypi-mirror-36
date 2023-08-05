# =============================================================================================
# Copyright 2017 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================================

import os
from rasterio import open as rasopen

from met.thredds import TopoWX, GridMet
from dem import AwsDem
from sat_image.fmask import Fmask
from sat_image import warped_vrt
from bounds import RasterBounds


class SSEBopData:
    def __init__(self, image_id, image_dir, transform,
            profile, clip_geo, date):

        self.image_id = image_id
        self.image_dir = image_dir
        self.transform = transform
        self.profile = profile
        self.clip_geo = clip_geo
        self.date = date
        self.bounds = RasterBounds(affine_transform=self.transform,
                                   profile=self.profile, latlon=True)

        self.variable = None
        self.file_path = None
        self.shape = (1, profile['height'], profile['width'])

    def data_check(self, variable, sat_image=None, temp_units='C'):

        self.variable = variable
        valid_vars = ['tmax', 'tmin', 'dem', 'fmask', 'pet']

        if self.variable not in valid_vars:
            raise KeyError('Variable {} is invalid, choose from {}'.format(self.variable,
                                                                           valid_vars))

        if self.variable == 'dem':
            self.file_name = '{}.tif'.format(self.variable)
            self.file_path = os.path.join(os.path.dirname(self.image_dir), self.file_name)
        else:
            self.file_name = '{}_{}.tif'.format(self.image_id, variable)
            self.file_path = os.path.join(self.image_dir, self.file_name)

        if self.file_name not in os.listdir(self.image_dir):
            if variable == 'tmax':
                var = self.fetch_temp('tmax', temp_units)
            if variable == 'tmin':
                var = self.fetch_temp('tmin', temp_units)
            if variable == 'dem':
                var = self.fetch_dem()
            if variable == 'fmask':
                var = self.fetch_fmask(sat_image)
            if variable == 'pet':
                var = self.fetch_gridmet('pet')

        else:

            with rasopen(self.file_path, 'r') as src:
                var = src.read()

        var = self.check_shape(var, self.file_path)
        return var

    def check_shape(self, var, path):
        if not var.shape == self.shape:
            new = warped_vrt.warp_single_image(image_path=path, profile=self.profile)
            return new
        else:
            return var

    def fetch_gridmet(self, variable='pet'):
        gridmet = GridMet(variable, date=self.date,
                          bbox=self.bounds,
                          target_profile=self.profile,
                          clip_feature=self.clip_geo)

        var = gridmet.get_data_subset(out_filename=self.file_path)
        return var

    def fetch_temp(self, variable='tmax', temp_units='C'):
        print('Downloading new {}.....'.format(variable))
        topowx = TopoWX(date=self.date, bbox=self.bounds,
                        target_profile=self.profile,
                        clip_feature=self.clip_geo, out_file=self.file_path)

        var = topowx.get_data_subset(grid_conform=True, var=variable,
                                     out_file=self.file_path,
                                     temp_units_out=temp_units)
        return var

    def fetch_dem(self):
        dem = AwsDem(bounds=self.bounds, clip_object=self.clip_geo,
                     target_profile=self.profile, zoom=8)
        var = dem.terrain(attribute='elevation', out_file=self.file_path,
                          save_and_return=True)
        return var

    def fetch_fmask(self, sat_image):
        f = Fmask(sat_image)
        combo = f.cloud_mask(min_filter=(3, 3), max_filter=(40, 40), combined=True)
        f.save_array(combo, self.file_path)
        return combo


if __name__ == '__main__':
    home = os.path.expanduser('~')

# ========================= EOF ====================================================================
