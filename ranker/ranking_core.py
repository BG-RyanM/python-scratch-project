from typing import List, Dict, Tuple
import math
import random
from statistics import mean, median, variance, StatisticsError


class RankItem:
    """
    Represents a single album in a ranked list. Contains album identifier, ranking number,
    and star rating (if available).
    """

    def __init__(self, idx, rank, stars=None):
        self.album_idx = idx
        self.ranking = rank
        self.stars = stars

    @staticmethod
    def sort_list(album_list: List, sort_chrono: bool = False):
        """Sorts a list of RankItem objects"""
        if sort_chrono:
            album_list.sort(key=lambda x: x.album_idx)
        else:
            album_list.sort(key=lambda x: x.ranking, reverse=True)

    @staticmethod
    def compare_lists(list1: List, list2: List) -> Tuple[bool, float]:
        """
        Returns a number that expresses 'distance' between two ranking lists. The higher
        the number, the more different the lists are.
        :return: (success, distance)
        """

        # Make list2 into a dict
        dict2 = {item.album_idx: item.ranking for item in list2}

        differences = []
        for rank_item in list1:
            if dict2.get(rank_item.album_idx):
                # Compare the two rankings
                diff = float(rank_item.ranking) - float(dict2[rank_item.album_idx])
                differences.append(diff * diff)
        return True, math.sqrt(sum(differences))

    @staticmethod
    def adjust_list(the_list: List):
        """
        If a ranking list is shorter than the total number of albums, (maybe) adjust
        the rankings. The idea is that the user might only have heard 13 / 15 albums
        (or whatever), so the rankings have to be stretched out a little to match
        complete lists. However, if the user gives a very short list, e.g. their top
        five only, it has to be assumed that the user is simply ignoring those albums
        they like less, which means no stretching.
        """
        list_size = len(the_list)
        total_albums = len(master_albums)
        adjustment_factor = float(total_albums) / float(list_size)
        # Only perform adjustment if list covers 75% or more of total master_albums.
        # Assumption is that user simply hasn't listened to a few.
        if (1.0 / adjustment_factor) < 0.75:
            return
        for rank_item in the_list:
            rank_item.ranking = rank_item.ranking * adjustment_factor

    @staticmethod
    def truncate_list(the_list: List, new_length: int):
        """Shortens ranking list down to length specified, keeping only highest-rated albums"""
        orig_len = len(the_list)
        new_length = new_length if new_length < len(the_list) else len(the_list)
        RankItem.sort_list(the_list)
        for i in range(orig_len - new_length):
            the_list.pop(0)

    @staticmethod
    def expand_list(the_list: List):
        """
        Expands ranking list to include all albums not given by user. These are
        simply given a ranking as though tied for Nth slot.
        """
        if len(the_list) >= len(master_albums):
            return

        master_album_indices = [i for i in range(len(master_albums))]
        filler_rank = len(the_list) + 1
        albums_present = set(master_album_indices)
        for item in the_list:
            albums_present.discard(item.album_idx)

        for album_idx in albums_present:
            the_list.append(RankItem(album_idx, filler_rank))

    @staticmethod
    def random_list():
        """Returns a randomized ranking list"""
        new_list = [(i, random.random()) for i in range(len(master_albums))]
        new_list.sort(key=lambda x: x[1])
        outlist = [RankItem(tup[0], i + 1) for i, tup in enumerate(new_list)]
        RankItem.sort_list(outlist)
        return outlist

    @staticmethod
    def rerank(the_list: List):
        """Reranks albums so that their ranking numbers match order in list"""
        total_albums = len(master_albums)
        RankItem.sort_list(the_list)
        for i, item in enumerate(the_list):
            item.ranking = total_albums - i


class ScoreItem:

    """
    Used to obtain statistical info about a particular album, based on how multiple
    users rate it.
    """

    def __init__(self, album_idx: int):
        """
        :param album_idx: represents chronological order of album, starting from zero
        """
        self.album_idx = album_idx
        self.user_rankings = []
        self.stars = []

        self.final_rank = -1
        self.underrated_score = 0.0
        self.variance = 0.0
        self.median = 0.0

    def add_ranking(self, ranking):
        """Adds user ranking, e.g. 3 for third-favorite album to that user"""
        self.user_rankings.append(ranking)

    def get_average_rank(self):
        """Return average rank based on multiple user rankings"""
        try:
            return mean(self.user_rankings)
        except StatisticsError as e:
            print(
                f"ERROR: exception for score item for {master_albums[self.album_idx]}, {e}"
            )
            return 0

    def add_stars_rating(self, stars):
        """Adds user star rating, with 5 stars being maximum"""
        if stars is None:
            return
        self.stars.append(stars)

    def get_average_star_rating(self):
        """Return average star rating across all users who provided one"""
        try:
            return mean(self.stars)
        except StatisticsError as e:
            return None
        except TypeError:
            print(f"What the hell? {self.stars}")

    @staticmethod
    def calculate_final_rankings(score_item_dict: Dict):
        """Calculate statistical information about album"""
        final_list: List[RankItem] = []
        for album_idx, score_item in score_item_dict.items():
            mean_rank = score_item.get_average_rank()
            mean_stars = score_item.get_average_star_rating()
            try:
                score_item.variance = variance(score_item.user_rankings)
            except StatisticsError as e:
                pass
            try:
                score_item.median = median(score_item.user_rankings)
            except StatisticsError as e:
                pass
            final_list.append(RankItem(album_idx, mean_rank, mean_stars))

        RankItem.sort_list(final_list)
        for idx, rank_item in enumerate(final_list):
            final_rank = len(master_albums) - idx
            score_item_dict[rank_item.album_idx].final_rank = final_rank
            score_item_dict[rank_item.album_idx].underrated_score = (
                float(final_rank) - rank_item.ranking
            )


# The master list of albums, by name, in chronological order
master_albums: List[str] = []
