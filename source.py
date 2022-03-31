import datetime


class WorkingDay:
    '''
    Класс для дней, которые можно забронировать.
    '''
    def __init__(self, date):
        self.date = date
        self.reserved = []

    def is_free(self, start, end):
        '''
        Проверить, свободно ли время
        :param start: time from
        :param end: time to
        :return True if time is free
        '''
        for time1, time2 in self.reserved:
            if time1 <= start <= time2 or time1 <= end <= time2:
                return False
        return True

    def reserve(self, start, end):
        '''
        Забронировать время определнного дня
        :param start: time from
        :param end: time to
        '''
        if self.is_free(start, end):
            self.reserved.append((start, end))
        else:
            raise Exception


class Auditorium:
    '''
    Класс для Аудиторий в университете
    '''
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.working_days = []
        for i in range(30):
            self.working_days.append(WorkingDay(datetime.date.today() + datetime.timedelta(days=i)))

    def reserve(self, date, start, end):
        '''
        Забронировать дату
        :param date: date
        :param start: time from
        :param end: time to
        '''
        ind = date - datetime.date.today()
        if self.working_days[ind.days].is_free(start, end):
            self.working_days[ind.days].reserve(start, end)
            return "200 OK"
        else:
            return "Ошибка! Вы уже забронировали аудиторию на это время"


class University:
    def __init__(self, name):
        self.name = name
        self.auditoriums_list = []

    def create_auditorium(self, name, size):
        '''
        Создать аудиторию
        :param name: Name of auditorium
        :param size: Capacity of auditorium
        '''
        self.auditoriums_list.append(Auditorium(name, size))


    def recommendation(self, size, date, start, end):
        '''
        Рекоммендованные аудитории
        :param size: Needed capacity of auditorium
        :param date: date for reserving
        :param start: time from
        :param end: time to
        :return: list of recommendations
        '''
        ind = date - datetime.date.today()
        result = []
        for aud in self.auditoriums_list:
            if aud.size > size:
                if aud.working_days[ind.days].is_free(start, end):
                    result.append(aud)
        return result[:]







