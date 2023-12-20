"""
    clearner_store.py defines the structures an algorithms for text cleaning.

    The
"""

import warnings, re

import pandas as pd


class temprary():

    def __init__(self, stop_words=None, join_words=None, swap_words=None):
        self.word_cleaners = {}

        self.word_cleaners['stopwords'] = word_cleaner(word=stop_words) if stop_words is not None else None
        self.word_cleaners['stopwords_extension'] = word_cleaner(word=stop_words) if stop_words is not None else None
        self.word_cleaners['joinwords'] = word_cleaner(join=join_words) if join_words is not None else None
        self.word_cleaners['swapwords'] = word_cleaner(swap=swap_words) if swap_words is not None else None
        self.word_cleaners['hiddenwords'] = word_cleaner(swap=swap_words) if swap_words is not None else None

        # TODO: insert the STOPWORDS initialisation.


# behaviour
class word_cleaner():

    def __init__(self, wordset=None, behaviour=None):
        self.behaviour = 'stop' # 'stop', 'swap', 'join'

        # stop just needs the word to remove (even if join word) tuple = (word,'')
        # -
        # swap needs a [list] to swap with a [list] e.g. (['AB'],['A','B']),  (['A','B'],['C','D']),
        # join needs a list of words to join. i.e. tuple = (['A','B','C])

        # if add is a tuple: assume it is correct for behaviour
        # If add is a tuple with single non-list item, assume a stop (single word) : (word) -> ([word],[''])
        # If is a tuple with single list item with single item, assume a stop (single word) : ([word]) -> ([word],[''])
        # If is a tuple with single list item with multiple strings, assume is join: (['A','B','C']) -> (['A','B','C'])
        # IF is a tupel with two items, ether of which, is a string, then

    def __call__(self, text=None):
        if text is None:
            return self._word_list
        else:
            return wswaper.remove_words(text, self._word_list)

    # self._word_list.append(tuple(join.split())) TODO: joinword, split from string.
    def add(self, wordset=None):
        # Add a word or a list of words
        # Stop words do not work on phrases - to remove phrases, use the join_words
        if isinstance(wordset, tuple):
            self._word_list.append(wordset)         # If a TUPLE, assume its a singel in correct format.
        elif isinstance(wordset, str):
            self._word_list.append((wordset,''))    # If a string, assume its a STOPWORD like
        elif isinstance(wordset, list):
            if len(wordset) > 0:                    # If a list, check if a list of tuples, strings or other
                if isinstance(wordset[0], tuple):
                    self._word_list += wordset
                elif isinstance(wordset[0], str):
                    self._word_list.append((wordset))
                else:
                    warnings.warn('Unknown type of list items: must be tuples or strings')
        else:
            warnings.warn('Unknown type of wordset: Shoudl be a tuple, list or string')

    def word(self, word, replace=None):
        if replace is not None:
            word = (word,replace)
        self.add(word=word)

    def set(self, wordset=None):
        if wordset is None:
            self._word_list = []
        else:
            self._word_list = wordset

    def reset(self):
        self._word_list = []


class wswaper():

    @staticmethod
    def swap_phrase(text, swap):
        # Swaps a single phrase (set of words) for another phrase.
        # Text: is either a string, or a list of words
        # target: is a phrase (ordered list of words) to be replaced in the text
        # replacement: is a phrase with which to replace the target.
        # Target and Replacement are an array of individual words, and can be as lot as wanted.

        if not isinstance(swap, tuple):
            warnings.warn('Not a valid swap: Swap must be a tuple')
        else:
            target = swap[0]
            replacement = swap[1]

        if isinstance(target, str):
            target = [target]

        if isinstance(replacement, str):
            replacement = [replacement]

        # If the text is a single string, then a simple regex should work
        if isinstance(text, str):
            # Replace a string of the target words, separated by spaces, with a string of replacement words, separated
            # by spaces.
            return re.sub(' '+str(' '.join(target).encode('unicode_escape') )+ ' ',
                          ' '+str(' '.join(replacement).encode('unicode_escape')) + ' ',
                          text) # TODO: Confirm this works with Escape charaters + CHECK REPLAC ' ' WITH variable length stop/ounctuation

        # If the text is a list of words, treat all words as seprate
        if len(target) == 1:
            if len(replacement) == 1:
                # If there is only a single word target and single word replacement, just go through each word and swap
                return [word if word != target[0] else replacement[0] for word in text]
            else:
                # If there is a single target word, but an extended replacement phrase, accumulate updates
                out_text = []
                for word in text:
                    if word == target[0]:
                        out_text += replacement
                    else:
                        out_text.append(word)
                return out_text
        else:
            phrase_len = len(target)
            out_text = []
            text_len = len(text)
            i = 0
            while i < text_len:
                if text[i] == target[0]:
                    # If the current word in the text is the first in the target phrase, check if the following words
                    # also match.
                    sub_phrase = text[i:min(i + phrase_len, text_len)]
                    if sub_phrase == target:
                        # If they match, replace them all and skip to end of target phrase in input.
                        out_text = out_text + replacement
                        i += phrase_len
                    else:
                        # Else move onto next word
                        out_text.append(text[i])
                        i += 1
                else:
                    # else move onto next word
                    out_text.append(text[i])
                    i += 1
            return out_text

    def swap_phrases(self, text, swaps):
        for swap in swaps:
            text = self.swap_phrase(text, swap)
        return text

    def remove_phrases(self, text, targets):
        for target in targets:
            text = self.swap_phrase(text, target, [])

    def remove_words(self, text, word_list, invert=False):
        """
            Simplified version of remove_phrase that assumes the removal of single string words.

            N.B. This assumes stop words are not multi-term
        """

        if isinstance(text, str):
            text = self._from_str(text)

        if invert:
            out_text = [word for word in text if word in word_list]
        else:
            out_text = [word for word in text if word not in word_list]

        if isinstance(text,str):# TODO: Fix this
            out_text =  self._to_str(out_text)

        return out_text

    @staticmethod
    def split(text):
        return text.split()

    @staticmethod
    def join(text):
        return ' '.join(text)




