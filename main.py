import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        """
        Перенос not плохо читается, лучше сделать
        dt.datetime.now().date() if not date 
        else dt.datetime.strptime(date, '%d.%m.%Y').date()

        чтобы было сразу было видно условие
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                """
                неконсистентность, в get_week_stats используется +=
                """
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        """
        Можно ещё добавить в конце else с возвращением ошибки,
        чтобы учитывать неправильную currency
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            """
            cash_remained == 1.00 лишняя операция которая не меняет итоговую сумму
            """
            cash_remained == 1.00
            currency_type = 'руб'
        """
        необязательно использовать elif потому что каждое условие возвращает из функции
        """
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            """
            Здесь используется функция format, вместо f'', как в остальном коде.
            Можно написать f'{cash_remained:.2f} чтобы также выводить только 2 числа после запятой
            """
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        """
        Нужно добавить return в начало, чтобы вернуть значение из Calculator.get_week_stats
        """
        super().get_week_stats()
