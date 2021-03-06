"""Unit tests for CDBScan algorithm
"""
import numpy as np
from sklearn.metrics import adjusted_rand_score
from ..cdbscan import cdbscan


def test_easy_clusters_no_constraints():
    """Tests a simple clustering when
    there are two easily distinguishable clusters
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [2, 3],
                       [50, 4],
                       [51, 2]])
    epsilon = 5
    minpts = 2
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts)
    expected = [0, 1, 0, 0, 1, 1]
    assert adjusted_rand_score(expected, clusters) == 1


def test_fully_constrained():
    """Tests clustering for what looks
    like two easily distinguishable clusters,
    but is fully constrained to make
    a unexpected clustering
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [2, 3],
                       [50, 4],
                       [51, 2]])
    epsilon = 5
    minpts = 2
    mustlink = set([(0, 1), (2, 3), (4, 5)])
    cannotlink = set([(0, 2), (1, 4), (3, 5)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=mustlink, cannotlink=cannotlink)
    expected = [0, 0, 1, 1, 2, 2, ]
    assert adjusted_rand_score(expected, clusters) == 1


def test_fully_must_constrained():
    """Tests clustering for what looks
    like two easily distinguishable clusters,
    but must-link constraints
    end up merging every cluster
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [50, 4],
                       [2, 3],
                       [51, 2]])
    epsilon = 5
    minpts = 2
    mustlink = set([(0, 1), (2, 3), (3, 4)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=mustlink)
    expected = [0, 0, 0, 0, 0, 0]
    assert adjusted_rand_score(expected, clusters) == 1


def test_fully_cannot_constrained():
    """Tests clustering for what looks
    like two easily distinguishable clusters,
    but cannot-link constraints
    end up breaking every cluster
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [50, 4],
                       [2, 3],
                       [51, 2]])
    epsilon = 5
    minpts = 2
    cannotlink = set([(0, 2), (2, 4), (1, 5), (3, 5)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       cannotlink=cannotlink)
    expected = [0, 1, 2, 3, 4, 5]
    assert adjusted_rand_score(expected, clusters) == 1


def test_mustlink_merging():
    """Tests clustering for what looks
    like two easily distinguishable clusters,
    but a single must-link constraint
    ends up merging the clusters
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [50, 4],
                       [2, 3],
                       [51, 2]])
    epsilon = 5
    minpts = 2
    mustlink = set([(0, 1)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=mustlink)
    expected = [0, 0, 0, 0, 0, 0]
    assert adjusted_rand_score(expected, clusters) == 1


def test_singleton_outlier():
    """Tests clustering when
    a single point is an outlier
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [50, 4],
                       [2, 3],
                       [51, 2],
                       [100, 200]])
    epsilon = 5
    minpts = 2
    mustlink = set([(0, 1)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=mustlink)
    expected = [0, 0, 0, 0, 0, 0, -1]
    assert adjusted_rand_score(expected, clusters) == 1


def test_outlier_cluster():
    """Tests clustering
    when two points make an outlier cluster
    and minpts is higher than two
    """
    points = np.array([[1, 1],
                       [52, 3],
                       [1, 2],
                       [50, 4],
                       [2, 3],
                       [51, 2],
                       [100, 200],
                       [100, 201]])
    epsilon = 5
    minpts = 3
    mustlink = set([(0, 1)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=mustlink)
    expected = [0, 0, 0, 0, 0, 0, -1, -1]
    assert adjusted_rand_score(expected, clusters) == 1


def test_connection_through_alpha():
    """Tests a more complex situation
    where there are three distinguishable clusters
    of 3 points each,
    and two points make bridges between the clusters,
    merging all of them in the end
    """
    points = np.array([[1, 1], [2, 2], [2, 1],  # cluster 1
                       [4, 5], [5, 4], [5, 5],  # cluster 2
                       [9, 1], [8, 0], [13, 2],  # cluster 3
                       [3, 3], [7, 3]])  # bridges between 1-2 and 2-3
    epsilon = 4
    minpts = 2
    mustlink = set([(7, 8)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=mustlink)
    expected = np.zeros(points.shape[0])
    assert adjusted_rand_score(expected, clusters) == 1


def test_merge_mustlink_when_cannotlink():
    """
    Tests whether the algorithm handles the following situtation correctly:
    There are 2 clusters c1={a,b,c} and c2{d,e,f} with constraints
    must_link={(a, d), (b, e)} and cannot_link={c,f}.
    The algorithm should not merge the clusters c1 and c2 AND should not crash (obviously).
    """
    points = np.array([[0, 0], [0, 1], [1, 0],  # cluster 1
                       [10, 10], [11, 10], [10, 11]])  # cluster 2
    epsilon = 1
    minpts = 3
    must_link = set([(0, 3), (1, 4)])
    cannot_link = set([(2, 5)])
    clusters = cdbscan(points, epsilon=epsilon, minpts=minpts,
                       mustlink=must_link, cannotlink=cannot_link)
