"""
Authors: Mariusz Krzyzopolski s21544 Tomasz Baj s20499
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


def main():
    temperature = ctrl.Antecedent(np.arange(-40, 40, 1), 'temperature')  # Celsius
    humidity = ctrl.Antecedent(np.arange(0, 85, 1), 'humidity')  # Absolute humidity in g/m3
    length_of_trip = ctrl.Antecedent(np.arange(0, 24, 1), 'length_of_trip')  # hours

    how_warm_cloth = ctrl.Consequent(np.arange(0, 5, 1), 'how_warm_cloth')
    """
    1. undershirt and shorts
    2. Shirt and and Long trousers
    3. transitional jacket and Long trousers
    4. winter Jacket and warmer pants
    5. polar jacket, thermal clothing, polar trousers
    """

    temperature.automf(5)  # poor, mediocre, average, decent, good
    humidity.automf(5)
    length_of_trip.automf(3)  # poor,average, good

    how_warm_cloth.automf(5)

    rule1 = ctrl.Rule(how_warm_cloth['good'] | temperature["poor"], length_of_trip["average"])
    rule2 = ctrl.Rule(how_warm_cloth['poor'] | temperature["good"], length_of_trip["average"])
    rule3 = ctrl.Rule(how_warm_cloth['average'] | humidity["good"], length_of_trip["good"])

    # debugging loops
    rule1.view()
    plt.show()

    clothing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

    cloth = ctrl.ControlSystemSimulation(clothing_ctrl)
    cloth.input["temperature"] = 15.0
    cloth.input["humidity"] = 30.4
    cloth.input["length_of_trip"] = 3

    cloth.compute()

    print(cloth.output["how_warm_cloth"])
    how_warm_cloth.view(sim=cloth)

    plt.show()


if __name__ == '__main__':
    main()
