from itertools import combinations
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import KDTree
from .constraint import *
import numpy as np

NEIGHBORHOOD_MIN_POINTS = 50
NEIGHBORHOOD_RADIUS = 2


def compute_density_reachable_points(dataset, point_index, maximum_distance):
    element_count = dataset.shape[0]
    distances = pairwise_distances(X=dataset, metric="euclidean")

    def compute_neighbors(element_index):
        return tuple(i for i in range(element_count)
                     if distances[point_index, i] <= maximum_distance)

    # Storing points already visited to prevent infinite loops
    points_already_visited = set()

    # The initial set of density_reachable points is the neighborhood of
    # the point
    density_reachable = set(compute_neighbors(point_index))

    new_points_to_explore = True
    while new_points_to_explore:
        old_reachable_point_count = len(density_reachable)
        reachable_neighborhoods = [compute_neighbors(i) for i in density_reachable
                                   if i not in points_already_visited]
        points_already_visited.update(density_reachable)
        for neighborhood in reachable_neighborhoods:
            density_reachable.update(neighborhood)
        new_points_to_explore = old_reachable_point_count < len(density_reachable)

    return density_reachable


def cdbscan(dataset, epsilon=0.01, minpts=5, mustlink=None, cannotlink=None):
    """
    Step 1 -> Partition the data space with a KD-Tree
    kdtree := BuildKDTree(D)

    Step 2 -> Create local clustersin the KD-Tree
    for each leaf node v in kdtree and each unlabeled point pi in v do
        DR(pi) := all points density-reachable from pi within eps
        if |DR(pi)| < MinPts then
            Label pi as NOISE_POINT
        else if exists a constraint CL among points in DR(pi) then
            Each point in DR(pi) and pi becomes one LOCAL_CLUSTER
        else
            Label pi as CORE_POINT
            All of {pi} U DR(pi) becomes one LOCAL_CLUSTER
        end
    end

    Step 3a -> Merge clusters and enforce the Must-Link constraints
    for each constraint in ML do
        Let p, p' be the data points in the constraint
        Find the clusters C, C' with p in C and p' in C'
        Merge C, C' into cluster Cnew := C U C' and label it as ALPHA_CLUSTER
    end

    Step 3b -> Build the final clusters
    while number of local clusters decreases do
        for each local cluster C do
            Let C' be the closest ALPHA_CLUSTER that is density-reachable from C
            if exists no constraint in CL between points of C, C' then
                Incorporate C into C', i.e. C' := C U C'
            end
        end
    end
    return each ALPHA_CLUSTER and each remaining LOCAL_CLUSTER
    """
    return None


def run_test():
    X = [
        (0, 0),
        (0, 1),
        (1, 0),
        (10, 0),
        (11, 1),
        (9, 0)]
    X = np.array(X)

    dr = compute_density_reachable_points(dataset=X,
                                          point_index=0,
                                          maximum_distance=NEIGHBORHOOD_RADIUS)
    print(dr)


if __name__ == "__main__":
    run_test()
