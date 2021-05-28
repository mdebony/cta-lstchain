import pytest
import numpy as np
from scipy.sparse import csr_matrix


@pytest.mark.parametrize('fraction', [0.2, 0.5])
def test_psf_smearer(fraction):
    from lstchain.image.modifier import random_psf_smearer, set_numba_seed

    set_numba_seed(0)

    # simple toy example with a single 7 pixel hexgroup
    image = np.zeros(7)

    # really large number so we can make tight checks on the distributed photon counts
    # 0 is the central, then clockwise
    image[0] = 10000

    neighbor_matrix = csr_matrix(np.array([
       #0  1  2  3  4  5  6
       [0, 1, 1, 1, 1, 1, 1],  # 0
       [1, 0, 1, 0, 0, 0, 1],  # 1
       [1, 1, 0, 1, 0, 0, 0],  # 2
       [1, 0, 1, 0, 1, 0, 0],  # 3
       [1, 0, 0, 1, 0, 1, 0],  # 4
       [1, 0, 0, 0, 1, 0, 1],  # 5
       [1, 1, 0, 0, 0, 1, 0],  # 6
    ]))


    smeared = random_psf_smearer(image, fraction, neighbor_matrix.indices, neighbor_matrix.indptr)
    # no charge lost in this case
    assert image.sum() == smeared.sum()

    # test charge is distributed into neighbors
    assert np.isclose(smeared[0], (1 - fraction) * image[0], rtol=0.01)
    assert np.allclose(smeared[1:], image[0] * fraction / 6, rtol=0.1)

    # test not all pixels got the same charge
    # (could happen by chance, but *very* unlikely at 10000 photons)
    assert np.any(smeared[1:] != smeared[1])

    # if we put charge in the edges, we should loose some
    image[1:] = 0.1 * image[0]
    smeared = random_psf_smearer(image, fraction, neighbor_matrix.indices, neighbor_matrix.indptr)
    assert smeared.sum() < image.sum()
