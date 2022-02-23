from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTE_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Этот метод не реализованн в Training')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED_MULTIPLE: int = 18
    MEAN_SPEED_SUBTRAHEND: int = 20

    def get_spent_calories(self) -> float:
        calories = ((self.MEAN_SPEED_MULTIPLE
                     * self.get_mean_speed()
                     - self.MEAN_SPEED_SUBTRAHEND
                     ) * self.weight / self.M_IN_KM
                    * self.duration * self.MINUTE_IN_HOUR
                    )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLE: float = 0.035
    WEIGHT_HIEGHT_MULTIPLE: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:

        calories = ((self.WEIGHT_MULTIPLE * self.weight
                    + (self.get_mean_speed()**2 // self.height
                       ) * self.WEIGHT_HIEGHT_MULTIPLE * self.weight
                     )
                    * self.duration * self.MINUTE_IN_HOUR
                    )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    MEAN_SPEED_SWIM_MULTIPLE: float = 1.1
    WEIGHT_SWIM_MULTIPLE: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        distance = (self.action * self.LEN_STEP / self.M_IN_KM)

        return distance

    def get_mean_speed(self) -> float:
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration
                 )
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.MEAN_SPEED_SWIM_MULTIPLE
                     ) * self.WEIGHT_SWIM_MULTIPLE * self.weight
                    )
        return calories


def read_package(workout_type: str, data: List[str]) -> Training:
    """Прочитать данные полученные от датчиков."""

    types_of_training: Dict[str, Training] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking}
    if workout_type not in types_of_training:
        raise ValueError("Отсутствует данный вид тренировок")
    return types_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
