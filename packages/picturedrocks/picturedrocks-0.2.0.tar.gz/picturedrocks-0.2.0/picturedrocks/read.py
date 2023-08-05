# Copyright © 2017, 2018 Anna Gilbert, Alexander Vargo, Umang Varma
#
# This file is part of PicturedRocks.
#
# PicturedRocks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PicturedRocks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PicturedRocks.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd

from anndata import AnnData
from warnings import warn
import numpy as np


def read_clusts(adata, filename, sep=",", copy=False):
    """Read cluster labels from a csv

    Args
    ----
    adata: anndata.AnnData
        the `AnnData` object to read labels into
    filename: str
        filename of the csv file with labels
    sep: str, optional
        csv delimiter 
    copy: bool
        determines whether a copy of `AnnData` object is returned

    Returns
    -------
    anndata.AnnData
        object with cluster labels
    
    Notes
    -----
     * Cluster ids will automatically be changed so they are 0-indexed
     * csv can either be two columns (in which case the first column is treated
       as observation label and merging handled by pandas) or one column (only
       cluster labels, ordered as in ``adata``)
    """
    adata = adata.copy() if copy else adata
    clustdf = pd.read_csv(filename, sep=sep)
    if clustdf.shape[1] == 2:
        clustdf = clustdf.set_index(clustdf.columns[0])
    assert clustdf.shape[1] == 1, "Cluster column ambigious"
    clusters = clustdf.iloc[:, 0]
    if clusters.dtype.kind == "i":
        if clusters.min() > 0:
            warn("Changing cluster ids to begin at 0.")
            clusters -= clusters.min()
        clustuniq = np.sort(clusters.unique())
        assert np.array_equal(
            clustuniq, np.arange(clustuniq.size)
        ), "Cluster ids need to be 0, 1, ..., K-1"
        adata.obs["y"] = clusters
        adata.obs["clust"] = ("Cluster " + clusters.astype("str")).astype("category")
    else:
        adata.obs["clust"] = clusters.astype("category")
        adata.obs["y"] = adata.obs["clust"].cat.codes
    if adata.obs["y"].isnull().any() or adata.obs["clust"].isnull().any():
        warn("Some or all cells not assigned to cluster.")
    return adata


def process_clusts(adata, copy=False):
    """Annotate with information about clusters

    Precomputes cluster indices, number of clusters, etc.

    Args
    ----
    adata: anndata.AnnData
    copy: bool
        determines whether a copy of `AnnData` object is returned

    Return
    -------
    anndata.AnnData
        object with annotation

    Notes
    ------
    The information computed here is lost when saving as a `.loom` file. If a
    `.loom` file has cluster information, you should run this function
    immediately after :func:`sc.read_loom <scanpy.api.read_loom>`.
    """
    adata = adata.copy() if copy else adata
    adata.obs["clust"] = adata.obs["clust"].astype("category")
    adata.uns["num_clusts"] = adata.obs["clust"].cat.categories.size
    clusterindices = {}
    for k in range(adata.uns["num_clusts"]):
        clusterindices[k] = (adata.obs["y"] == k).nonzero()[0]
    adata.uns["clusterindices"] = clusterindices
    return adata
