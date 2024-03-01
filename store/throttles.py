from rest_framework.throttling import BaseThrottle
from datetime import datetime


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
