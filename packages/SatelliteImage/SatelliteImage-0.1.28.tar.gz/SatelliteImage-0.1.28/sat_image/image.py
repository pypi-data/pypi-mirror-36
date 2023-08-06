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
import shutil
from rasterio import open as rasopen
from numpy import where, pi, cos, nan, inf, true_divide, errstate, log
from numpy import float32, sin, deg2rad, array, isnan
from shapely.geometry import Polygon, mapping
from fiona import open as fiopen
from fiona.crs import from_epsg
from tempfile import mkdtemp
from datetime import datetime

from bounds import RasterBounds
from sat_image import mtl


class UnmatchedStackGeoError(ValueError):
    pass


class InvalidObjectError(TypeError):
    pass


class LandsatImage(object):
    '''
    Object to process landsat images. The parent class: LandsatImage takes a directory 
    containing untarred files, for now this ingests images that have been downloaded
    from USGS earth explorer, using our Landsat578 package.
    
    '''

    def __init__(self, obj):
        ''' 
        :param obj: Directory containing an unzipped Landsat 5, 7, or 8 image.  This should include at least
        a tif for each band, and a .mtl file.
        '''
        self.obj = obj
        if os.path.isdir(obj):
            self.isdir = True

        self.date_acquired = None

        self.file_list = os.listdir(obj)
        self.tif_list = [x for x in os.listdir(obj) if x.endswith('.TIF')]
        self.tif_list.sort()

        # parse metadata file into attributes
        # structure: {HEADER: {SUBHEADER: {key(attribute), val(attribute value)}}}
        self.mtl = mtl.parsemeta(obj)
        self.meta_header = list(self.mtl)[0]
        self.super_dict = self.mtl[self.meta_header]
        for key, val in self.super_dict.items():
            for sub_key, sub_val in val.items():
                # print(sub_key.lower(), sub_val)
                setattr(self, sub_key.lower(), sub_val)
        self.satellite = self.landsat_scene_id[:3]

        # create numpy nd_array objects for each band
        self.band_list = []
        self.tif_dict = {}
        for i, tif in enumerate(self.tif_list):
            raster = os.path.join(self.obj, tif)

            # set all lower case attributes
            tif = tif.lower()
            front_ind = tif.index('b')
            end_ind = tif.index('.tif')
            att_string = tif[front_ind: end_ind]

            self.band_list.append(att_string)
            self.tif_dict[att_string] = raster
            self.band_count = i + 1

            if i == 0:
                with rasopen(raster) as src:
                    transform = src.transform
                    profile = src.profile
                meta = src.meta.copy()
                self.rasterio_geometry = meta
                self.profile = profile
                self.transform = transform
                self.shape = (1, profile['height'], profile['width'])

                bounds = RasterBounds(affine_transform=transform,
                                      profile=profile,
                                      latlon=False)
                self.bounds = bounds
                self.north, self.west, self.south, self.east = bounds.get_nwse_tuple()
                self.coords = bounds.as_tuple('nsew')

        self.solar_zenith = 90. - self.sun_elevation
        self.solar_zenith_rad = self.solar_zenith * pi / 180
        self.sun_elevation_rad = self.sun_elevation * pi / 180
        self.earth_sun_dist = self.earth_sun_d(self.date_acquired)

        dtime = datetime.strptime(str(self.date_acquired), '%Y-%m-%d')
        julian_day = dtime.strftime('%j')
        self.doy = int(julian_day)
        self.scene_coords_deg = self._scene_centroid()
        self.scene_coords_rad = deg2rad(self.scene_coords_deg[0]), deg2rad(self.scene_coords_deg[1])

    def _get_band(self, band_str):
        path = self.tif_dict[band_str]
        with rasopen(path) as src:
            arr = src.read(1)
        arr = array(arr, dtype=float32)
        arr[arr < 1.] = nan
        return arr

    def _scene_centroid(self):
        """ Compute image center coordinates
        :return: Tuple of image center in lat, lon
        """
        ul_lat = self.corner_ul_lat_product
        ll_lat = self.corner_ll_lat_product
        ul_lon = self.corner_ul_lon_product
        ur_lon = self.corner_ur_lon_product
        lat = (ul_lat + ll_lat) / 2.
        lon = (ul_lon + ur_lon) / 2.

        return lat, lon

    @staticmethod
    def earth_sun_d(dtime):
        """ Earth-sun distance in AU
        
        :param dtime time, e.g. datetime.datetime(2007, 5, 1)
        :type datetime object
        :return float(distance from sun to earth in astronomical units)
        """
        doy = int(dtime.strftime('%j'))
        rad_term = 0.9856 * (doy - 4) * pi / 180
        distance_au = 1 - 0.01672 * cos(rad_term)
        return distance_au

    @staticmethod
    def _divide_zero(a, b, replace=0):
        with errstate(divide='ignore', invalid='ignore'):
            c = true_divide(a, b)
            c[c == inf] = replace
            return c

    def get_tile_geometry(self, output_filename=None, geographic_coords=False):

        if not output_filename:
            temp_dir = mkdtemp()
            temp = os.path.join(temp_dir, 'shape.shp')
        else:
            temp = output_filename

        # corners = {'ul': (self.corner_ul_projection_x_product,
        #                   self.corner_ul_projection_y_product),
        #            'll': (self.corner_ll_projection_x_product,
        #                   self.corner_ll_projection_y_product),
        #            'lr': (self.corner_lr_projection_x_product,
        #                   self.corner_lr_projection_y_product),
        #            'ur': (self.corner_ur_projection_x_product,
        #                   self.corner_ur_projection_y_product)}
        if geographic_coords:
            points = [(self.north, self.west), (self.south, self.west),
                      (self.south, self.east), (self.north, self.east),
                      (self.north, self.west)]
        else:
            points = [(self.west, self.north), (self.west, self.south),
                      (self.east, self.south), (self.east, self.north),
                      (self.west, self.north)]

        polygon = Polygon(points)

        schema = {'geometry': 'Polygon',
                  'properties': {'id': 'int'}}

        crs = from_epsg(int(self.rasterio_geometry['crs']['init'].split(':')[1]))

        with fiopen(temp, 'w', 'ESRI Shapefile', schema=schema, crs=crs) as shp:
            shp.write({
                'geometry': mapping(polygon),
                'properties': {'id': 1}})

        if output_filename:
            return None

        with fiopen(temp, 'r') as src:
            features = [f['geometry'] for f in src]
            if not output_filename:

                try:
                    shutil.rmtree(temp_dir)
                except UnboundLocalError:
                    pass

                return features

    def save_array(self, arr, output_filename):
        geometry = self.rasterio_geometry
        arr = arr.reshape(1, arr.shape[0], arr.shape[1])
        geometry['dtype'] = arr.dtype
        with rasopen(output_filename, 'w', **geometry) as dst:
            dst.write(arr)
        return None

    def mask_by_image(self, arr):
        image = self._get_band('b1')
        image = array(image, dtype=float32)
        image[image < 1.] = nan
        arr = where(isnan(image), nan, arr)
        return arr

    def mask(self):
        image = self._get_band('b1')
        image = array(image, dtype=float32)
        image[image < 1.] = nan
        arr = where(isnan(image), 0, 1)
        return arr


class Landsat5(LandsatImage):
    def __init__(self, obj):
        LandsatImage.__init__(self, obj)

        if self.satellite != 'LT5':
            raise ValueError('Must init Landsat5 object with Landsat5 data, not {}'.format(self.satellite))

        # https://landsat.usgs.gov/esun
        self.ex_atm_irrad = (1958.0, 1827.0, 1551.0,
                             1036.0, 214.9, nan, 80.65)

        # old values from fmask.exe
        # self.ex_atm_irrad = (1983.0, 1796.0, 1536.0, 1031.0, 220.0, nan, 83.44)

        self.k1, self.k2 = 607.76, 1260.56

    def radiance(self, band):
        qcal_min = getattr(self, 'quantize_cal_min_band_{}'.format(band))
        qcal_max = getattr(self, 'quantize_cal_max_band_{}'.format(band))
        l_min = getattr(self, 'radiance_minimum_band_{}'.format(band))
        l_max = getattr(self, 'radiance_maximum_band_{}'.format(band))
        qcal = self._get_band('b{}'.format(band))
        rad = ((l_max - l_min) / (qcal_max - qcal_min)) * (qcal - qcal_min) + l_min

        return rad.astype(float32)

    def brightness_temp(self, band, temp_scale='K'):

        if band in [1, 2, 3, 4, 5, 7]:
            raise ValueError('LT5 brightness must be band 6')

        rad = self.radiance(band)
        brightness = self.k2 / (log((self.k1 / rad) + 1))

        if temp_scale == 'K':
            return brightness

        elif temp_scale == 'F':
            return brightness * (9 / 5.0) - 459.67

        elif temp_scale == 'C':
            return brightness - 273.15

        else:
            raise ValueError('{} is not a valid temperature scale'.format(temp_scale))

    def reflectance(self, band):
        """ 
        :param band: An optical band, i.e. 1-5, 7
        :return: At satellite reflectance, [-]
        """
        if band == 6:
            raise ValueError('LT5 reflectance must be other than  band 6')

        rad = self.radiance(band)
        esun = self.ex_atm_irrad[band - 1]
        toa_reflect = (pi * rad * self.earth_sun_dist ** 2) / (esun * cos(self.solar_zenith_rad))

        return toa_reflect

    def albedo(self, model='smith'):
        """Finds broad-band surface reflectance (albedo)
        
        Smith (2010),  “The heat budget of the earth’s surface deduced from space”
        LT5 toa reflectance bands 1, 3, 4, 5, 7
        # normalized i.e. 0.356 + 0.130 + 0.373 + 0.085 + 0.07 = 1.014
        
        Should have option for Liang, 2000; 
        
        Tasumi (2008), "At-Surface Reflectance and Albedo from Satellite for
                        Operational Calculation of Land Surface Energy Balance"
                        
        
        :return albedo array of floats
        """
        if model == 'smith':
            blue, red, nir, swir1, swir2 = (self.reflectance(1), self.reflectance(3), self.reflectance(4),
                                            self.reflectance(5), self.reflectance(7))
            alb = (0.356 * blue + 0.130 * red + 0.373 * nir + 0.085 * swir1 + 0.072 * swir2 - 0.0018) / 1.014
        elif model == 'tasumi':
            pass
        # add tasumi algorithm TODO
        return alb

    def saturation_mask(self, band, value=255):
        """ Mask saturated pixels, 1 (True) is saturated.
        :param band: Image band with dn values, type: array
        :param value: Maximum (saturated) value, i.e. 255 for 8-bit data, type: int
        :return: boolean array
        """
        dn = self._get_band('b{}'.format(band))
        mask = self.mask()
        mask = where((dn == value) & (mask > 0), True, False)

        return mask

    def ndvi(self):
        """ Normalized difference vegetation index.
        :return: NDVI
        """
        red, nir = self.reflectance(3), self.reflectance(4)
        ndvi = self._divide_zero((nir - red), (nir + red), nan)

        return ndvi

    def lai(self):
        """
        Leaf area index (LAI), or the surface area of leaves to surface area ground.
        Trezza and Allen, 2014
        :param ndvi: normalized difference vegetation index [-]
        :return: LAI [-]
        """
        ndvi = self.ndvi()
        lai = 7.0 * (ndvi ** 3)
        lai = where(lai > 6., 6., lai)
        return lai

    def emissivity(self, approach='tasumi'):

        ndvi = self.ndvi()

        if approach == 'tasumi':
            lai = self.lai()
            # Tasumi et al., 2003
            # narrow-band emissivity
            nb_epsilon = where((ndvi > 0) & (lai <= 3), 0.97 + 0.0033 * lai, nan)
            nb_epsilon = where((ndvi > 0) & (lai > 3), 0.98, nb_epsilon)
            nb_epsilon = where(ndvi <= 0, 0.99, nb_epsilon)
            return nb_epsilon

        if approach == 'sobrino':
            # Sobrino et el., 2004
            red = self.reflectance(3)
            bound_ndvi = where(ndvi > 0.5, ndvi, 0.99)
            bound_ndvi = where(ndvi < 0.2, red, bound_ndvi)

            pv = ((ndvi - 0.2) / (0.5 - 0.2)) ** 2
            pv_emiss = 0.004 * pv + 0.986
            emissivity = where((ndvi >= 0.2) & (ndvi <= 0.5), pv_emiss, bound_ndvi)

            return emissivity

    def land_surface_temp(self):
        """
        Mean values from Allen (2007)
        :return: 
        """
        rp = 0.91
        tau = 0.866
        rsky = 1.32
        epsilon = self.emissivity(approach='tasumi')
        radiance = self.radiance(6)
        rc = ((radiance - rp) / tau) - ((1 - epsilon) * rsky)
        lst = self.k2 / (log((epsilon * self.k1 / rc) + 1))
        return lst

    def ndsi(self):
        """ Normalized difference snow index.
        :return: NDSI
        """
        green, swir1 = self.reflectance(2), self.reflectance(5)
        ndsi = self._divide_zero((green - swir1), (green + swir1), nan)

        return ndsi


class Landsat7(LandsatImage):
    def __init__(self, obj):
        LandsatImage.__init__(self, obj)

        if self.satellite != 'LE7':
            raise ValueError('Must init Landsat7 object with Landsat5 data, not {}'.format(self.satellite))
        # https://landsat.usgs.gov/esun; Landsat 7 Handbook
        self.ex_atm_irrad = (1970.0, 1842.0, 1547.0, 1044.0,
                             255.700, nan, 82.06, 1369.00)

        self.k1, self.k2 = 666.09, 1282.71

    def radiance(self, band):
        if band == 6:
            band = '6_vcid_1'
        qcal_min = getattr(self, 'quantize_cal_min_band_{}'.format(band))
        qcal_max = getattr(self, 'quantize_cal_max_band_{}'.format(band))
        l_min = getattr(self, 'radiance_minimum_band_{}'.format(band))
        l_max = getattr(self, 'radiance_maximum_band_{}'.format(band))
        qcal = self._get_band('b{}'.format(band))
        rad = ((l_max - l_min) / (qcal_max - qcal_min)) * (qcal - qcal_min) + l_min
        return rad

    def brightness_temp(self, band=6, gain='low', temp_scale='K'):

        if band in [1, 2, 3, 4, 5, 7, 8]:
            raise ValueError('LE7 brightness must be either vcid_1 or vcid_2')

        if gain == 'low':
            # low gain : b6_vcid_1
            band_gain = '6_vcid_1'
        else:
            band_gain = '6_vcid_2'

        rad = self.radiance(band_gain)
        brightness = self.k2 / (log((self.k1 / rad) + 1))

        if temp_scale == 'K':
            return brightness

        elif temp_scale == 'F':
            return brightness * (9 / 5.0) - 459.67

        elif temp_scale == 'C':
            return brightness - 273.15

        else:
            raise ValueError('{} is not a valid temperature scale'.format(temp_scale))

    def reflectance(self, band):
        """ 
        :param band: An optical band, i.e. 1-5, 7
        :return: At satellite reflectance, [-]
        """
        if band in ['b6_vcid_1', 'b6_vcid_2']:
            raise ValueError('LE7 reflectance must not be b6_vcid_1 or b6_vcid_2')

        rad = self.radiance(band)
        esun = self.ex_atm_irrad[band - 1]
        toa_reflect = (pi * rad * self.earth_sun_dist ** 2) / (esun * cos(self.solar_zenith_rad))
        return toa_reflect

    def albedo(self):
        """Finds broad-band surface reflectance (albedo)
        
        Smith (2010),  “The heat budget of the earth’s surface deduced from space”
        Should have option for Liang, 2000; 
        
        LE7 toa reflectance bands 1, 3, 4, 5, 7
        
        # normalized i.e. 0.356 + 0.130 + 0.373 + 0.085 + 0.07 = 1.014
        :return albedo array of floats
        """
        blue, red, nir, swir1, swir2 = (self.reflectance(1), self.reflectance(3), self.reflectance(4),
                                        self.reflectance(5), self.reflectance(7))
        alb = (0.356 * blue + 0.130 * red + 0.373 * nir + 0.085 * swir1 + 0.072 * swir2 - 0.0018) / 1.014

        return alb

    def saturation_mask(self, band, value=255):
        """ Mask saturated pixels, 1 (True) is saturated.
        :param band: Image band with dn values, type: array
        :param value: Maximum (saturated) value, i.e. 255 for 8-bit data, type: int
        :return: boolean array
        """
        dn = self._get_band('b{}'.format(band))
        mask = where((dn == value) & (self.mask() > 0), True, False)

        return mask

    def ndvi(self):
        """ Normalized difference vegetation index.
        :return: NDVI
        """
        red, nir = self.reflectance(3), self.reflectance(4)
        ndvi = self._divide_zero((nir - red), (nir + red), nan)

        return ndvi

    def lai(self):
        """
        Leaf area index (LAI), or the surface area of leaves to surface area ground.
        Trezza and Allen, 2014
        :param ndvi: normalized difference vegetation index [-]
        :return: LAI [-]
        """
        ndvi = self.ndvi()
        lai = 7.0 * (ndvi ** 3)
        lai = where(lai > 6., 6., lai)
        return lai

    def emissivity(self, approach='tasumi'):

        ndvi = self.ndvi()

        if approach == 'tasumi':
            lai = self.lai()
            # Tasumi et al., 2003
            # narrow-band emissivity
            nb_epsilon = where((ndvi > 0) & (lai <= 3), 0.97 + 0.0033 * lai, nan)
            nb_epsilon = where((ndvi > 0) & (lai > 3), 0.98, nb_epsilon)
            nb_epsilon = where(ndvi <= 0, 0.99, nb_epsilon)
            return nb_epsilon

        if approach == 'sobrino':
            # Sobrino et el., 2004
            red = self.reflectance(3)
            bound_ndvi = where(ndvi > 0.5, ndvi, 0.99)
            bound_ndvi = where(ndvi < 0.2, red, bound_ndvi)

            pv = ((ndvi - 0.2) / (0.5 - 0.2)) ** 2
            pv_emiss = 0.004 * pv + 0.986
            emissivity = where((ndvi >= 0.2) & (ndvi <= 0.5), pv_emiss, bound_ndvi)

            return emissivity

    def land_surface_temp(self):
        rp = 0.91
        tau = 0.866
        rsky = 1.32
        epsilon = self.emissivity()
        rc = ((self.radiance(6) - rp) / tau) - ((1 - epsilon) * rsky)
        lst = self.k2 / (log((epsilon * self.k1 / rc) + 1))
        return lst

    def ndsi(self):
        """ Normalized difference snow index.
        :return NDSI
        """
        green, swir1 = self.reflectance(2), self.reflectance(5)
        ndsi = self._divide_zero((green - swir1), (green + swir1), nan)

        return ndsi


class Landsat8(LandsatImage):
    def __init__(self, obj):
        LandsatImage.__init__(self, obj)

        self.oli_bands = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def brightness_temp(self, band, temp_scale='K'):
        """Calculate brightness temperature of Landsat 8
    as outlined here: http://landsat.usgs.gov/Landsat8_Using_Product.php

    T = K2 / log((K1 / L)  + 1)

    and

    L = ML * Q + AL

    where:
        T  = At-satellite brightness temperature (degrees kelvin)
        L  = TOA spectral radiance (Watts / (m2 * srad * mm))
        ML = Band-specific multiplicative rescaling factor from the metadata
             (RADIANCE_MULT_BAND_x, where x is the band number)
        AL = Band-specific additive rescaling factor from the metadata
             (RADIANCE_ADD_BAND_x, where x is the band number)
        Q  = Quantized and calibrated standard product pixel values (DN)
             (ndarray img)
        K1 = Band-specific thermal conversion constant from the metadata
             (K1_CONSTANT_BAND_x, where x is the thermal band number)
        K2 = Band-specific thermal conversion constant from the metadata
             (K1_CONSTANT_BAND_x, where x is the thermal band number)

    Returns
    --------
    ndarray:
        float32 ndarray with shape == input shape
    """

        if band in self.oli_bands:
            raise ValueError('Landsat 8 brightness should be TIRS band (i.e. 10 or 11)')

        k1 = getattr(self, 'k1_constant_band_{}'.format(band))
        k2 = getattr(self, 'k2_constant_band_{}'.format(band))
        rad = self.radiance(band)
        brightness = k2 / log((k1 / rad) + 1)

        if temp_scale == 'K':
            return brightness

        elif temp_scale == 'F':
            return brightness * (9 / 5.0) - 459.67

        elif temp_scale == 'C':
            return brightness - 273.15

        else:
            raise ValueError('{} is not a valid temperature scale'.format(temp_scale))

    def reflectance(self, band):
        """Calculate top of atmosphere reflectance of Landsat 8
        as outlined here: http://landsat.usgs.gov/Landsat8_Using_Product.php
    
        R_raw = MR * Q + AR
    
        R = R_raw / cos(Z) = R_raw / sin(E)
    
        Z = 90 - E (in degrees)
    
        where:
    
            R_raw = TOA planetary reflectance, without correction for solar angle.
            R = TOA reflectance with a correction for the sun angle.
            MR = Band-specific multiplicative rescaling factor from the metadata
                (REFLECTANCE_MULT_BAND_x, where x is the band number)
            AR = Band-specific additive rescaling factor from the metadata
                (REFLECTANCE_ADD_BAND_x, where x is the band number)
            Q = Quantized and calibrated standard product pixel values (DN)
            E = Local sun elevation angle. The scene center sun elevation angle
                in degrees is provided in the metadata (SUN_ELEVATION).
            Z = Local solar zenith angle (same angle as E, but measured from the
                zenith instead of from the horizon).
    
        Returns
        --------
        ndarray:
            float32 ndarray with shape == input shape
    
        """

        if band not in self.oli_bands:
            raise ValueError('Landsat 8 reflectance should OLI band (i.e. bands 1-8)')

        elev = getattr(self, 'sun_elevation')
        dn = self._get_band('b{}'.format(band))
        mr = getattr(self, 'reflectance_mult_band_{}'.format(band))
        ar = getattr(self, 'reflectance_add_band_{}'.format(band))

        if elev < 0.0:
            raise ValueError("Sun elevation must be non-negative "
                             "(sun must be above horizon for entire scene)")

        rf = ((mr * dn.astype(float32)) + ar) / sin(deg2rad(elev))

        return rf

    def radiance(self, band):
        """Calculate top of atmosphere radiance of Landsat 8
        as outlined here: http://landsat.usgs.gov/Landsat8_Using_Product.php
    
        L = ML * Q + AL
    
        where:
            L  = TOA spectral radiance (Watts / (m2 * srad * mm))
            ML = Band-specific multiplicative rescaling factor from the metadata
                 (RADIANCE_MULT_BAND_x, where x is the band number)
            AL = Band-specific additive rescaling factor from the metadata
                 (RADIANCE_ADD_BAND_x, where x is the band number)
            Q  = Quantized and calibrated standard product pixel values (DN)
                 (ndarray img)
    
        Returns
        --------
        ndarray:
            float32 ndarray with shape == input shape
    """
        ml = getattr(self, 'radiance_mult_band_{}'.format(band))
        al = getattr(self, 'radiance_add_band_{}'.format(band))
        dn = self._get_band('b{}'.format(band))
        rad = ml * dn.astype(float32) + al

        return rad

    def albedo(self):
        """Smith (2010), finds broad-band surface reflectance (albedo)
        Should have option for Liang, 2000; Tasumi, 2008;
        
        LC8 toa reflectance bands 2, 4, 5, 6, 7
        
        # normalized i.e. 0.356 + 0.130 + 0.373 + 0.085 + 0.07 = 1.014
        :return albedo array of floats
        """

        blue, red, nir, swir1, swir2 = (self.reflectance(2), self.reflectance(4), self.reflectance(5),
                                        self.reflectance(6), self.reflectance(7))
        alb = (0.356 * blue + 0.130 * red + 0.373 * nir + 0.085 * swir1 + 0.072 * swir2 - 0.0018) / 1.014

        return alb

    def ndvi(self):
        """ Normalized difference vegetation index.
        :return: NDVI
        """
        red, nir = self.reflectance(4), self.reflectance(5)
        ndvi = self._divide_zero((nir - red), (nir + red), nan)

        return ndvi

    def lai(self):
        """
        Leaf area index (LAI), or the surface area of leaves to surface area ground.
        Trezza and Allen, 2014
        :param ndvi: normalized difference vegetation index [-]
        :return: LAI [-]
        """
        ndvi = self.ndvi()
        lai = 7.0 * (ndvi ** 3)
        lai = where(lai > 6., 6., lai)
        return lai

    def emissivity(self, approach='tasumi'):

        ndvi = self.ndvi()

        if approach == 'tasumi':
            lai = self.lai()
            # Tasumi et al., 2003
            # narrow-band emissivity
            nb_epsilon = where((ndvi > 0) & (lai <= 3), 0.97 + 0.0033 * lai, nan)
            nb_epsilon = where((ndvi > 0) & (lai > 3), 0.98, nb_epsilon)
            nb_epsilon = where(ndvi <= 0, 0.99, nb_epsilon)
            return nb_epsilon

        if approach == 'sobrino':
            # Sobrino et el., 2004
            red = self.reflectance(3)
            bound_ndvi = where(ndvi > 0.5, ndvi, 0.99)
            bound_ndvi = where(ndvi < 0.2, red, bound_ndvi)

            pv = ((ndvi - 0.2) / (0.5 - 0.2)) ** 2
            pv_emiss = 0.004 * pv + 0.986
            emissivity = where((ndvi >= 0.2) & (ndvi <= 0.5), pv_emiss, bound_ndvi)

            return emissivity

    def land_surface_temp(self):

        band = 10

        k1 = getattr(self, 'k1_constant_band_{}'.format(band))
        k2 = getattr(self, 'k2_constant_band_{}'.format(band))

        rp = 0.91
        tau = 0.866
        rsky = 1.32
        epsilon = self.emissivity()
        rc = ((self.radiance(band) - rp) / tau) - ((1 - epsilon) * rsky)
        lst = k2 / (log((epsilon * k1 / rc) + 1))
        return lst

    def ndsi(self):
        """ Normalized difference snow index.
        :return: NDSI
        """
        green, swir1 = self.reflectance(3), self.reflectance(6)
        ndsi = self._divide_zero((green - swir1), (green + swir1), nan)

        return ndsi

# =============================================================================================
