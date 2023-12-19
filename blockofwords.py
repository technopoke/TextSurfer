"""
    textblock.py defines the structural elements of set of textual inputs.

    The basic functions all work on the principle of a WORDBLOCK, each of which can be processed in almost identical
    ways, treated as a Structured piece of text or as a BOW as required. it also allows for scores to be applied and
    processed for each block. SENTENCES, PARAGRAPHS, DOCUMENTS and CORPUS are all treated as WORDBLOCKs but with
    minor adjustments in the behaviour of each.
"""

import warnings
import pandas as pd
# TODO: This document is still being moved over from the langStructures.py in LanguageForms project

class hydic():
    def __init__(self):
        pass


class WordBlock():
    """ WordBlock

        Basic unit of functionality for all textual structures. Edits to functionality should be added here for
        ubiquitous application, though hierarchy specific traits should go in teh respsective sub-wordblock
    """

    _subclass = str     # Unique to Class of Wordblock: the class of objects that are sub objects of this class
    _seperator = ' '    # Unique to Class of WordBlock: the character that usually separates the subclass of this class
    """ The _seperator is used to join the _subclass units together when reproducing the text output."""
    #TODO: Move seprator to dynamic seettings fro default wordblock.

    def __init__(self, item=None, **kwargs):
        self._settings = kwargs
        self._settings["cleaner"] = kwargs["cleaner"] if "cleaner" in kwargs.keys() else None
        self.__from(item)
        self._scores = {}

    # TODO: Finish off the scores section of the word block

    class scores():
        """
        Nested Class to handle text scoring operations.

        """
        _scores = {}

        def __init__(self, item=None, **kwargs):
            """
            Initialise the score sub-object.

            Does nothing
            """
            pass

        def add(self, group=None, topic=None, value=0):
            """
            Add a Score to the table of scores

            Parameters
            ----------
            group : str or None, default None
                The name of the group of scores, usually the name/id of a topic scoring model used.
            topic : str or None, default None
                The name of the specif topic or statistic that this score represent.

            Notes
            -----
            group is treated as a row ID and topic as a column ID
            If scoring GROUP  is not specified, score will be added to the generic group '-'.
            If the TOPIC name is not specified, the name will be numbered with th next available numeric slot.
            """

            group = '-' if group is None else group
            if group not in self._scores.keys():
                self._scores[group] = {}

            name = str(len(self._scores[group])) if topic is None else topic
            self._scores[group][name] = value
        # .add(self, group=None, topic=None, value=0) # Add a Score to the score table

        """ Scores Structure Queries Formats
            
            categories(self) :  Returns a list of all the categories in the scores for this object
            cats(self):         Returns a list of all the categories in the scores for this object
            topics(self):       Returns a dictionary of lists, one list for each topic in each category
            topic_list(self):   Returns a list of all unique topic names, across all categories
        
        """

        def categories(self):
            """
                Returns a list of all the categories in the scores for this object

            """
            return list(self._scores.keys())

        def cats(self):
            """
                Returns a list of all the categories in the scores for this object

            """
            return self.categories()

        def topics(self):
            """
                Returns a dictionary of lists, one list for each topic in each category

            """
            out = {}
            for each in self._scores.keys():
                out[each] = list(self._scores[each].keys())

            return out

        def topic_list(self):
            """
                Returns a list of all unique topic names, across all categories

            """

            # Returns a dictionary of lists, one list for each topic in each category
            return list(set(([topic for cat in self._scores.keys() for topic in self._scores[cat].keys()])))

        """ Output Score Formats
        
            N.B. This is only the score for this block
        
        """

        def score(self, group=None, name=None):
            """
                Get score or group (type) of scores by Group name and Topic name

                Note that if no group is provided, looks for name in default ('-') group and if no name is provided, it
                returns the entire group.
                Returns the whole lof the default group if neither group or name are provided.
                Returns a dictionary of dictionaries.
            """

            group = '-' if group is None else group
            if group in self._scores.keys():
                if name is None:
                    return self._scores[group]
                elif name in self._scores[group].keys():
                    return self._scores[group][name]
                else:
                    warnings.warn('No Score by name %s.%s' % (group, name))
                    return None
            else:
                warnings.warn('No Score by group %s' % (group))
                return None

        def scores(self, search=None):
            """
                Return any score that has the search text in its name, category or topic.

                Returns a dictionary of dictionaries
            """

            if search is not None:
                out_scores = {}
                for group in self._scores.keys():
                    if search in group:
                        out_scores[group] = self._scores[group].copy()
                    else:
                        sub_set = {}
                        for name in self._scores[group].keys():
                            if search in name:
                                sub_set[group] = self._scores[group][name]
                        out_scores[group] = sub_set
            else:
                out_scores = self._scores

            return out_scores

        def filter(self, search=None):
            return self.scores(search=search)

        def as_table(self, search=None):
            pass #TODO: add function for output as TEXT

        def as_dict(self, search=None, flat=False):
            output = {}
            for group in self._scores:
                for topic in self._scores[group]:
                    output[group + topic] = self._scores[group][topic]

            return output

        def as_text(self, search=None, seperator=','):
            flat = self.as_dict()
            pass # TODO: add function for output as TEXT

        def as_row(self, search=None):
            pass # TODO: add function for output as PANDAS ROW

        def as_json(self, filter=None):
            pass # TODO: add function for output as JSON ROW

        def copy_from(self):
            pass # TODO: add function for COPY SCORES FROM ANOTHER WORDBLOCK

        def copy_to(self):
            pass # TODO: add function for COPY SCORES FROM ANOTHER WORDBLOCK

        def score_table(self, filter=None, level=None, tag=None):
            if level is None:
                loc_table = pd.DataFrame.from_dict(self._scores)

                if filter is None:
                    return loc_table
                else:
                    valid_rows = [row_name for row_name in loc_table.index() if filter in row_name]
                    return loc_table.loc[valid_rows]
            elif level == self.__class__:
                loc_table = pd.DataFrame()
                for each in self.set:
                    if tag is None:
                        loc_tag = str(each)
                    else:
                        loc_tag = tag + str(each)
                    loc_table = loc_table.join(self[each].score_flat_as_table(filter=filter, tag=loc_tag), how='outer')
                return loc_table
            else:
                loc_table = pd.DataFrame()
                for each in self.set:
                    if tag is None:
                        loc_tag = str(each)
                    else:
                        loc_tag = tag + str(each)
                    loc_table = loc_table.join(self[each].score_table(filter=filter, level=level, tag=loc_tag),
                                               how='outer')
                return loc_table


        # TODO: finsih off here.
        # .level_as_table(self, level=None, search=None): # Return all the scores at the specified level.
        # .all_as_hydict(self): # Return all the scores from all the levels as a hydict
        # .all_as_json(self, filename=None): # Return all the scores from all the levels as a json string
        ######################################################################
        # Hierarchy Score Outputs
        # All the scores of ALL sub-items of the current item, no matter the level
        ######################################################################

        def apply(self, score_function, category=None, name=None, deep=True):
            # create score from function for this level
            # Expecting a Dictionary of values
            # Score Function: the function that evaluates the words in each level of hierarchy. Accepts a list of words
            # and can return either a list (each entry assumed to be a TOPIC, and are labeled numerically) or dict, with
            # each dictioanry label used to label scores internally.
            # category: is name of a model - if not provied rewrites to the default '-' (Anon) group
            # name: name is a topic prefix, for which each value in result will be added in order or with the topci names
            # from model i.e. the name is a prefix for the topic names from the output of score function
            # deep: if true, apply to all the layers below the top layer.

            # Apply the scoring function to object words as list.
            results = score_function(self.parent.as_list())

            # Setup labels (Catagory and Topic in score table)
            name = '' if name is None else name  # leave name as empty if Name is None (see a. below)
            name = '' if name == '' else name  # Whitespace cleaning (invisible chraters)

            # if output of function is a list, convert to numerically labeled topics.
            if isinstance(results, list):
                results = {i: r for i, r in enumerate(results)}

            # Add each of the result values into the .score
            if isinstance(results, dict):
                for i in results:
                    self.add(category=category, topic=(name + str(i)), value=results[i])  # Set as full subgroup
            else:
                warnings.warn("Score function has unrecognised output format")

            # If scoring is for all level (i.e. paragraph, sentences), apply to parents sub_sets.
            if deep:  # todo: and not isinstance(self, Sentence) for .scores.apply
                for each in self.parent:
                    each.scores.apply(score_function=lambda x: score_function(x), category=category, name=name,
                                      deep=deep)

        def copy(self):
            return self._scores.copy()

        def copy_from(self, source=None):
            # Copy the entire hierarchy of scores from the source WordBlock
            # Assumes source is a reduced (i.e. stopwords removed, etc) version of this object
            # Assumes that general structure is retained. Empty blocks are ignored but present

            # Check if the current blocks are of the same type
            if not isinstance(source, self.__class__):
                warnings.warn('Mismatched block type: %S vs %S ' % (str(self.__class__), str(source.__class__)))
            else:
                # if self.match(source) < 0.3: TODO Decide upon this match warning.
                #    warnings.warn('Match is Low: may be miss aligned at text: %s' % (' '.join(source.as_string())))
                self._scores = source.scores.copy()

                # Check if has any entries, and then check if te first sub_set is a Wordblock (i.e. not a string/word)
                if len(self.parent) > 0:
                    if isinstance(self.parent.index(0), WordBlock):
                        for id in self.parent:  # For each Subblock in THIS object
                            if id in source.keys():  # IF the subblock id is present in source objects TODO make usre that WORDblock has a keys function id in source._set.keys()
                                self.parent[id].scores.copy_from(source[id])  # copy all the scores for the sub blockcs

    ######################################################################
    # Micalanious Functions
    # All the scores of ALL sub-items of the current item, no matter the level
    ######################################################################

    def trim(self):
        # Default trim function for wordblocks (pass through)
        pass

    def _setting(self, key, value):
        if key in self._settings.keys():
            self._settings[key] = value
            for item in self:
                item._setting(key=key, value=value)

    def entries(self):
        # Experimental Iterator for returning tuples rather than single values.
        for item in self._set:
            yield item, self._set[item]


    @staticmethod
    def hydict_to_json(hydict=None):
        json_str = "{"
        for each in hydict:
            json_str += "'" + each + "':"
            if isinstance(hydict[each], str):
                json_str += "'" + hydict[each] + "'"
            elif isinstance(hydict[each], np.number):
                json_str += str(hydict[each])
            elif isinstance(hydict[each], dict):
                json_str += WordBlock.scores.hydict_to_json(hydict[each])
            elif isinstance(hydict[each], list):
                json_str += '['
                for item in hydict[each]:
                    json_str += ("'" + item + "'" if isinstance(item, str) else str(item)) + ','
                json_str = json_str[0:-1] + ']'
            else:
                print('unknown')
            json_str += ","
        if json_str == '{':
            json_str = '{}'
        else:
            json_str = json_str[0:-1] + "}"
        return json_str


""" Specific Word Block Classes
    
    There are 4 current levels of word block.
        - Sentence
        - Paragraph 
        - Document
        - Corpus
        
    There can be others/ extensions, such as multipal corpuses or tweet/social medias units. The processes are as 
    generic as possible in the WordBlock Class. It may be prudent to put these sub blocks into thier own package to 
    behave like future extensions. 
"""


class Sentence(WordBlock):
    """
        A Wordblock of words (str) sub units.

        The separator is a space (' ') for sentences.


    """

    _subclass = str

    def __init__(self, item=None, **kwargs):
        """
            Initialise the Sentence object

            Set the splitter to be NONE (as ' ' conflicts with the code for deconstructing the sentences)
            TODO: check the above is true.
            Set the sperator to be ' ' (Space)
            Pass to the WordBlock initalisation

        :param item: is a block of text to be deconstructed at the appropriate level.
        :param kwargs: is additional arguments that are passed through to WordBlock.
        """

        self._settings["splits"] = None
        self._settings["seperator"] = ' '
        super(Sentence, self).__init__(item=item, **kwargs)

    def as_string(self, joins=None, level=None):
        """
            returns the text `as a string.
        :param joins:
        :param level:
        :return:
        """
        # TODO: move sentence as_string in to the WORDBLOCK
        if joins is None:
            loc_join = self._seperator
        else:
            loc_join = joins

        return loc_join.join(self)


class Paragraph(WordBlock):
    seperator = '. '
    _subclass = Sentence

    def __init__(self, item=None, **kwargs):
        self._settings["splits"] = '[.!?]'  # '[.!?]()' TODO deal wit5h brackets and refrences
        kwargs["min_sent_len"] = kwargs["min_sent_len"] if "min_sent_len" in kwargs.keys() else 0
        super(Paragraph, self).__init__(item=item, **kwargs)

    def trim(self):
        """
            Special version of the trim function, which removes subclass groups that are 'invalid'.

            For documents, if the length of a sentence (in words) is too short (default is min 0 words), the sentence is
            reduced to an empty block.

        :return:
        """
        self.filter(lambda x: len(x) > self._settings['min_sent_len'])


class Document(WordBlock):
    """
        Define a class fro storing a whoel

        For documents, if the length of a paragraph (in words) is too short (default is min 20 words), the pargraph
        is reduced to an empty block.

    :return:
    """

    _subclass = Paragraph

    # N.B. That 20 is the number of words in a paragraph, not the number of sentences. TODO: Fix this commment

    def __init__(self, item=None, **kwargs):
        """
            Special version of the trim function, which removes subclass groups that are 'invalid'.

            For documents, if the length of a paragraph (in words) is too short (default is min 20 words), the pargraph
            is reduced to an empty block.

        :return:
        """
        kwargs["splits"] = '\n'
        kwargs["seperator"] = '\n'
        kwargs["min_para_len"] = kwargs['min_para_len'] if 'min_para_len' in kwargs.keys() else 20
        super(Document, self).__init__(item=item, **kwargs)

    def trim(self):
        """
            Special version of the trim function, which removes subclass groups that are 'invalid'.

            For documents, if the length of a paragraph (in words) is too short (default is min 20 words), the pargraph
            is reduced to an empty block.

        :return:
        """
        self.filter(lambda x: x.count() > self._settings['min_para_len'])


class Collection(WordBlock):
    _subclass = Document

    def __init__(self, item=None, **kwargs):
        super(Collection, self).__init__(item=item, **kwargs)

    def _split_string(self, string):
        return [string]

    def as_lists(self):
        return self.as_list(level=Document)