"""
Copyright (C) 2017, 申瑞珉 (Ruimin Shen)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import inspect

import inflection
import numpy as np
import cv2


def rescale(image, yx_min, yx_max, height, width):
    _height, _width = image.shape[:2]
    scale = np.array([height / _height, width / _width], np.float32)
    image = cv2.resize(image, (width, height))
    yx_min *= scale
    yx_max *= scale
    return image, yx_min, yx_max


class Rescale(object):
    def __init__(self):
        self.fn = eval(inflection.underscore(type(self).__name__))

    def __call__(self, data, height, width):
        data['image'], data['yx_min'], data['yx_max'] = self.fn(data['image'], data['yx_min'], data['yx_max'], height, width)
        return data


def resize(config, image, yx_min, yx_max, height, width):
    fn = eval(config.get('data', inspect.stack()[0][3]))
    return fn(image, yx_min, yx_max, height, width)


class Resize(object):
    def __init__(self, config):
        self.config = config
        self.fn = eval(config.get('data', inflection.underscore(type(self).__name__)))

    def __call__(self, data, height, width):
        data['image'], data['yx_min'], data['yx_max'] = self.fn(data['image'], data['yx_min'], data['yx_max'], height, width)
        return data

def random_crop(config, image, yx_min, yx_max, height, width):
    name = inspect.stack()[0][3]
    scale = config.getfloat('augmentation', name)
    assert 0 < scale <= 1
    _yx_min = np.min(yx_min, 0)
    _yx_max = np.max(yx_max, 0)
    dtype = yx_min.dtype
    size = np.array(image.shape[:2], dtype)
    margin = scale * np.random.rand(4).astype(dtype) * np.concatenate([_yx_min, size - _yx_max], 0)
    _yx_min = margin[:2]
    _yx_max = size - margin[2:]
    _ymin, _xmin = _yx_min
    _ymax, _xmax = _yx_max
    _ymin, _xmin, _ymax, _xmax = tuple(map(int, (_ymin, _xmin, _ymax, _xmax)))
    image = image[_ymin:_ymax, _xmin:_xmax, :]
    yx_min, yx_max = yx_min - _yx_min, yx_max - _yx_min
    return resize(config, image, yx_min, yx_max, height, width)


class RandomCrop(object):
    def __init__(self, config):
        self.config = config
        self.fn = eval(inflection.underscore(type(self).__name__))

    def __call__(self, data, height, width):
        data['image'], data['yx_min'], data['yx_max'] = self.fn(self.config, data['image'], data['yx_min'], data['yx_max'], height, width)
        return data
