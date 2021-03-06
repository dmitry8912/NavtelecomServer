#Для основных пакетов
flexdictionary = [
    #I - int; F - float, если composite - true, type не нужен
    {'name':'Сквозной номер записи в энергонезависимой памяти', 'size': 4, 'signed': False, 'type': 'I'  },
    {'name':'Код события', 'size': 2, 'signed': False, 'type': 'I'  },
    {'name':'Время события', 'size': 4, 'signed': False, 'type': 'I'  },
    {'name':'Статус устройства', 'size': 1, 'composite': True },
    {'name':'Статус фнукциональных модулей 1', 'size': 1, 'composite': True  },
    {'name':'Статус фнукциональных модулей 2', 'size': 1, 'composite': True  },
    {'name':'Уровень GSM', 'size': 1, 'composite': True  },
    {'name':'Сосотояние навигационного датчика GPS/GLONASS', 'size': 1, 'composite': True  },
    {'name':'Время последних валидных координат (до произошедшего события)', 'size': 4, 'signed': False, 'type': 'I'  },
    {'name':'Последняя валидная широта', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Последняя валидная долгота', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Последняя валидная высота', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Скорость', 'size': 4, 'signed': False, 'type': 'F' },
    {'name':'Курс', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Текущий пробег', 'size': 4, 'signed': False, 'type': 'F'},
    {'name':'Последний отрезок пути', 'size': 4, 'signed': False, 'type': 'F'},
    {'name':'Общее кол-во секунд на последнем отрезке пути', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Кол-во секунд на последнем отрезке пути, по к-рым вычислялся пробег', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на основном источнике питания', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на резервном источнике питания', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 1 (Ain1)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 2 (Ain2)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 3 (Ain3)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 4 (Ain4)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 5 (Ain5)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 6 (Ain6)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 7 (Ain7)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Напряжение на аналоговом выходе 8 (Ain8)', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Текущие показания дискретных датчиков 1', 'size': 1, 'composite': True  },
    {'name':'Текущие показания дискретных датчиков 2', 'size': 1, 'composite': True  },
    {'name':'Текущее состояние выходов 1', 'size': 1, 'composite': True  },
    {'name':'Текущее состояние выходов 2', 'size': 1, 'composite': True  },
    {'name':'Показания счетчика импульсов 1', 'size': 4, 'signed': False, 'type': 'I' },
    {'name':'Показания счетчика импульсов 2', 'size': 4, 'signed': False, 'type': 'I' },
    {'name':'Частота на аналогово-частотном датчике уровня топлива 1', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Частота на аналогово-частотном датчике уровня топлива 2', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Моточасы, подсчитанные во время срабатывания датчика работы генератора', 'size': 4, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива 1 RS-485', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива 2 RS-485', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива 3 RS-485', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива 4 RS-485', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива 5 RS-485', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива 6 RS-485', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Уровень топлива, измеренный датчиком уровня топлива RS-232', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Температура с цифрового датчика 1 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 2 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 3 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 4 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 5 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 6 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 7 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура с цифрового датчика 8 (в градусах цельсия)', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'CAN Уровень топлива в баке', 'size': 2, 'composite': True  },
    {'name':'CAN полный расход топлива', 'size': 4, 'signed': False, 'type': 'F' },
    {'name':'CAN обороты двигателя', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'CAN температура ОЖ', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'CAN полный пробег ТС', 'size': 4, 'signed': False, 'type': 'F' },
    {'name':'CAN нагрзка на ось 1', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'CAN нагрзка на ось 2', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'CAN нагрзка на ось 3', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'CAN нагрзка на ось 4', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'CAN нагрзка на ось 5', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'CAN положение педали газа', 'size': 1, 'signed': False, 'type': 'I' },
    {'name':'CAN положение педали тормоза', 'size': 1, 'signed': False, 'type': 'I' },
    {'name':'CAN нагрузка на двигатель', 'size': 1, 'signed': False, 'type': 'I' },
    {'name':'CAN Уровень жидкости в дизельном фильтре выхлопных газов', 'size': 2, 'composite': True  },
    {'name':'CAN полное время работы двигатеся', 'size': 4, 'signed': False, 'type': 'I' },
    {'name':'CAN Расстояние до ТО', 'size': 2, 'signed': True, 'type': 'I' },
    {'name':'CAN Скорость ТС', 'size': 1, 'signed': False, 'type': 'I' },
    #FLEX 2.0
    #Информация о навигации
    # {'name':'Количество видимых спутников ГЛОНАСС', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников GPS', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников Galileo', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников Compass', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников Beidou', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников DORIS', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников IRNSS', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'Количество видимых спутников QZSS', 'size': 1, 'signed': False, 'type': 'I' },
    {'name':'Информация о навигации', 'size': 8, 'composite': True },
    # {'name':'HDOP штатного приемника', 'size': 1, 'signed': False, 'type': 'I' },
    # {'name':'PDOP штатного приемника', 'size': 1, 'signed': False, 'type': 'I' },
    {'name':'HDOP\PDOP штатного приемника', 'size': 2, 'composite': True },
    {'name':'Состояние дополнительного высокоточного навигационного приемника', 'size': 1, 'composite': True },
    # {'name':'Широта координаты от высокоточного приёмника', 'size': 8, 'signed': True, 'type': 'I' },
    # {'name':'Долгота координаты от высокоточного приёмника', 'size': 8, 'signed': True, 'type': 'I' },
    {'name':'Широта\Долгота координаты от высокоточного приёмника', 'size': 16, 'composite': True },
    {'name':'Высота от высокоточного приёмника', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Курс от высокоточного приёмника', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Скорость от высокоточного приёмника', 'size': 4, 'signed': False, 'type': 'F' },
    {'name':'Информация LBS', 'size': 37, 'composite': True },
    {'name':'Температура, измеренная датчиком уровня топлива 1 RS-485', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура, измеренная датчиком уровня топлива 2 RS-485', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура, измеренная датчиком уровня топлива 3 RS-485', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура, измеренная датчиком уровня топлива 4 RS-485', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура, измеренная датчиком уровня топлива 5 RS-485', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Температура, измеренная датчиком уровня топлива 6 RS-485', 'size': 1, 'signed': True, 'type': 'I' },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 7 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 8 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 9 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 10 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 11 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 12 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 13 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 14 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 15 RS-485', 'size': 3, 'composite': True },
    {'name':'Уровень топлива, Температура, измеренная датчиком уровня топлива 16 RS-485', 'size': 3, 'composite': True },
    {'name':'Информация о датчиках 1-2 давления в шинах', 'size': 6, 'composite': True },
    {'name':'Информация о датчиках 3-6 давления в шинах', 'size': 12, 'composite': True },
    {'name':'Информация о датчиках 7-14 давления в шинах', 'size': 24, 'composite': True },
    {'name':'Информация о датчиках 15-30 давления в шинах', 'size': 48, 'composite': True },
    #Данные тахографа
    {'name':'Активность водителей и состояние слотов карт', 'size': 1, 'composite': True },
    {'name':'Режим работы тахографа\карта', 'size': 1, 'composite': True },
    {'name':'Флаги состояния от тахографа', 'size': 1, 'composite': True },
    {'name':'Скорость по тахографу', 'size': 1, 'signed': False, 'type': 'I' },
    {'name':'Одометр по тахографу', 'size': 4, 'signed': False, 'type': 'I' },
    {'name':'Время по тахографу', 'size': 4, 'signed': False, 'type': 'I' },
    {'name':'Теущее состояние водителя, принятое от дисплейного модуля', 'size': 1, 'composite': True },
    {'name':'Индекс последнего полученного\прочитанного сообщения на дисплейном модуле', 'size': 4, 'composite': True },
    {'name':'Приращение к времесостони относительно предыдущей записи', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Линейное ускорение по осям X,Y,Z', 'size': 6, 'composite': True },
    {'name':'Модуль вектора ускорения', 'size': 2, 'signed': True, 'type': 'I' },
    {'name':'максимальное значение ускорения за период', 'size': 6, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 1-2', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 3-4', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 5-6', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 7-8', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 9-10', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 11-12', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 13-14', 'size': 2, 'composite': True },
    {'name':'Данные счетчиков пассажиропотока 15-16', 'size': 2, 'composite': True },
    {'name':'Статус автоинформатора', 'size': 1, 'composite': True },
    {'name':'ID последней геозоны', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'ID последней остановки', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'ID последнего маршрута', 'size': 2, 'signed': False, 'type': 'I' },
    {'name':'Статус камеры', 'size': 1, 'composite': True },
]

additionalpackagedict = [
    {'name':'Сквозной номер записи в энергонезависимой памяти', 'size': 4, 'signed': False, 'type': 'I'  },
    {'name':'Код события', 'size': 2, 'signed': False, 'type': 'I'  },
    {'name':'Время события', 'size': 4, 'signed': False, 'type': 'I'},
    {'name':'Состояние навигационного датчика', 'size': 1, 'composite': True},
    {'name':'Время последних валидных координат (до произошедшего события)', 'size': 4, 'signed': False, 'type': 'I'  },
    {'name':'Последняя валидная широта', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Последняя валидная долгота', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Последняя валидная высота', 'size': 4, 'signed': True, 'type': 'I' },
    {'name':'Скорость', 'size': 4, 'signed': False, 'type': 'F' },
    {'name':'Курс', 'size': 2, 'signed': False, 'type': 'I'},
    {'name':'Текущий пробег', 'size': 4, 'signed': False, 'type': 'F'},
]