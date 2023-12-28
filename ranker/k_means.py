import copy
from typing import List, Tuple, Dict, Optional

from ranking_core import RankItem, ScoreItem

"""
Code in this file implements a K-Means clustering heuristic. Individual user ranking
lists are essentially treated as vectors, with it being possible to measure distance
between them. A group of user ranking lists can be averaged together to obtain the
centroid for that group.

A rough explanation:
1. Start off with arbitrary centroids
2. Assign users to cluster based on nearest centroid
3. Recalculate centroid from all in cluster
4. Repeat (some number of times) from step 2.
"""


class KMeansCluster:

    """
    Represents a cluster, as described above.
    """

    def __init__(
        self,
        starting_list: Optional[List[RankItem]] = None,
        total_albums: Optional[int] = None,
    ):
        """
        :param starting_list: use this ranking list as starting centroid.
        """
        if total_albums is None:
            total_albums = len(starting_list)
        self.score_item_dict: Dict[int, ScoreItem] = {
            i: ScoreItem(i) for i in range(total_albums)
        }
        if starting_list:
            self.centroid_list: List[RankItem] = copy.deepcopy(starting_list)
        else:
            self.centroid_list = RankItem.random_list()
        self.users = []
        self._total_albums = total_albums

    def score_user_list(self, user_list: List[RankItem]) -> float:
        """
        Determine user "distance" from cluster centroid. Return it.
        """
        success, score = RankItem.compare_lists(user_list, self.centroid_list)
        return score

    def add_user_list(self, user_list: List[RankItem], user_name: str):
        """Add user list to cluster."""
        for item in user_list:
            self.score_item_dict[item.album_idx].add_ranking(item.ranking)
        self.users.append(user_name)

    def recalculate_centroid(self):
        """Average of all user lists in cluster"""
        min_acceptable_users = 2 if random_clusters else 1
        if len(self.users) < min_acceptable_users:
            if not random_clusters:
                print("ERROR: this shouldn't happen in K-Means Clustering")
            new_list = RankItem.random_list()
        else:
            new_list = []
            for album_idx, item in self.score_item_dict.items():
                new_list.append(RankItem(album_idx, item.get_average_rank()))

        self.score_item_dict: Dict[int, ScoreItem] = {
            i: ScoreItem(i) for i in range(self._total_albums)
        }
        self.centroid_list: List[RankItem] = new_list
        RankItem.sort_list(self.centroid_list)
        self.users = []


# For looking up user list by username
k_means_user_lists: Dict[str, List[RankItem]] = {}
k_means_clusters: List[KMeansCluster] = []
random_clusters = False


def do_cluster_assignment(master_albums: List[str], top_n_slots: int):
    """
    Perform K-Means clustering heuristic.
    :param master_albums: list of band's albums, in chronological order
    :param top_n_slots: We are only interested in printing the top N albums in each cluster
    """

    bottom_n_slots = 3

    x = 50
    while True:
        # Assign users to cluster based on nearness
        for user_name, user_list in k_means_user_lists.items():
            shortest_distance = 1000000000.0
            closest_cluster = 0
            for g, cluster in enumerate(k_means_clusters):
                distance = cluster.score_user_list(user_list)
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_cluster = g
            k_means_clusters[closest_cluster].add_user_list(user_list, user_name)

        x -= 1
        if x <= 0:
            break

        for g, cluster in enumerate(k_means_clusters):
            cluster.recalculate_centroid()

    # Each list contains album indices of top five albums in cluster, by album index
    top_n_lists = []
    bottom_n_lists = []
    for g, cluster in enumerate(k_means_clusters):
        top_n_lists.append(
            [item.album_idx for item in cluster.centroid_list[-top_n_slots:]]
        )
        bottom_n_lists.append(
            [item.album_idx for item in cluster.centroid_list[0:bottom_n_slots]]
        )
    top_n_sets = [set(l) for l in top_n_lists]
    intersection_set = top_n_sets[0].intersection(*top_n_sets[1:])
    bottom_n_sets = [set(l) for l in bottom_n_lists]
    bottom_intersection_set = bottom_n_sets[0].intersection(*bottom_n_sets[1:])

    print("\nFans Clusters (K-Means Clustering)")
    print("============================================")
    print(
        f"Most fans best fit one of the following. Select one of these top {top_n_slots} / bottom {bottom_n_slots} lists. * = not shared across all lists."
    )
    cluster_num = 1
    for set_idx, top_n_list in enumerate(top_n_lists):
        bottom_n_list = bottom_n_lists[set_idx]
        if len(top_n_list) > 0:
            top_albums = []
            for album_idx in top_n_list:
                star_str = "" if album_idx in intersection_set else " *"
                top_albums.append(f"{master_albums[album_idx]}{star_str}")
            top_albums.reverse()
            bottom_albums = []
            for album_idx in bottom_n_list:
                star_str = "" if album_idx in bottom_intersection_set else " *"
                bottom_albums.append(f"{master_albums[album_idx]}{star_str}")
            bottom_albums.reverse()
            print(
                f"Cluster {cluster_num} ({len(k_means_clusters[set_idx].users)} fans): "
                f"{', '.join(top_albums)}... {', '.join(bottom_albums)}"
            )
            cluster_num += 1


def get_cluster_info(
    num_groups: int,
    top_n_slots: int,
    use_random_clusters: bool,
    per_user_rankings: Dict[str, List[RankItem]],
    master_albums: List[str],
):
    """Do initialization, then run clustering heuristic."""
    global random_clusters
    random_clusters = use_random_clusters
    all_rank_lists = []
    for user_name, rank_list in per_user_rankings.items():
        new_list = copy.deepcopy(rank_list)
        RankItem.truncate_list(new_list, top_n_slots * 2)
        RankItem.expand_list(new_list)
        k_means_user_lists[user_name] = new_list
        all_rank_lists.append(new_list)

    for g in range(num_groups):
        if random_clusters:
            k_means_clusters.append(KMeansCluster(total_albums=len(master_albums)))
        else:
            k_means_clusters.append(KMeansCluster(all_rank_lists[g]))

    do_cluster_assignment(master_albums, top_n_slots)
