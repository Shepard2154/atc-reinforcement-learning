import math

class Airplane:
    def __init__(self, sim_parameters, x, y, h, phi, v, h_min=0, h_max=38000, v_min=100, v_max=300):
        """
        State of one aircraft simulated in the environment

        :param sim_parameters: Definition of the simulation, timestep and more
        :param x: Position in cartesian world coordinates
        :param y: Position in cartesian world cooridantes
        :param h: Height [feet]
        :param phi: Angle of direction, between 1 and 360 degrees
        :param v: Speed [knots]
        :param v_min: Min. speed [knots]
        :param v_max: Max. speed [knots]
        :param h_min: Min. speed [feet]
        :param h_max: Max. speed [feet]        
        """
        self.sim_parameters = sim_parameters
        self.x = x
        self.y = y
        self.h = h
        self.v = v
        self.phi = phi
        if (v < v_min) or (v > v_max):
            raise ValueError("invalid velocity")
        if (h < h_min) or (h > h_max):
            raise ValueError("invalid altitude")
        self.h_dot = [-1000,0,1000]
        self.v_dot = [-5,0,5]
        self.phi_dot = [-3,0,3]
        self.h_set = None
        self.v_set = None
        self.phi_set = None  
        
    def overMVA(self, MVA):
        if self.h >= MVA:
            return True
        else: return False

    def command(self, h_set=None, v_set=None, phi_set=None):
        self.h_set = h_set
        self.v_set = v_set
        self.phi_set = phi_set
        

    def action_v(self, action_v):
        """
        Updates the aircrafts state to a new target speed.

        The target speed will be bound by [_a_min, _a_max]

        :param action_v: New target speed of the aircraft
        :return: Change has been made to the self speed
        """
        delta_v = action_v - self.v
        # restrict to max acceleration, upper bound
        delta_v = min(delta_v, self._a_max * self.sim_parameters.timestep)

        # restrict to min acceleration, lower bound
        delta_v = max(delta_v, self._a_min * self.sim_parameters.timestep)

        self.v = self.v + delta_v

        return math.abs(delta_v) >= self.sim_parameters.precision

class SimParameters:
    def __init__(self, timestep, precision = 0.0001):
        """
        Defines the simulation parameters

        :param timestep: Timestep size [seconds]
        :param precision: Epsilon for 0 comparisons
        """
        self.timestep = timestep
        self.precision = precision

class Airspace:
    def __init__(self, *area):
        """
        Defines the airspace. Areas are entered as lists of touples that form polygons. MVA is defined by a number (heigt in feet)
        """
        self.areas = []
        for i in area:
            self.areas.append(i)