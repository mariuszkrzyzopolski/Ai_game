"""
Authors: Mariusz Krzyzopolski s21544 Tomasz Baj s20499
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


def map_cloth(cloth_value: int) -> str:
    """
    Simple maping values to clothing, to receive meaningful output for human

    :param cloth_value: int from 0 to 6
    :return: description for set of clothes
    """
    if 0 <= cloth_value < 2:
        return "undershirt and shorts"
    elif 2 <= cloth_value < 3:
        return "Shirt and and Long trousers"
    elif 3 <= cloth_value < 4:
        return "Transitional jacket and Long trousers"
    elif 4 <= cloth_value < 5:
        return "Winter Jacket and warmer pants"
    elif cloth_value >= 5:
        return "Polar jacket, thermal clothing, polar trousers"


def main():
    """
        Fuzzy logic 'advice' what set of clothes user should wear, depending on the weather (temperature and humidity)
        and how long the trip will be. Sample sets:
        1. undershirt and shorts
        2. Shirt and Long trousers
        3. transitional jacket and Long trousers
        4. winter Jacket and warmer pants
        5. polar jacket, thermal clothing, polar trousers

        Which is connected to indicators - hot, warm, british, cold and frosty
        Range for temperature is -40 to 40 Celsius
        Range for Humidity is 0 to 100%
        Length of trip can be from 0 to 300, where 0 to 100 is short (short, medium, long)
        """
    temperature = ctrl.Antecedent(np.arange(-40, 41, 1), 'temperature')  # Celsius
    humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')  # Absolute humidity in g/m3
    length_of_trip = ctrl.Antecedent(np.arange(0, 301, 1), 'length_of_trip')  # minutes

    how_warm_cloth = ctrl.Consequent(np.arange(1, 6, 1), 'how_warm_cloth')

    temperature['low'] = fuzz.trapmf(np.arange(-40, 41, 1), [-40, -40, -5, 10])
    temperature['medium'] = fuzz.trapmf(np.arange(-40, 41, 1), [5, 10, 17, 21])
    temperature['high'] = fuzz.trapmf(np.arange(-40, 41, 1), [19, 27, 40, 40])
    temperature.view()

    humidity['low'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 30, 50])
    humidity['medium'] = fuzz.trimf(np.arange(0, 101, 1), [40, 55, 75])
    humidity['high'] = fuzz.trapmf(np.arange(0, 101, 1), [60, 85, 100, 100])
    humidity.view()

    length_of_trip['short'] = fuzz.trapmf(np.arange(0, 301, 1), [0, 0, 10, 25])
    length_of_trip['medium'] = fuzz.trimf(np.arange(0, 301, 1), [15, 45, 75])
    length_of_trip['long'] = fuzz.trapmf(np.arange(0, 301, 1), [60, 240, 300, 300])
    length_of_trip.view()

    how_warm_cloth['hot'] = fuzz.trapmf(how_warm_cloth.universe, [0, 0, 1, 2])
    how_warm_cloth['warm'] = fuzz.trimf(how_warm_cloth.universe, [1, 2, 3])
    how_warm_cloth['british'] = fuzz.trimf(how_warm_cloth.universe, [2, 3, 4])
    how_warm_cloth['cold'] = fuzz.trimf(how_warm_cloth.universe, [3, 4, 5])
    how_warm_cloth['frosty'] = fuzz.trapmf(how_warm_cloth.universe, [4, 5, 6, 6])
    how_warm_cloth.view()

    rule1 = ctrl.Rule(temperature['high'] & humidity['high'], how_warm_cloth['warm'])
    rule2 = ctrl.Rule(temperature['high'] & humidity['low'], how_warm_cloth['hot'])
    rule3 = ctrl.Rule(temperature['medium'], how_warm_cloth['british'])
    rule4 = ctrl.Rule(temperature['low'] & length_of_trip['short'], how_warm_cloth['cold'])
    rule5 = ctrl.Rule(temperature['low'] & length_of_trip['long'], how_warm_cloth['frosty'])
    rule6 = ctrl.Rule(humidity['medium'] & length_of_trip['medium'], how_warm_cloth['british'])
    rule7 = ctrl.Rule(humidity['high'] & length_of_trip['medium'], how_warm_cloth['british'])
    rule8 = ctrl.Rule(humidity['high'] & length_of_trip['long'], how_warm_cloth['british'])
    rule9 = ctrl.Rule(humidity['medium'] & length_of_trip['short'], how_warm_cloth['hot'])

    clothing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    cloth = ctrl.ControlSystemSimulation(clothing_ctrl)

    cloth.input["temperature"] = int(input("Temperature: "))  # = 15.0
    cloth.input["humidity"] = int(input("Humidity: "))  # = 30.4
    cloth.input["length_of_trip"] = int(input("Length_of_trip: "))  # = 60
    cloth.compute()
    print(cloth.output['how_warm_cloth'])
    print(f"You should wear {map_cloth(cloth.output['how_warm_cloth'])}")
    how_warm_cloth.view(sim=cloth)

    cloth.input["temperature"] = -15.0
    cloth.input["humidity"] = 5
    cloth.input["length_of_trip"] = 10
    cloth.compute()
    print(cloth.output["how_warm_cloth"])
    how_warm_cloth.view(sim=cloth)

    cloth.input["temperature"] = -15.0
    cloth.input["humidity"] = 5
    cloth.input["length_of_trip"] = 120
    cloth.compute()
    print(cloth.output["how_warm_cloth"])
    how_warm_cloth.view(sim=cloth)

    cloth.input["temperature"] = 25.0
    cloth.input["humidity"] = 60.4
    cloth.input["length_of_trip"] = 6
    cloth.compute()
    print(cloth.output["how_warm_cloth"])
    how_warm_cloth.view(sim=cloth)

    cloth.input["temperature"] = 25.0
    cloth.input["humidity"] = 60.4
    cloth.input["length_of_trip"] = 120
    cloth.compute()
    print(cloth.output["how_warm_cloth"])
    how_warm_cloth.view(sim=cloth)
    plt.show()


if __name__ == '__main__':
    main()
