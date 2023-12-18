"""
    textblock.py defines the structural elements of set of textual inputs.

    The basic functions all work on the principle of a WORDBLOCK, each of which can be processed in almost identical
    ways, treated as a Structured piece of text or as a BOW as required. it also allows for scores to be applied and
    processed for each block. SENTENCES, PARAGRAPHS, DOCUMENTS and CORPUS are all treated as WORDBLOCKs but with
    minor adjustments in the behaviour of each.
"""

import warnings

# TODO: This diocument is still being moved over from the langStructures.py in LanguageForms project

class WordBlock():
    """ WordBlock

        Basic unit of functionality for all textual structures. Edits to functionality should be added here for
        ubiquitous application, though hierarchy specific traits should go in teh respsective sub-wordblock
    """

    def __init__(self, item=None, **kwargs):
        self.settings = kwargs
        self.settings["min_sent_len"] = kwargs["min_sent_len"] if "min_sent_len" in kwargs.keys() else 0
        self.settings["min_para_len"] = kwargs[
            'min_para_len'] if 'min_para_len' in kwargs.keys() else 20  # N.B. That 20 is the number of words in a paragraph, not the number of sentences.
        self.settings["cleaner"] = kwargs["cleaner"] if "cleaner" in kwargs.keys() else None
        self.__from(item)
        self._scores = {}

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

        ######################################################################
        # Output Score Formats
        ######################################################################

        def score(self, group=None, name=None):

            # Get score or group (type) of scores by Group name and Topic name

            # Note that if no group is provided, looks for name in default ('-') group and if no name is provided, it
            # returns the entire group.
            # Returns the whoel lof the default group if neither group or name are provided.

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
            pass

        def as_dict(self, search=None, flat=False):
            output = {}
            for group in self._scores:
                for topic in self._scores[group]:
                    output[group + topic] = self._scores[group][topic]

            return output

        def as_text(self, search=None, seperator=','):
            flat = self.as_dict()
            pass

        def as_row(self, search=None):
            pass

        def as_json(self, filter=None):
            pass

        def copy_from(self):
            pass

        def copy_to(self):
            pass

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