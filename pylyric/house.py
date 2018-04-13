from datetime import datetime, timedelta

from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem


class House:
    """
    Represents a house with a heating system and an environment sensor
    """
    WARMUP_GRADIENT = 0.001637426900584798  # degC per minute
    COOLDOWN_GRADIENT = 0.001825459656038644  # degC per minute

    def __init__(self, heating_system: HeatingSystem=None, environment_sensor: EnvironmentSensor=None):
        self.heating_system = heating_system
        self.environment_sensor = environment_sensor
        self.warm_up_time_mins = None
        self.cool_down_time_mins = None

    def is_time_to_warm_up(self, schedule) -> bool:
        """
        Returns True if it is time to start heating the house
        """
        required_temperature = schedule.active_period_minimum_temperature
        required_time = schedule.period_end
        current_temperature = self.environment_sensor.internal_temperature

        # print(required_temperature, required_time)

        self.warm_up_time_mins = int((required_temperature - current_temperature) / self.WARMUP_GRADIENT)
        warm_up_time = timedelta(minutes=self.warm_up_time_mins)
        warm_up_start_time = required_time - warm_up_time

        # print(warm_up_time, warm_up_start_time)

        return datetime.now() > warm_up_start_time

    def is_time_to_cool_down(self, schedule) -> bool:
        """
        Returns True if it is time to stop heating the house
        """
        required_temperature = schedule.inactive_period_minimum_temperature
        required_time = schedule.period_end
        current_temperature = self.environment_sensor.internal_temperature

        self.cool_down_time_mins = int((current_temperature - required_temperature) / self.COOLDOWN_GRADIENT)
        cool_down_time = timedelta(minutes=self.cool_down_time_mins)
        cool_down_start_time = required_time - cool_down_time

        return datetime.now() > cool_down_start_time
