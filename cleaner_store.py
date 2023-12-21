"""
    clearner_store.py defines the structures an algorithms for text cleaning.

    The
"""

import warnings, re
from nltk.corpus import stopwords
import pandas as pd
import gensim

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
class PhraseStore():

    def __init__(self, change_phrases=None):
        self._word_list = pd.DataFrame(columns=['Target', 'Replace', 'Active', 'Deleted'])
        if change_phrases is not None:
            self.add(change_phrases)
            
        # stop just needs the word to remove (even if join word) tuple = (word,'')
        # -
        # swap needs a [list] to swap with a [list] e.g. (['AB'],['A','B']),  (['A','B'],['C','D']),
        # join needs a list of words to join. i.e. tuple = (['A','B','C])

        # if add is a tuple: assume it is correct for behaviour
        # If add is a tuple with single non-list item, assume a stop (single word) : (word) -> ([word],[''])
        # If is a tuple with single list item with single item, assume a stop (single word) : ([word]) -> ([word],[''])
        # If is a tuple with single list item with multiple strings, assume is join: (['A','B','C']) -> (['A','B','C'])
        # IF is a tupel with two items, ether of which, is a string, then

    def convert(self, change_phrases=None):
        """
            Default is that assumes it is a list of yuples
        :param change_phrases:
        :return:
        """
        if isinstance(change_phrases, list):
            if len(change_phrases) < 1:
                warnings.warn("No values added")
            elif isinstance(change_phrases[0], tuple):
                change_phrases = [self.convert(each) for each in change_phrases]                              # If list of tuples, check indevidual types
            elif isinstance(change_phrases[0], str):
                change_phrases = self._list_convert(change_phrases)

        elif isinstance(change_phrases, str):
            change_phrases = (change_phrases, '') # Default single string, is a stop word (nothign to exchange)
        elif isinstance(change_phrases, tuple):
            if isinstance(change_phrases[0], str):
                change_phrases = (change_phrases,'_'.join(change_phrases))
            elif isinstance(change_phrases[0], list):
                pass

        return change_phrases

    """ 
    if a list of strings, then it is a list of stop words
    if it is a list of tuples then it is a swap word (join words and stopwrods included)
    if it is a tuple of strings, it is a join word 
    if it is a tuple of lists, it is a swap word.
    """

    def _list_convert(self, change_phrases):
        return [(each,'') for each in change_phrases]

    def add(self, change_phrase=None, active=True):
        """
            Adds a change_phrase or set of change_phrases to the internal table

        :param change_phrase:
        :return:
        """
        change_phrase = self.convert(change_phrase)
        if isinstance(change_phrase, list):
            for each in change_phrase:
                self._word_list.loc[len(self._word_list)] = {'Target': each[0],
                                                             'Replace': each[1],
                                                             'Active': active,
                                                             'Deleted': False}
        else:
            self._word_list.loc[len(self._word_list)] = {'Target': change_phrase[0],
                                                         'Replace': change_phrase[1],
                                                         'Active': active,
                                                         'Deleted': False}

        if len(self._word_list) > 1:
            self._word_list = self._word_list.drop_duplicates()

    def remove(self, change_phrase=None):
        if not isinstance(change_phrase,int):
            change_phrase = self.id(change_phrase)

        self._word_list.drop(change_phrase)

    def id(self, change_phrase):
        if isinstance(change_phrase,int):
            return change_phrase
        else:
            return self._word_list.index[self._word_list['Target']==change_phrase].tolist()[0]

    def edit(self, change_phrase=None, value=None, column='Active'):
        if change_phrase is None:
            if value is None:
                return list(self._word_list[column])
            else:
                self._word_list[column] = value
        else:
            if not isinstance(change_phrase, int):
                change_phrase = self.id(change_phrase)
            if value is None:
                return self._word_list.loc[column,change_phrase]
            else:
                self._word_list.loc[column,change_phrase] = value

    def delete(self, change_phrase=None):
        if change_phrase is None:
            warnings.warn("Need to define Words to delete")
        else:
            self.edit(change_phrase=change_phrase,value=True,column='Deleted')

    def status(self, change_phrase=None, active=True):
        self.edit(change_phrase=change_phrase,value=active,column='Active')

    def toggle(self, change_phrase=None):
        value = not self.edit(change_phrase=change_phrase, value=None, column='Active')
        self.edit(change_phrase=change_phrase,value=value, column='Active')
        
    def words(self):
        return self.edit(change_phrase=None, value=None, column='Target')
    
    def as_table(self):
        return self._word_list
    
    def as_tuples(self):
        return [(self._word_list.loc[item,each] for item in self._word_list.columns ) for each in self._word_list.index]


class PhraseCleaner(PhraseStore):

    def __init__(self, change_phrases=None):
        super(PhraseCleaner, self).__init__(change_phrases=change_phrases)
        
    def __call__(self, text=None):
        if text is None:
            return self._word_list
        else:
            return self.clean_text(text)
        
    def valid_tuples(self):
        return[(self._word_list.loc[id,'Target'],self._word_list.loc[id,'Replace'])
         for id in self._word_list.index
         if (self._word_list.loc[id,'Active'] and not self._word_list.loc[id,'Deleted'])]

    def clean_text(self, text):
        local = self.valid_tuples()
        sw = wswaper()
        return sw.change_phrases(text, swaps=local)




    

    """ 
    List manipulation
        add (single)
        add (block)
        delete (single)
        set (
    
    Status manipulation
        state
    Save and load status. 
    
    
    """

    """

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
"""

class wswaper():

    @staticmethod
    def single_spaces(text):
        return re.sub(' +', ' ', text)

    @staticmethod
    def change_phrase(text, swap, caps_sens=True, cleaned=True):
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

        if isinstance(target, tuple):
            target = [word for word in target]

        if isinstance(replacement, str):
            replacement = [replacement]

        if isinstance(replacement, tuple):
            target = [word for word in replacement]

        # If the text is a single string, then a simple regex should work
        if isinstance(text, str):
            # Replace a string of the target words, separated by spaces, with a string of replacement words, separated
            # by spaces.
            if caps_sens:
                flags = re.IGNORECASE
            else:
                flags = re.NOFLAG

            if 0:
                out_text =  re.sub(str(' '.join(target).encode('unicode_escape')),
                              str(' '.join(replacement).encode('unicode_escape')),
                              text,flags = flags) # TODO: Confirm the problems with escapes.
            else:
                out_text = re.sub("{}".format(' '+' '.join(target)+' '),
                                  "{}".format(' '+' '.join(replacement)+' '),
                                  text,
                                  flags=flags)
            if cleaned:
                out_text = wswaper.single_spaces(out_text)
            return out_text

        elif isinstance(text, list):
            # If the text is a list of words, treat all words as seprate
            if len(target) == 1:
                if len(replacement) == 1:
                    # If there is only a single word target and single word replacement, just go through each word and swap
                    out_text =  [word if word != target[0] else replacement[0] for word in text]
                else:
                    # If there is a single target word, but an extended replacement phrase, accumulate updates
                    out_text = []
                    for word in text:
                        if word == target[0]:
                            out_text += replacement
                        else:
                            out_text.append(word)
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
        if cleaned:
            out_text = [word for word in out_text if word != '']

        return out_text

    def change_phrases(self, text, swaps):
        for swap in swaps:
            text = self.change_phrase(text, swap)
        return text

    def remove_phrases(self, text, targets):
        for target in targets:
            text = self.change_phrase(text, target, [])

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



if __name__ == '__main__':

    join_word_list = [('social', 'media'), ('et', 'al'), ('google', 'scholar'), ('big', 'data'), ('web', 'science'),
                      ('science', 'google'),
                      ('crossref', 'google'), ('machine', 'learning'), ('new', 'york'), ('african', 'american'),
                      ('united', 'states'), ('crossref', 'web'),
                      ('data',
                       'collection')]

    swap_word_list = [(['bd'], ['big', 'data'])]

    wordsets = {}
    wordsets['stops'] = PhraseCleaner(stopwords.words('english'))
    wordsets['joins'] = PhraseCleaner(join_word_list)
    wordsets['swaps'] = PhraseCleaner(swap_word_list)

    print(wordsets['stops'])

    """ 
    if a list of strings, then it is a list of stop words
    if it is a list of tuples then it is a swap word (join words and stopwrods included)
    if it is a tuple of strings, it is a join word 
    if it is a tuple of lists, it is a swap word.
    """

    test_text = "Introduction Big data (BD) is difficult to define. Precisely the features, scope, purview or threshold" \
                " of BD continues to sow confusions and generate ethical controversies. Despite the preceding, the " \
                "emerging consensus (Ekbia et al. 2015: p. 3; Alharthi et al. 2017: p. 286) is that BD is characterized" \
                " by 5 Vs: Volume (that is, a vast amount of datasets requiring innovative and big tools for capturing, " \
                "storing and analyzing); variety (un/semi/structured and collected from diverse sources);" \
                " velocity (rapidly evolving datasets and expanded by actual data streams); " \
                "veracity (that is, data uncertainty, quality, reliability or predictive force); " \
                "and value (this is the artificial intelligence that is created either for learning new patterns " \
                "in vast datasets or offering personalized services).There is a growing adoption of BD in various " \
                "fields (engineering, life sciences, business, behavioural studies, online and offline commerce, " \
                "education and politics). This article focuses on healthcare big data use and access. Healthcare " \
                "big data (HBD) come from different sources such as sequencing data, Electronic Health Records " \
                "(EHR), biological specimens, Quantified Self (QS), biomedical data, patient-reported data, " \
                "biomarker data, medical imaging, large clinical trials; which may be stored in repositories or " \
                "biobanks (Mittelstadt et al. 2016: p. 306). Other means of expanding HBD streams include healthcare " \
                "literature databases like PubMed, automated sources like health and fitness devices and volunteered " \
                "sources such as e-health networks like patientslikeme.HBD analytics integrates, explores, identifies" \
                " clusters, correlates, analyze and infer (with an unparalleled degree of exactitude) based on datasets" \
                " from the preceding complex heterogeneous sources to create – HBD – value or (artificial) intelligence" \
                " for offering a range of personalized health services, support health policies or clinical decisions," \
                " or advance science (Michael et al. 2013: p. 22). The HDB value relies mostly on analytic techniques" \
                " such as algorithms and machine learning that are generated from processed data. HBD may be " \
                "processed by using graphics processing units or cloud computing. The advancement in the omics " \
                "studies, patient-contributed online data, imaging processes and the increasing affordability and " \
                "accessibility of health electronic devices also imply that a large volume of heterogeneous data can " \
                "now be analyzed to create HBD intelligence at a low cost. Advances have also been made in " \
                "extracting previously difficult text data (from doctor’s notes, millions of books photographs " \
                "from the past) for data analytics and mining purposes.Notwithstanding its (potential) benefits, HBD" \
                " also creates a challenge for all stakeholders such as data utilizers, contributors and " \
                "beneficiaries of HBD intelligence. New digital technologies can empower, yet they are also " \
                "intrusive. HBD vividly exemplifies this dual character (Ekbia et al. 2015: p. 27). As an example, " \
                "digital surveillance can usefully provide support for contact tracing in the event of a virus " \
                "outbreak such as the COVID-19/Ebola outbreak. It could also monitor an individual’s healthcare " \
                "decisions, behaviors or outcomes with the aim of fostering healthy habits and practices in the " \
                "individual or the wider population, providing critical insights on health needs or status, " \
                "assisting with the development of equitable interventions. However, it also introduces a level of " \
                "oversight that significantly threatens individuals’ privacy.Furthermore, HBD may also be abused or " \
                "misused. The literature is awash with examples of data misuse."

    test_text = gensim.utils.simple_preprocess(str(test_text), deacc=True)

    swaped = wordsets['swaps'](test_text)
    joined = wordsets['joins'](swaped)
    stoped = wordsets['stops'](joined)
    print(stoped)