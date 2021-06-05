"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object,
    such as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown),
     and whether it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments
         supplied to the constructor.
        """
        self.designation = info.get('pdes', None)
        name = info.get('name', None)
        diameter = info.get('diameter', 'nan')

        if name == "":
            name = None
        if diameter == "":
            diameter = 'nan'

        self.name = name
        self.diameter = float(diameter)
        self.hazardous = (info.get('pha', False) == 'Y')

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        fullname = f"{self.designation} ({self.name})" \
            if self.name is not None else f"{self.designation}"
        return fullname

    def __str__(self):
        """Return `str(self)`."""
        pha = "potentially hazardous asteroid" if self.hazardous\
            else "safe asteroid"
        diameter = f"an undefined diameter" if self.diameter == float('nan') \
            else f"a diameter of {self.diameter:.3f} km"
        return f"NEO {self.fullname} has {diameter} and marked as a {pha}."

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r},"
                f" name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's
    close approach to Earth, such as the date and time (in UTC) of closest
     approach, the nominal approach distance in astronomical units,
      and the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments
         supplied to the constructor.
        """
        self._designation = info.get('des')
        self.time = cd_to_datetime(info.get('cd'))
        self.distance = float(info.get('dist', 'nan'))
        self.velocity = float(info.get('v_rel', 'nan'))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `self`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation,
        the default representation includes seconds - significant figures
         that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        str_representation = f"On {self.time_str}, " \
                             f"{self.neo.fullname} " \
                             f"approaches Earth at a distance of " \
                             f"{self.distance:.2f} au and a velocity of" \
                             f" {self.velocity:.2f} km/s."\
            if self.neo is not None else f"empty CloseApproach object"
        return str_representation

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r},"
                f" distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def to_csv(self):
        """Prepare the date to be dumped into a csv file.

        Returns:
            A collection of date that represent the object formatted
             for csv files
        """
        return {'datetime_utc': self.time_str,
                'distance_au': self.distance,
                'velocity_km_s': self.velocity,
                'designation': self.neo.designation,
                'name': self.neo.name, 'diameter_km': self.neo.diameter,
                'potentially_hazardous': self.neo.hazardous}

    def to_json(self):
        """Prepare the date to be dumped into a json file.

        Returns:
            A collection of date that represent the object formatted
            for json files
        """
        return {'datetime_utc': self.time_str, 'distance_au': self.distance,
                'velocity_km_s': self.velocity,
                'neo': {'designation': self.neo.designation,
                        'name': self.neo.name,
                        'diameter_km': self.neo.diameter,
                        'potentially_hazardous': self.neo.hazardous}}
