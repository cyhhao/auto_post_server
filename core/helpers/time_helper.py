# coding=utf-8
import time

import datetime


class TimeHelper:
    @classmethod
    def gen_time_format(cls, year=True, month=True, day=True, date=True, hour=True, minute=True, second=True,
                        time=True):

        date_list = []
        time_list = []
        if date:
            if year:
                date_list.append("%Y")
            if month:
                date_list.append("%m")
            if day:
                date_list.append("%d")
        if time:
            if hour:
                time_list.append("%H")
            if minute:
                time_list.append("%M")
            if second:
                time_list.append("%S")

        date_str = '-'.join(date_list)
        time_str = ':'.join(time_list)
        if not date_str:
            return time_str
        if not time_str:
            return date_str
        return ' '.join([date_str, time_str])

    @classmethod
    def str2stamp(cls, string, **kwargs):
        if string.count(':') == 1:
            string += ':00'
        print string
        timeArray = time.strptime(string, cls.gen_time_format(**kwargs))

        timeStamp = int(time.mktime(timeArray))
        timeStamp *= 1000
        return timeStamp

    @classmethod
    def stamp2str(cls, stamp, **kwargs):
        timeArray = time.localtime(stamp / 1000.0)
        return time.strftime(cls.gen_time_format(**kwargs), timeArray)

    @classmethod
    def datetime2stamp(cls, s):
        return time.mktime(s.timetuple()) * 1000

    @classmethod
    def stamp2datetime(cls, cts):
        if isinstance(cts, str) or isinstance(cts, unicode):
            cts = int(cts)
        return datetime.datetime.fromtimestamp(cts / 1000.0)

    @classmethod
    def gen_stamp_by_time_size(cls, start, end, time_size):
        if time_size == 'month' or time_size == 'year':
            # Todo:没考虑闰年
            delta_cts = datetime.timedelta(days=1).total_seconds() * 1000 * 30
            for it in xrange(start, end, int(delta_cts)):
                yield it
        else:
            if not time_size.endswith('s'):
                time_size += 's'
            delta_dict = {
                time_size: 1
            }
            delta_cts = datetime.timedelta(**delta_dict).total_seconds() * 1000
            for it in xrange(start, end, int(delta_cts)):
                yield it
