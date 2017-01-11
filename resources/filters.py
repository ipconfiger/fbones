# coding=utf8
import datetime


def format_date(value, format='%Y-%m-%d'):
    if value:
        return '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(value)
    return ""


def pretty_date(value, default="just now"):
    now = datetime.datetime.utcnow()
    diff = now - value

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default
