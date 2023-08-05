from copy import deepcopy

import numpy as np

from starfish.stack import ImageStack
from starfish.util.synthesize import SyntheticData


def divide(array, value):
    return array / value


def test_apply():
    """test that apply correctly applies a simple function across 2d tiles of a Stack"""
    stack = ImageStack.synthetic_stack()
    assert (stack.numpy_array == 1).all()
    stack.apply(divide, value=2)
    assert (stack.numpy_array == 0.5).all()


def test_apply_3d():
    """test that apply correctly applies a simple function across 3d volumes of a Stack"""
    stack = ImageStack.synthetic_stack()
    assert np.all(stack.numpy_array == 1)
    stack.apply(divide, value=4, is_volume=True)
    assert (stack.numpy_array == 0.25).all()


def test_apply_labeled_dataset():
    """
    test that apply correctly applies a simple function across starfish-generated synthetic data
    """
    original = SyntheticData().spots()
    image = deepcopy(original)
    image.apply(divide, value=2)
    assert np.all(image.numpy_array == original.numpy_array / 2)


def test_apply_not_in_place():
    """
    test that apply correctly applies a simple function across a starfish stack without modifying
    original data
    """
    image = SyntheticData().spots()
    new = image.apply(divide, value=2, in_place=False)
    assert np.all(new.numpy_array == image.numpy_array / 2)
