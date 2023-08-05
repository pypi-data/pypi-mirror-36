import argparse
from functools import partial
from typing import Callable, Optional, Tuple, Union

import numpy as np
import xarray as xr

from starfish.image._filter.gaussian_low_pass import GaussianLowPass
from starfish.stack import ImageStack
from starfish.types import Number
from ._base import FilterAlgorithmBase
from .util import preserve_float_range, validate_and_broadcast_kernel_size


class GaussianHighPass(FilterAlgorithmBase):

    def __init__(
            self, sigma: Union[Number, Tuple[Number]], is_volume: bool=False, **kwargs
    ) -> None:
        """Gaussian high pass filter

        Parameters
        ----------
        sigma : Union[Number, Tuple[Number]]
            standard deviation of gaussian kernel
        is_volume : bool
            If True, 3d (z, y, x) volumes will be filtered, otherwise, filter 2d tiles
            independently.

        """
        self.sigma = validate_and_broadcast_kernel_size(sigma, is_volume)
        self.is_volume = is_volume

    @classmethod
    def add_arguments(cls, group_parser: argparse.ArgumentParser) -> None:
        group_parser.add_argument(
            "--sigma", type=float, help="standard deviation of gaussian kernel")
        group_parser.add_argument(
            "--is-volume", action="store_true",
            help="indicates that the image stack should be filtered in 3d")

    @staticmethod
    def high_pass(
            image: Union[xr.DataArray, np.ndarray], sigma: Union[Number, Tuple[Number]]
    ) -> Union[xr.DataArray, np.ndarray]:
        """
        Applies a gaussian high pass filter to an image

        Parameters
        ----------
        image : numpy.ndarray[np.uint16]
            2-d or 3-d image data
        sigma : Union[Number, Tuple[Number]]
            Standard deviation of gaussian kernel

        Returns
        -------
        np.ndarray :
            filtered image of the same shape as the input image

        """

        blurred = GaussianLowPass.low_pass(image, sigma)
        filtered = image - blurred
        filtered = preserve_float_range(filtered)

        return filtered

    def run(
            self, stack: ImageStack, in_place: bool=True, verbose: bool=True,
            n_processes: Optional[int]=None
    ) -> Optional[ImageStack]:
        """Perform filtering of an image stack

        Parameters
        ----------
        stack : ImageStack
            Stack to be filtered.
        in_place : bool
            if True, process ImageStack in-place, otherwise return a new stack
        verbose : bool
            if True, report on filtering progress (default = False)
        n_processes : Optional[int]
            Number of parallel processes to devote to calculating the filter

        Returns
        -------
        Optional[ImageStack] :
            if in-place is False, return the results of filter as a new stack

        """
        high_pass: Callable = partial(self.high_pass, sigma=self.sigma)
        result = stack.apply(
            high_pass, is_volume=self.is_volume, verbose=verbose, in_place=in_place,
            n_processes=n_processes
        )
        if not in_place:
            return result
        return None
