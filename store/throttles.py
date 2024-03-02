from rest_framework.throttling import BaseThrottle, AnonRateThrottle
from datetime import datetime
from django.core.cache import caches


class TimeRateThrottle(BaseThrottle):

    def __init__(self):
        super().__init__()
        self.__from_hour = 23
        self.__from_minute = 0
        self.__to_hour = 24
        self.__to_minute = 0
        self.__args = None

    def __exchange_and_check(self, current_hour, current_minute):
        from_minutes = self.__from_hour * 60 + self.__from_minute
        to_minutes = self.__to_hour * 60 + self.__to_minute
        current_minutes = current_hour * 60 + current_minute
        self.__args = {
            "from_minutes": from_minutes,
            "to_minutes": to_minutes,
            "current_minutes": current_minutes
        }
        return from_minutes <= current_minutes <= to_minutes

    def __get_wait_minutes(self):
        time = self.__args["from_minutes"] - self.__args["current_minutes"]
        if time < 0:
            time = 24 * 60 - (self.__args["current_minutes"] - self.__args["to_minutes"] + self.__args["from_minutes"])
        return time

    def allow_request(self, request, view):
        current_hour = datetime.now().time().hour
        current_minute = datetime.now().time().minute
        return self.__exchange_and_check(current_hour, current_minute)

    def wait(self):
        return self.__get_wait_minutes() * 60


class AnonUserRateThrottle(AnonRateThrottle):
    cache = caches['custom']

    def __init__(self):
        super().__init__()
        self.__block_times = (5, 15, 60)

    def __add_or_retry_dict(self, addr, hour, minute):
        self.__dict[f'{addr}'] = {
            "counter": 0,
            "limit": 3,
            "minutes": hour * 60 + minute,
            "number_blocks": 0,
            "blocked_minute": 0
        }

    def __check(self, addr, hour, minute):
        minutes = hour * 60 + minute
        index = self.__dict[addr]["number_blocks"] - 1

        """
        If number block of anon user greater len(block_times),
        set __dict[addr] to default
        """

        if index == len(self.__block_times):
            self.__add_or_retry_dict(addr, hour, minute)
            index = self.__dict[addr]["number_blocks"] - 1

        """
        Check anon user has in the blocks
        """

        if index >= 0:
            if minutes - self.__dict[addr]["blocked_minute"] < self.__block_times[index]:
                return False

        """
        Check number of requests lower of limit
        """

        if self.__dict[addr]["counter"] < self.__dict[addr]["limit"] - 1:

            """
            Check current time of the request minus first request's time lower than 15 minutes
            """

            if minutes - self.__dict[addr]["minutes"] < 15:
                self.__dict[addr]["counter"] += 1
            else:
                self.__dict[addr]["counter"] = 0
        else:
            self.__dict[addr]["counter"] = 0
            self.__dict[addr]["number_blocks"] += 1
            self.__dict[addr]["blocked_minute"] = minutes
        return True

    def allow_request(self, request, view):

        if request.user.is_authenticated:
            return True
        self.addr = request.META["REMOTE_ADDR"]

        hour = datetime.now().hour if datetime.now().hour != 0 else 24
        minute = datetime.now().minute

        self.__dict = request.session.get('main')
        if not request.session.get('main'):
            self.__dict = request.session['main'] = {}

        if not self.__dict.get(f'{self.addr}'):
            self.__add_or_retry_dict(self.addr, hour, minute)

        check = self.__check(self.addr, hour, minute)
        request.session.modified = True
        return check

    def wait(self):
        index = self.__dict[self.addr]["number_blocks"] - 1
        time = self.__block_times[index]
        return time * 60
