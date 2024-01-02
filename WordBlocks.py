import warnings


class ModelScores(object):
    """
        ModelScores is a class that is used to store and manipulate the Topic Modeling type scores for a block of words

        Stores are scores by GROUPNAME and TOPIC, such that multiple models each with matching or non-matching topic
        defintions can be included.
        the default GROUPNAME is '-', which is accessed when ever a GROUPNAME is ommitted.


        --- INTERNAL VARIABLES ---
        _SCORES : Hidden variable that stores teh scores as a dictionary of dictionaries. The first Dictionary index is
                        the GROUPNAME, and the second index is the TOPIC NAME.

    """
    # INTERNAL VARIABLES
    _SCORES = {}

    def __init__(self, item=None, **kwargs):
        """
        Initialise the score sub-object.

        Does nothing TODO Check if somthing needs initalising in MODELSCORES Class
        """
        pass

    """
    --------------------------BUILT IN FUNCTIONS -----------------------------------------
    """

    # TODO __setitem__, __getitem__ to be mirrors to the add function


    """
    ------------------------------- ACCESS ENTRY ------------------------------------------
    """

    def add(self, group=None, topic=None, value=0):
        """
        Add a Score to the table of scores

        Parameters
        ----------
        group : str or None, default None
            The name of the group of scores, usually the name/id of a topic scoring model used.
        topic : str or None, default None
            The name of the specif topic or statistic that this score represent.
        value : numeric, default 0
            The score value to assign to the group/topic

        Notes
        -----
        group is treated as a row ID and topic as a column ID
        If scoring GROUP  is not specified, score will be added to the generic group '-'.
        If the TOPIC name is not specified, the name will be numbered with th next available numeric slot.
        """

        # If no group given, use default group.
        group = '-' if group is None else group

        # If group doesn't exist, create it.
        if group not in self._SCORES.keys():
            self._SCORES[group] = {}

        if isinstance(value, dict):
            # If the value is a dictionary, then add the whole group (topic is irrelevant)
            if len(self._SCORES) > 0:
                # If group already exists, give warning.
                warnings.warn("Replacing Entire Group - Data may be lost")
            self._SCORES[group] = value
        else:
            # If there is no topic name, use the number of existing topics in group as NAME
            name = str(len(self._SCORES[group])) if topic is None else topic

            # Set the value of the score
            self._SCORES[group][name] = value

    def get(self, group=None, topic=None):
        """
            Get score or group (type) of scores by Group name and Topic name

        Parameters
        ----------
            group : str or None, default None
                The name of the group of scores, usually the name/id of a topic scoring model used.
            topic : str or None, default None
                The name of the specif topic or statistic that this score represent.

        Notes
        -----
            - if no group is provided, looks for name in default ('-') group
            - if no topic is provided, it returns the entire group.
            - therfore Returns the whole of the default group if neither group or name are provided.
            - Returns a Signe number or a dictioanry of scores.
        """

        # If no group given, use default group.
        group = '-' if group is None else group

        # If group is in scores object
        if group in self._scores.keys():
            if topic is None:
                # If topic is not provided, return whole group
                return self._scores[group]
            elif topic in self._scores[group].keys():
                # if valid topic, return the score
                return self._scores[group][topic]
            else:
                # If topic doesn't exist, retunr nothing & warning
                warnings.warn('No Score by name %s.%s' % (group, topic))
                return None
        else:
            # if group doesn't exist, return nothing.
            warnings.warn('No Score by group %s' % (group))
            return None

    def score(self, group=None, topic=None, value=None):
        """
            Get or set score or group of scores by Group name and Topic name

        Parameters
        ----------
            group : str or None, default None
                The name of the group of scores, usually the name/id of a topic scoring model used.
            topic : str or None, default None
                The name of the specif topic or statistic that this score represent.
            value : numeric or None, default None
                The value to store. If None, return the current value.

        Notes
        -----
            - if no group is provided, looks for name in default ('-') group
            - if no topic is provided, it returns the entire group.
            - therfore Returns the whole of the default group if neither group or name are provided.
            - Returns a Signe number or a dictioanry of scores.
        """
        if value is None:
            return self.get(group=group,topic=topic)
        else:
            self.add(group=group,topic=topic, value=value)