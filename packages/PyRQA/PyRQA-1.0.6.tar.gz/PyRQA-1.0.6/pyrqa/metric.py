#!/usr/bin/python
#
# This file is part of PyRQA.
# Copyright 2015 Tobias Rawald, Mike Sips.

"""
Distance metrics
"""

import math

import numpy as np

from pyrqa.base_classes import BaseMetric


class TaxicabMetric(BaseMetric):
    """
    Taxicab metric (L_1).
    """

    name = 'taxicab_metric'

    @classmethod
    def get_p(cls):
        return 1.0

    @classmethod
    def get_distance_time_series(cls,
                                 time_series_x,
                                 time_series_y,
                                 embedding_dimension,
                                 time_delay,
                                 index_x,
                                 index_y):

        distance = 0

        for idx in np.arange(embedding_dimension):
            temp_x = index_x + (idx * time_delay)
            temp_y = index_y + (idx * time_delay)

            distance += math.fabs(time_series_x[temp_x] - time_series_y[temp_y])

        return distance

    @classmethod
    def get_distance_vectors(cls,
                             vectors_x,
                             vectors_y,
                             embedding_dimension,
                             index_x,
                             index_y):
        distance = 0

        for idx in np.arange(embedding_dimension):
            temp_x = index_x * embedding_dimension + idx
            temp_y = index_y * embedding_dimension + idx

            distance += math.fabs(vectors_x[temp_x] - vectors_y[temp_y])

        return distance


class EuclideanMetric(BaseMetric):
    """
    Euclidean metric (L_2).
    """

    name = 'euclidean_metric'

    @classmethod
    def get_p(cls):
        return 2.0

    @classmethod
    def get_distance_time_series(cls,
                                 time_series_x,
                                 time_series_y,
                                 embedding_dimension,
                                 time_delay,
                                 index_x,
                                 index_y):
        distance = 0

        for idx in np.arange(embedding_dimension):
            temp_x = index_x + (idx * time_delay)
            temp_y = index_y + (idx * time_delay)

            distance += math.pow(time_series_x[temp_x] - time_series_y[temp_y], 2)

        return math.sqrt(distance)

    @classmethod
    def get_distance_vectors(cls,
                             vectors_x,
                             vectors_y,
                             embedding_dimension,
                             index_x,
                             index_y):
        distance = 0

        for idx in np.arange(embedding_dimension):
            temp_x = index_x * embedding_dimension + idx
            temp_y = index_y * embedding_dimension + idx

            distance += math.pow(vectors_x[temp_x] - vectors_y[temp_y], 2)

        return math.sqrt(distance)


class MaximumMetric(BaseMetric):
    """
    Maximum metric (L_inf).
    """

    name = 'maximum_metric'

    @classmethod
    def get_p(cls):
        return np.float("inf")

    @classmethod
    def get_distance_time_series(cls,
                                 time_series_x,
                                 time_series_y,
                                 embedding_dimension,
                                 time_delay,
                                 index_x,
                                 index_y):
        distance = np.finfo(np.float32).min

        for index in np.arange(embedding_dimension):
            temp_x = index_x + (index * time_delay)
            temp_y = index_y + (index * time_delay)

            value = math.fabs(time_series_x[temp_x] - time_series_y[temp_y])

            if value > distance:
                distance = value

        return distance

    @classmethod
    def get_distance_vectors(cls,
                             vectors_x,
                             vectors_y,
                             embedding_dimension,
                             index_x,
                             index_y):
        distance = np.finfo(np.float32).min

        for idx in np.arange(embedding_dimension):
            temp_x = index_x * embedding_dimension + idx
            temp_y = index_y * embedding_dimension + idx

            value = math.fabs(vectors_x[temp_x] - vectors_y[temp_y])

            if value > distance:
                distance = value

        return distance
