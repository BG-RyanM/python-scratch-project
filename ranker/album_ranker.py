import copy
from typing import Dict, Tuple, List, Set
from statistics import mean, variance, median, StatisticsError
import argparse
import math

from ranking_core import ScoreItem, RankItem, master_albums
from k_means import get_cluster_info

band_name = None
band_phases: Dict[str, Tuple[str, str]] = {}
key_users: List[str] = []
critical_star_ratings: Dict[int, float] = {}


# Maps album by chronological index (Rush == 0) to ScoreItem
score_dict: Dict[int, ScoreItem] = {}
total_users = 0

# Maps username to list of (album idx, ranking)
per_user_rankings: Dict[str, List[RankItem]] = {}


def process_album_lines(list_lines: List[str], user_name: str) -> bool:
    """
    Processes each line in human-created list down to an album index, a ranking, and a star rating,
    if provided.

    A line looks something like: "19. Test For Echo (2.5 stars) biggest highlight: Driven (6.7/10)"

    The part in () is used to determine star rating, in this case 2.5 stars.
    """
    global total_users
    if len(list_lines) > len(master_albums) or len(list_lines) == 0:
        print(f"Wrong number of master_albums for user {user_name}")
        return False

    # For making sure person has ranked all master_albums, with no duplicate rankings
    rankings_not_covered: Set[int] = set([(i + 1) for i in range(len(list_lines))])
    idx_to_rank_and_stars = {}

    for line in list_lines:
        # Extract ranking number
        ranking = ""
        # For dealing with spaces that precede the number
        accept_spaces = True
        for c in line:
            if c.isnumeric():
                accept_spaces = False
                ranking += c
            elif c.isspace() and accept_spaces:
                pass
            else:
                break
        ranking = int(ranking)

        # Figure out which album this is. All capitalized words in a global album entry must
        # match words in the human's text input.
        # Problem scenario: Metallica's "Reload" matches "Load" in album list, so we want to
        # go with higher-scoring match.
        ignore_words = {"The", "Of", "A"}
        album_to_match_score = {}
        for idx, album in enumerate(master_albums):
            album_words = album.split(" ")
            album_words = [
                word
                for word in album_words
                if not word[0].islower() and word not in ignore_words
            ]
            match = True
            match_score = 0
            for word in album_words:
                if word.lower() not in line.lower():
                    match = False
                    break
                match_score += len(word)
            if match:
                album_to_match_score[idx] = match_score

        if len(album_to_match_score) == 0:
            print(
                f"Could not process list for username {user_name}, failed on line {line}"
            )
            return False

        album_idx = -1
        best_score = -1
        for idx, score in album_to_match_score.items():
            if score > best_score:
                album_idx = idx
                best_score = score

        stars = extract_star_rating(line, user_name, album_idx)

        idx_to_rank_and_stars[album_idx] = (ranking, stars)
        rankings_not_covered.discard(ranking)

    if len(rankings_not_covered) > 0:
        print(
            f"Bad ranking numbers for user {user_name}, remaining numbers are {rankings_not_covered}"
        )
        return False

    # Record per-user ranked list. Update ranking scores across all users.
    per_user_rankings[user_name] = []
    for idx, rank_and_stars in idx_to_rank_and_stars.items():
        rank_item = RankItem(idx, rank_and_stars[0], rank_and_stars[1])
        per_user_rankings[user_name].append(rank_item)

    RankItem.adjust_list(per_user_rankings[user_name])

    # Update collective ranking scores
    for rank_item in per_user_rankings[user_name]:
        score_dict[rank_item.album_idx].add_ranking(rank_item.ranking)
        score_dict[rank_item.album_idx].add_stars_rating(rank_item.stars)

    total_users += 1
    return True


def process_master_album_list(list_lines: List[str]) -> bool:
    """
    Given a master album list (at the top of data file), process lines of input to determine
    master album list, band phases, and critic star ratings.

    Sample input lines:
    1. Boy @Classic U2 (4)
    2. October @Classic U2 (3)
    3. War @Classic U2 (5)
    etc...

    Returns True if processing successful.
    """
    expected_numbers = set([(i + 1) for i in range(len(list_lines))])
    phase_map: Dict[str, List[str]] = {}

    for line in list_lines:
        # Extract chronological number
        album_num_str = ""
        for c in line:
            if c.isnumeric():
                album_num_str += c
            else:
                break
        album_num = int(album_num_str)
        expected_numbers.discard(album_num)

        album_and_phase = line[len(album_num_str) :]
        album_and_phase = album_and_phase.lstrip(" .)")
        parts = album_and_phase.split("@")
        album_name = parts[0]
        album_name = album_name.rstrip()
        if len(parts) >= 2:
            # Get rid of critical rating part, e.g. (3.5)
            phase_names = [part.split("(")[0] for part in parts[1:]]
            phase_names = [pn.rstrip() for pn in phase_names]
        else:
            # Get rid of star rating info
            album_name = album_name.split("(")[0].rstrip()
            phase_names = []
        master_albums.append(album_name)

        for phase_name in phase_names:
            if phase_map.get(phase_name) is None:
                phase_map[phase_name] = []
            phase_map[phase_name].append(album_name)

        critical_stars = extract_star_rating(line)
        critical_star_ratings[album_num - 1] = critical_stars

    if len(expected_numbers) > 0:
        print("ERROR: bad master album list")
        return False

    for phase_name, album_list in phase_map.items():
        band_phases[phase_name] = (album_list[0], album_list[-1])

    for i in range(len(master_albums)):
        score_dict[i] = ScoreItem(i)

    return True


def extract_star_rating(line: str, user_name: str = "", album_idx: int = -1):
    """
    Extracts star rating from line of raw text. Can look like:
    (3.5)
    (3,5)
    (4/5)
    (7/10)
    (4 stars)
    (4/5 stars)

    :param line: line of user-created input
    :param user_name: name of user
    :param album_idx: index of album, chronological order
    :return: rating out of five stars maximum
    """
    parts = line.split("(")
    if len(parts) <= 1:
        return None
    stars = None
    for part in parts[1:]:
        if ")" not in part:
            continue
        text_str = part.split(")")[0]
        # We have a block of text like "*)", where * is some set of characters
        # Remove the word "stars" and "stars"
        text_str = text_str.replace("stars", "")
        text_str = text_str.replace("Stars", "")
        text_str = text_str.replace("star", "")
        text_str = text_str.replace("Star", "")
        # European people sometimes use comma instead of a decimal point
        text_str = text_str.replace(",", ".")
        text_str = text_str.rstrip()
        if "/" in text_str:
            subparts = text_str.split("/")
            try:
                numerator = float(subparts[0])
                denominator = float(subparts[1])
                stars = numerator * 5.0 / denominator
            except ValueError:
                pass
        else:
            try:
                stars = float(text_str)
                if stars > 5.0:
                    # this is a year, not star rating
                    stars = None
            except ValueError:
                pass
        if stars is not None:
            break

    return stars


def load_lists_file(filename: str) -> bool:
    """
    Processes an input file for a particular band. Look at one of the sample files to
    understand the format.
    :return: True if processing successful
    """
    global band_name, key_users
    try:
        with open(filename) as f:
            file_lines = f.readlines()
    except FileNotFoundError:
        message = f"couldn't open file {filename}"
        print(message)
        return
    file_lines = [line.replace("\n", "").lstrip() for line in file_lines]

    user_name = None
    album_lines = []
    auto_user_id = 0
    very_first_list = True
    found_error = False
    for line in file_lines:
        if len(line) == 0:
            continue
        if line[0] == "#":
            if len(album_lines) > 0:
                # We've now arrived at the second # in the file -- what to do?
                if very_first_list:
                    # Generate the master album list, now that raw input has been collected.
                    success = process_master_album_list(album_lines)
                    if not success:
                        return False
                    very_first_list = False
                else:
                    # Generate user rankings list from previously collected raw input.
                    success = process_album_lines(album_lines, user_name)
                    if not success:
                        found_error = True

            if len(line) > 2:
                user_name = line[2:]
                if very_first_list and "Master List" in user_name:
                    parts = user_name.split(":")
                    band_name = parts[1].lstrip()
                elif "*" in user_name:
                    parts = user_name.split("*")
                    user_name = parts[0].rstrip()
                    key_users.append(user_name)
            else:
                user_name = f"User{auto_user_id}"
                auto_user_id += 1
            album_lines = []
        if line[0].isnumeric() or line[1].isnumeric():
            album_lines.append(line)

    if len(album_lines) > 0:
        found_error = not process_album_lines(album_lines, user_name)

    return not found_error


def calculate_final_scores():
    """Calculate and print final rankings list, along with statistical analysis findings."""

    final_list: List[RankItem] = []

    ScoreItem.calculate_final_rankings(score_dict)

    for idx, score_item in score_dict.items():
        final_rank = score_item.get_average_rank()
        final_stars = score_item.get_average_star_rating()
        final_list.append(RankItem(idx, final_rank, final_stars))

    RankItem.sort_list(final_list)

    album_idx_to_underrated_score = {}
    album_idx_to_stars = {}

    print(f"{band_name} Studio Albums Ranked by {total_users} People")
    print("============================================")
    for i, item in enumerate(final_list):
        album_idx = item.album_idx
        nominal_rank = len(final_list) - i
        average_rank = item.ranking
        average_stars = item.stars
        album_idx_to_stars[album_idx] = average_stars
        stars_str = "--" if average_stars is None else f"{average_stars:.1f}"
        underrated_score = score_dict[album_idx].underrated_score
        album_idx_to_underrated_score[album_idx] = underrated_score
        print(
            f"{nominal_rank}. {master_albums[album_idx]}: average rank={average_rank:.3f}, average star rating={stars_str}"
        )

    print("\nStatistical Analysis")
    print("============================================")
    num_to_list = 3 if 3 < len(master_albums) else len(master_albums)
    scores = [(idx, score) for idx, score in album_idx_to_underrated_score.items()]
    scores.sort(key=lambda x: x[1])
    underrated_strs = []
    for i in range(num_to_list):
        underrated_strs.append(
            f"{master_albums[scores[-1 - i][0]]}: {scores[-1 - i][1]:.3f}"
        )
    print(f"Most underrated {band_name} albums: {', '.join(underrated_strs)}")
    overrated_strs = []
    for i in range(num_to_list):
        overrated_strs.append(f"{master_albums[scores[i][0]]}: {scores[i][1]:.3f}")
    print(f"Most overrated {band_name} albums: {', '.join(overrated_strs)}")

    abs_scores = [
        (idx, abs(score)) for idx, score in album_idx_to_underrated_score.items()
    ]
    abs_scores.sort(key=lambda x: x[1])
    fairly_ranked_strs = []
    for i in range(num_to_list):
        fairly_ranked_strs.append(
            f"{master_albums[abs_scores[i][0]]}: {abs_scores[i][1]:.3f}"
        )
    print(f"Most fairly-ranked {band_name} albums: {', '.join(fairly_ranked_strs)}")

    variance_scores = [
        (album_idx, score_item.variance) for album_idx, score_item in score_dict.items()
    ]
    variance_scores.sort(key=lambda x: x[1])
    controversial_strs = []
    for i in range(num_to_list):
        controversial_strs.append(
            f"{master_albums[variance_scores[-1 - i][0]]}: {variance_scores[-1 - i][1]:.3f}"
        )
    print(f"Most controversial {band_name} albums: {', '.join(controversial_strs)}")
    least_controversial_strs = []
    for i in range(num_to_list):
        least_controversial_strs.append(
            f"{master_albums[variance_scores[i][0]]}: {variance_scores[i][1]:.3f}"
        )
    print(
        f"Least controversial {band_name} albums: {', '.join(least_controversial_strs)}"
    )

    median_vs_mean_scores = [
        (
            album_idx,
            score_item.median / mean(score_item.user_rankings),
            score_item.median,
            mean(score_item.user_rankings),
        )
        for album_idx, score_item in score_dict.items()
    ]
    median_vs_mean_scores.sort(key=lambda x: x[1])
    print(
        f"Most negative dissent: {master_albums[median_vs_mean_scores[0][0]]} at {median_vs_mean_scores[0][2]:.3f}/{median_vs_mean_scores[0][3]:.3f} (lowest median-to-mean)"
    )
    print(
        f"Most positive dissent: {master_albums[median_vs_mean_scores[-1][0]]} at {median_vs_mean_scores[-1][2]:.3f}/{median_vs_mean_scores[-1][3]:.3f} (highest median-to-mean)"
    )

    print(
        "\n(* underrated = receives a higher average rank than its final rank, "
        "fair = average rank pretty close to final rank, "
        "controversial = a lot of variation in how people rank it)"
    )
    print(
        "(* positive dissent = people giving higher rankings feel more strongly than those giving lower ones)"
    )
    print(
        "(** note: an album can still be non-controversial if everyone agrees that it's bad)"
    )

    print("\nThe Critics")
    print("============================================")
    critically_overrated_ratio = 0.0
    critically_overrated_idx = -1
    critically_underrated_ratio = 10000000.0
    critically_underrated_idx = -1
    agreement_factor = 1000000.0
    agreement_idx = -1
    fan_stars_list = []
    critic_stars_list = []
    for idx in range(len(master_albums)):
        fan_stars = album_idx_to_stars.get(idx)
        if fan_stars:
            fan_stars_list.append(fan_stars)
        critic_stars = critical_star_ratings.get(idx)
        if critic_stars:
            critic_stars_list.append(critic_stars)
        if fan_stars and critic_stars:
            ratio = critic_stars / fan_stars
            if ratio < critically_underrated_ratio:
                critically_underrated_ratio = ratio
                critically_underrated_idx = idx
            if ratio > critically_overrated_ratio:
                critically_overrated_ratio = ratio
                critically_overrated_idx = idx
            if abs(1.0 - ratio) < agreement_factor:
                agreement_factor = abs(1.0 - ratio)
                agreement_idx = idx
    if critically_underrated_idx != -1 and critically_overrated_idx != -1:
        print(
            f"Most underrated by critics: {master_albums[critically_underrated_idx]}, "
            f"{critical_star_ratings[critically_underrated_idx]} vs "
            f"{album_idx_to_stars[critically_underrated_idx]:.1f} from fans"
        )
        print(
            f"Most overrated by critics: {master_albums[critically_overrated_idx]}, "
            f"{critical_star_ratings[critically_overrated_idx]} vs "
            f"{album_idx_to_stars[critically_overrated_idx]:.1f} from fans"
        )
        print(f"Most critic/fan consensus: {master_albums[agreement_idx]}")
    if len(fan_stars_list) > 0 and len(critic_stars_list) > 0:
        print(
            f"Overall critic rating vs fan rating of {band_name}: {mean(critic_stars_list):.1f} / {mean(fan_stars_list):.1f}"
        )

    # Generate critic ranking list
    critic_list = [
        RankItem(idx, 0, stars) for idx, stars in critical_star_ratings.items()
    ]
    critic_list.sort(key=lambda x: x.album_idx)
    critic_list.sort(key=lambda x: x.stars)
    for i, item in enumerate(critic_list):
        item.ranking = len(master_albums) - i
    critic_album_strs = []
    for item in critic_list:
        critic_album_strs.append(f"{item.ranking}. {master_albums[item.album_idx]}")
    print(f"Ranked list from critics: {', '.join(critic_album_strs)}")
    per_user_rankings["The Critics"] = critic_list

    do_phase_rankings(final_list)
    score_key_users(final_list)


def do_phase_rankings(final_list: List[RankItem]):
    """
    Calculate and print statistical info about band's various "phases". A
    phase is a chronologically consecutive series of albums, covering some
    "era" in the band's life (e.g. maybe they got a new lead singer).
    """
    if len(band_phases) == 0:
        return
    print(f"\nPhases of {band_name} ranked:")
    print("============================================")
    best_phase_average = 10000000.0
    best_phase = None
    phase_info_list = []
    for phase, tup in band_phases.items():
        try:
            start_index = master_albums.index(tup[0])
            end_index = master_albums.index(tup[1])
        except ValueError:
            print("ERROR: Something bad happened with phase rankings...")
            return
        in_phase_list = [
            item for item in final_list if (start_index <= item.album_idx <= end_index)
        ]
        RankItem.sort_list(in_phase_list)
        albums_by_name = [master_albums[item.album_idx] for item in in_phase_list]
        phase_average = mean([item.ranking for item in in_phase_list])
        try:
            phase_star_average = mean(
                [item.stars for item in in_phase_list if item.stars is not None]
            )
            phase_star_str = f"({phase_star_average:.1f} stars) "
        except (StatisticsError, TypeError):
            phase_star_str = ""
        phase_line = (
            f"* {phase} (from {tup[0]} to {tup[1]}): average of {phase_average:.3f} {phase_star_str}across "
            f"{len(in_phase_list)} albums: {', '.join(albums_by_name)}"
        )
        phase_info_list.append((phase_average, phase_line))

        if phase_average < best_phase_average:
            best_phase = phase
            best_phase_average = phase_average

    phase_info_list.sort(key=lambda x: x[0])
    for tup in phase_info_list:
        print(tup[1])

    print(f"Most popular phase: {best_phase}")


def score_key_users(final_list: List[RankItem]):
    """
    Collect and print statistics about certain key users, marked with a "*" in input file.
    """
    if len(key_users) <= 0:
        return
    print("\nFans of Interest")
    print("============================================")
    if "The Critics" not in key_users:
        key_users.append("The Critics")
    most_stereotypical_key_user = None
    most_stereotypical_score = 100000.0
    least_stereotypical_key_user = None
    least_stereotypical_score = 0.0
    scores_by_user = {}
    for key_user in key_users:
        host_list = per_user_rankings[key_user]
        success, score = RankItem.compare_lists(host_list, final_list)
        scores_by_user[key_user] = score
        if score < most_stereotypical_score and key_user != "The Critics":
            most_stereotypical_score = score
            most_stereotypical_key_user = key_user
        if score > least_stereotypical_score and key_user != "The Critics":
            least_stereotypical_score = score
            least_stereotypical_key_user = key_user

    scores_by_user_list = [
        (user_name, score) for user_name, score in scores_by_user.items()
    ]
    scores_by_user_list.sort(key=lambda x: x[1])
    info_strs = []
    for tup in scores_by_user_list:
        info_strs.append(f"{tup[0]}: {tup[1]:.3f}")
    print(f"Key fan scores (lower is more stereotypical): {', '.join(info_strs)}")

    print(f"Most stereotypical {band_name} fan: {most_stereotypical_key_user}")
    print(f"Least stereotypical {band_name} fan: {least_stereotypical_key_user}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script for generating a 'collective' ranking of a band's albums, based on user rankings"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=False,
        default=None,
        help="File containing user-created rankings and master album list",
    )
    parser.add_argument(
        "--clusters",
        type=int,
        required=False,
        default=0,
        help="Number of fan clusters to find",
    )
    parser.add_argument(
        "--top_n_slots",
        type=int,
        required=False,
        default=5,
        help="Paired with 'clusters', number of top albums to show per cluster",
    )
    parser.add_argument(
        "--random_clusters",
        action="store_true",
        default=False,
        help="Paired with 'clusters'; if set, generate random clusters initially",
    )

    args = parser.parse_args()

    success = load_lists_file(args.file)
    if success:
        calculate_final_scores()
        if args.clusters > 0:
            get_cluster_info(
                num_groups=args.clusters,
                top_n_slots=args.top_n_slots,
                use_random_clusters=args.random_clusters,
                per_user_rankings=per_user_rankings,
                master_albums=master_albums,
            )
        print(
            "\nMethodology: User lists and host lists (including star ratings, where provided) are pasted into text file,"
        )
        print(
            "which is then processed and analyzed by Python script. Text file also includes info about artist and"
        )
        print("album names. Critic star ratings come from Allmusic.com.")
    else:
        print("*** Not calculating rankings: error in input data. ***")
