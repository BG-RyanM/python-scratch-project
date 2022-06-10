from random import randrange
from typing import Tuple

# Globals
alphabet = []
word_list = []
word_scores = {}
game_master = GameMaster()
player = Player(game_master, False)


def create_word_list():
    """
    Builds a list of allowable words by reading in a text file.
    """
    global word_list, alphabet
    with open('FiveLetterWords.txt') as f:
        lines = f.readlines()

    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    word_set = set()

    for line in lines:
        word = line.strip().lower()
        # Remove entries with non-letter characters
        valid = True
        for let in word:
            if let not in alphabet:
                valid = False
                break

        if valid:
            # in case duplicates
            if word not in word_set:
                word_set.add(word)
                word_list.append(word)

    word_list.sort()

def determine_word_scores():
    # A list of dictionaries of {letter: count}, one for each positions
    letter_counts = []
    # A list of tuples of (best score, best letter)
    best_letters = []
    for i in range(5):
        the_dict = {}
        for a in alphabet:
            the_dict[a] = 0
        letter_counts.append(the_dict)
        best_letters.append((0, 'a'))

    for word in word_list:
        for i, c in enumerate(word):
            letter_counts[i][c] += 1

    for word in word_list:
        score = 0
        for i, c in enumerate(word):
            count = letter_counts[i][c]
            score += count
            tup = best_letters[i]
            if count > tup[0]:
                best_letters[i] = (count, c)
        word_scores[word] = score
        #print(f"score of word {word} is {score}")
    #print("total words are", len(word_list))
    #print("best letters are", best_letters)


class GameMaster:
    """
    This class runs the game, handling player guesses and doing all necessary record-keeping.
    """

    def __init__(self):
        self.guesses_left = 0
        self.correct_word = None
        self.last_guess = None
        self.definite_letters = None
        self.eliminated_letters = None
        self.misplaced_letters = None
        self.misplaced_letter_count = None
        self.misplaced_letter_map = None
        self.reset()
        self.allow_non_words = False

    def reset(self):
        """
        Call before starting a new game, to reset data.
        """
        word_list_size = len(word_list)
        self.guesses_left = self.total_guesses = 6
        self.correct_word = None if word_list_size == 0 else word_list[randrange(word_list_size)]
        self.last_guess = None
        self.definite_letters = [None for i in range(5)]
        # Letters no longer usable, though they might have been correct choices earlier
        self.eliminated_letters = set()
        # Misplaced = right letter, wrong position
        self.misplaced_letters = set()
        # The minimum number of times the letter appears in the word
        self.misplaced_letter_count = {}
        # Maps a letter to an list of True/False marking where it has/hasn't been tried.
        self.misplaced_letter_map = {}
        for c in alphabet:
            self.misplaced_letter_count[c] = 0
            self.misplaced_letter_map[c] = [False for i in range(5)]

    def get_score(self):
        return self.total_guesses - self.guesses_left

    def handle_guess(self, guess: str) -> Tuple[bool, list, list, list]:
        """
        Handles a guess from the player. Returns lists of green, yellow, and gray letters,
        where green letters are in the right place, yellow letters are in the answer word,
        but the wrong place in the guess word, and gray letters aren't in the word at all.

        In each list, the letter's position corresponds to its place in the guess word.
        If no letter of that color was present at the position, then the value is None.

        :param guess: string containing the guess
        :return: tuple containing (True if guess was acceptable,
        """
        if not self.allow_non_words and guess not in word_list:
            print("Not a valid word!")
            return False, [], [], []

        """
        Process:
        1. Mark any green letters in the guess, cross them off in the goal word (so they can't be marked yellow)
        2. Mark any yellow letters in the guess, crossing each off in the goal word. This step goes from left
           to right. If the player guesses the same letter twice and that letter in in the goal word twice,
           then there will be two yellows.
        3. Mark any gray letters in the guess.
        4. Update the overall list of definite letters.
        5. Update the overall list of misplaced letters.
        6. Update the overall list of eliminated letters.
        """

        guess_array = [c for c in guess]
        correct_word_array = [c for c in self.correct_word]
        green_letters = [None for i in range(5)]
        gray_letters = [None for i in range(5)]
        yellow_letters = [None for i in range(5)]

        # Determine all greens, remove these letters (in final word) as option for yellows
        for i in range(5):
            let = guess_array[i]
            if let == correct_word_array[i]:
                green_letters[i] = let
                correct_word_array[i] = None

        # Find yellows and grays
        # From the internet:
        #    If you guess a repeated letter more times than it appears in the word of the day,
        #    the first use of that letter will turn yellow and the second will turn gray,
        for i in range(5):
            let = guess_array[i]
            if let != green_letters[i]:
                if let in correct_word_array:
                    yellow_letters[i] = let
                    # eliminate the letter in the target word so it won't be flagged by
                    # another yellow
                    idx = correct_word_array.index(let)
                    correct_word_array[idx] = None
                else:
                    gray_letters[i] = let

        # Add any greens to definite list
        for i, c in enumerate(green_letters):
            if c is not None:
                if self.definite_letters[i] is None:
                    # This green letter was not previously recorded as a definite
                    # Remove it from tracking as a misplaced letter (if there)
                    if c in self.misplaced_letters:
                        self.misplaced_letter_count[c] -= 1
                        pos_list = self.misplaced_letter_map[c]
                        pos_list[i] = True
                        if self.misplaced_letter_count[c] == 0:
                            # This is no longer a misplaced letter at all
                            self.misplaced_letters.remove(c)
                            for i in range(5):
                                pos_list[i] = True
                self.definite_letters[i] = c

        """
        Add any yellows to misplaced list. Reasoning by example:

        Two yellows for a "b" imply at least two Bs, maybe more. As long as the number of 
        untried slots for "b" equals or exceeds two, then we know that there are two Bs yet
        to be placed. When a B lands in the right slight and turns green, then we drop the
        count by one.
        """
        misplaced_counts_in_turn = {}
        for i, c in enumerate(yellow_letters):
            if c is not None:
                self.misplaced_letters.add(c)
                if misplaced_counts_in_turn.get(c) is None:
                    misplaced_counts_in_turn[c] = 0
                misplaced_counts_in_turn[c] += 1
                pos_list = self.misplaced_letter_map[c]
                pos_list[i] = True
        for c, count in misplaced_counts_in_turn.items():
            if self.misplaced_letter_count[c] < misplaced_counts_in_turn[c]:
                self.misplaced_letter_count[c] = misplaced_counts_in_turn[c]

        # Add any grays to the eliminated list
        for i, c in enumerate(gray_letters):
            if c is not None:
                if c not in self.misplaced_letters:
                    self.eliminated_letters.add(c)

        self.guesses_left -= 1
        self.last_guess = guess
        return True, gray_letters, yellow_letters, green_letters

    def get_all_yellow_letters(self):
        """
        For all currently known misplaced letters, return a string containing the letter
        at all positions where placeable. If not placeable, then put in "_" instead.
        :return: list of strings, one for each letter
        """
        ret_list = []
        for let in self.misplaced_letters:
            entry = ""
            pos_list = self.misplaced_letter_map.get(let)
            for tried in pos_list:
                if tried:
                    entry += "_"
                else:
                    entry += let
            ret_list.append(entry)
        return ret_list

    def get_hint(self):
        """
        Prints a hint for the player.
        """
        self.print_data()
        usable_words = self.get_usable_words()
        print(f"There are {len(usable_words)} valid choices")
        if len(usable_words) > 5:
            hint = usable_words[randrange(len(usable_words))]
            print(f"Hint word is: {hint}")

    def print_data(self):
        """
        Prints data about game in progress.
        """
        print("unplaced:", self.misplaced_letters)
        print("definite:", self.definite_letters)
        print("eliminated:", self.eliminated_letters)

    def get_usable_words(self):
        """
        Returns a list of all words in master list that are still usable, given
        successfully placed, misplaced, and eliminated letters.
        :return: the list
        """
        usable_words = []
        for word in word_list:
            keep = True
            # Eliminate words with unusable letters or letters that don't align with "definite" letters
            for i, c in enumerate(word):
                if self.definite_letters[i] is not None and self.definite_letters[i] != c:
                    keep = False
                    break
                if c in self.eliminated_letters:
                    if c not in self.definite_letters:
                        keep = False
                        break

            # Make sure misplaced letters are present in reasonable places
            for let in self.misplaced_letters:
                if let in word:
                    # Letter is in the word, but is it an untried slot?
                    found_slot = False
                    pos_list = self.misplaced_letter_map.get(let)
                    for i, tried in enumerate(pos_list):
                        if not tried and word[i] == let:
                            found_slot = True
                            break
                    if not found_slot:
                        keep = False
                        break
                else:
                    keep = False
                    break
            if keep:
                usable_words.append(word)
        return usable_words

    def select_usable_word(self, usable_words: list):
        best_score = 0
        best_word = None
        for word in usable_words:
            score = word_scores[word]
            if score > best_score:
                best_score = score
                best_word = word
        return best_word

    def _count_possible_slots_for_misplaced_letter(self, letter):
        """
        Returns count of number of slots in which letter can still be placed.
        """
        pos_list = self.misplaced_letter_map[letter]
        count = 0
        for tried in pos_list:
            count += 0 if tried else 1
        return count

class Player:
    """
    This class represents the game player. It can either manage a game for a human player
    or play automatically itself.
    """

    def __init__(self, game_master: GameMaster, human_player: bool):
        self.game_master = game_master
        self.automatic_play = not human_player

    def handle_guess(self) -> Tuple[bool, bool]:
        """
        Makes a single guess or handles one from human player.
        :return: tuple of (True if player won, True if player quit)
        """
        if self.automatic_play:
            return self._handle_robot_guess()
        else:
            return self._handle_human_guess()

    def print_help(self):
        """
        Prints out the user manual.
        """
        print("\nManual:")
        print("Enter your word guess or use one of the following commands:")
        print("'q' or 'exit': Exit game")
        print("'hint': Get a hint")
        print("'answer': Show the answer")
        print("'nonwords': Allow non-words to be guesses")
        print("'words': Only words from the dictionary file can be guesses")
        print("'help': Show these instructions")

    def _handle_human_guess(self) -> Tuple[bool, bool]:
        guess_num = self.game_master.total_guesses - self.game_master.guesses_left + 1
        print(f"\nGuess {guess_num}/{self.game_master.total_guesses}")
        guess = input("> ")
        if guess == self.game_master.correct_word:
            print("You win!! Yay.")
            return True, False
        if guess == "q" or guess == "exit":
            return False, True
        if guess == "hint":
            self.game_master.get_hint()
            return False, False
        if guess == "answer":
            print(f"Answer is: {self.game_master.correct_word}")
            return False, False
        if guess == "nonwords":
            self.game_master.allow_non_words = True
            return False, False
        if guess == "words":
            self.game_master.allow_non_words = False
            return False, False

        success, gray_letters, yellow_letters, green_letters = self.game_master.handle_guess(guess)
        remaining_letters = [a for a in alphabet if a not in self.game_master.eliminated_letters]
        remaining_letters_str = self._to_string(remaining_letters, True)
        print(f"Gray letters:   {self._to_string(gray_letters)}")
        print(f"Green letters:  {self._to_string(green_letters)}")
        print(f"Yellow letters: {self._to_string(yellow_letters)}")
        print(f"\nLetters left:   {remaining_letters_str}")
        print(f"Definite:       {self._to_string(self.game_master.definite_letters)}")
        print(f"All yellows:    {self._to_string(self.game_master.get_all_yellow_letters(), True)}")
        return False, False

    def _handle_robot_guess(self) -> Tuple[bool, bool]:
        guess_num = self.game_master.total_guesses - self.game_master.guesses_left + 1
        usable_words = self.game_master.get_usable_words()
        if len(usable_words) == 0:
            print(f"ERROR: no usable words, answer was {self.game_master.correct_word}")
            print("")
            self.game_master.print_data()
            return False, True
        guess = self.game_master.select_usable_word(usable_words)
        success, gray_letters, yellow_letters, green_letters = self.game_master.handle_guess(guess)
        print(f"\nGuess is: {guess}. Turn {guess_num} of {self.game_master.total_guesses}")
        if guess == self.game_master.correct_word:
            print(f"Victory!")
            return True, False
        if guess_num >= self.game_master.total_guesses:
            print("Out of guesses, game over. Defeat!")
            return False, True
        print(f"Gray letters:   {self._to_string(gray_letters)}")
        print(f"Green letters:  {self._to_string(green_letters)}")
        print(f"Yellow letters: {self._to_string(yellow_letters)}")
        return False, False

    def _to_string(self, array, commas=False):
        """
        Given an array of strings or single characters, produce a human-readable string
        :param array: the input list
        :param commas: if True, then commas will separate items in the string
        :return: the string
        """
        ret_str = ""
        comma_str = ", " if commas else ""
        for c in array:
            let = "_" if c is None else c
            if len(ret_str) == 0:
                ret_str = f"{let}"
            else:
                ret_str += f"{comma_str}{let}"
        return ret_str


def run_game() -> Tuple[bool, int]:
    game_master.reset()
    while game_master.guesses_left > 0:
        won, quit = player.handle_guess()
        if quit or won:
            break
    score = game_master.get_score()
    return game_master.guesses_left > 0, score


def run_many_games(game_count):
    global game_master, player
    create_word_list()
    determine_word_scores()
    player.print_help()

    victory_count = 0
    defeat_count = 0
    average_score = 0.0
    for g in range(game_count):
        victory, score = run_game()
        if victory:
            victory_count += 1
            average_score = (average_score * float(victory_count) + float(score)) / float(victory_count + 1)
        else:
            defeat_count += 1
    print("\nResults:")
    print(f"Total games:     {game_count}")
    print(f"Total victories: {victory_count}")
    print(f"Total defeats:   {defeat_count}")
    print(f"Average score:   {average_score}")

run_many_games(100)