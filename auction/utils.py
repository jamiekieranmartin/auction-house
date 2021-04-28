from sqlalchemy.inspection import inspect


class JSON(object):
    '''JSON serialiser'''

    def serialise(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialise_list(l):
        return [m.serialise() for m in l]


def humanise(value):
    """
    Finds the difference between the datetime value given and now()
    and returns appropriate humanised string
    """

    from datetime import datetime
    from math import floor

    if isinstance(value, datetime):
        diff = datetime.now() - value
        if diff.days > 6:  # i.e October 14
            return value.strftime("%b %d")
        if diff.days > 1:  # i.e Wednesday
            return value.strftime("%A")
        elif diff.days == 1:  # i.e yesterday
            return 'yesterday'
        elif diff.seconds > 3600:  # i.e 3 hours ago
            return str(floor(diff.seconds / 3600)) + ' hours ago'
        elif diff.seconds > 120:  # i.e 29 minutes ago
            return str(floor(diff.seconds / 60)) + ' minutes ago'
        else:  # i.e a moment ago
            return 'a moment ago'
    else:
        return str(value)
