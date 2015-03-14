from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

class djChoice(object):

    def __init__(self, label_name, presentation_name=None, db_name=None):
        #TODO: make use of @property

        # identifier_map = label_name -> db_name
        # display map = db_name -> presentation_name
        # db_values (set of db_names)

        self.label_name = label_name # Python identifier names

        #TODO: format "hello_world" -> "Hello World"
        self.presentation_name = presentation_name or label_name
        self.db_name = db_name or label_name

    def __str__(self):
        return "%s" % self.label_name

    def __unicode(self):
        return u"%s" % self.label_name


class djChoices(object):

    def __init__(self, djChoice_list):

        self._choices = []

        # dictionary mapping db representation to human-readable
        self._display_map = {}

        # dictionary mapping Python identifier to db representation
        self._identifier_map = {}

        # dictionary mapping Python identifier to human-readable
        self._label_map = {}

        # set of db representations
        self._db_values = set()

        for c in djChoice_list:
            if isinstance(c, djChoice):
                self._choices.append(c)
                self._display_map[c.db_name] = c.presentation_name
                self._identifier_map[c.label_name] = c.db_name
                self._label_map[c.label_name] = c.presentation_name
                self._db_values.add(c.db_name)
            else:
                raise ValueError("Must take a list of djChoice objects")

    def __len__(self):
        return len(self._choices)

    def __iter__(self):
        return iter(self._db_values)
        #return iter(_choices)

    def __getattr__(self, attname):
        try:
            # Would rather have self._label_map[attname] if that wouldn't break
            # django
            return self._identifier_map[attname]
        except KeyError:
            raise AttributeError(attname)

    def __getitem__(self, key):
        # Would rather have self._label_map[key]
        return self._display_map[key]

    def __add__(self, other):
        if isinstance(other, self._class__):
            #TODO: check for dupes?
            return djChoices(self._choices + other._choices)
        else:
            raise AttributeError(other)

    def __radd__(self, other):
        # radd is never called for matching types, so we don't check here
        return djChoices(other._choices + self._choices)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._choices == other._choices

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(("%s" % repr(i) for i in self._choices)
                          ))

    def __contains__(self, item):
        return item in self._db_values

    def __deepcopy__(self, memo):
        #TODO: what is this used for?
        return self.__class__(*copy.deepcopy(self._choices, memo))

