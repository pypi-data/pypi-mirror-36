from functools import partial
from typing import Optional

import numpy as np

from starfish.stack import ImageStack
from ._base import FilterAlgorithmBase


class Clip(FilterAlgorithmBase):

    def __init__(self, p_min: int=0, p_max: int=100, is_volume: bool=False, **kwargs) -> None:
        """Image clipping filter

        Parameters
        ----------
        p_min : int
            values below this percentile are set to p_min (default 0)
        p_max : int
            values above this percentile are set to p_max (default 100)
        is_volume : bool
            If True, 3d (z, y, x) volumes will be filtered. By default, filter 2-d (y, x) tiles

        kwargs
        """
        self.p_min = p_min
        self.p_max = p_max
        self.is_volume = is_volume

    @classmethod
    def add_arguments(cls, group_parser) -> None:
        group_parser.add_argument(
            "--p-min", default=0, type=int, help="clip intensities below this percentile")
        group_parser.add_argument(
            "--p-max", default=100, type=int, help="clip intensities above this percentile")

    @staticmethod
    def clip(image: np.ndarray, p_min: int, p_max: int) -> np.ndarray:
        """Clip values of img below and above percentiles p_min and p_max

        Parameters
        ----------
        image : np.ndarray
            image to be clipped
        p_min : int
          values below this percentile are set to the value of this percentile
        p_max : int
          values above this percentile are set to the value of this percentile

        Notes
        -----
        - Wrapper for np.clip
        - No shifting or transformation to adjust dynamic range is done after clipping

        Returns
        -------
        np.ndarray :
          Numpy array of same shape as img

        """
        v_min, v_max = np.percentile(image, [p_min, p_max])

        # asking for a float percentile clipping value from an integer image will
        # convert to float, so store the dtype so it can be restored
        dtype = image.dtype
        image = image.clip(min=v_min, max=v_max)
        return image.astype(dtype)

    def run(
            self, stack: ImageStack, in_place: bool=True, verbose: bool=False,
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
            If True, report on the percentage completed (default = False) during processing
        n_processes : Optional[int]
            Number of parallel processes to devote to calculating the filter

        Returns
        -------
        Optional[ImageStack] :
            if in-place is False, return the results of filter as a new stack

        """
        clip = partial(self.clip, p_min=self.p_min, p_max=self.p_max)
        result = stack.apply(
            clip,
            is_volume=self.is_volume, verbose=verbose, in_place=in_place, n_processes=n_processes
        )
        if not in_place:
            return result
        return None
