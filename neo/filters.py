"""Provide filters for querying close approaches and limit generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch
an attribute of interest from the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.
"""
import operator
from dataclasses import dataclass
from itertools import islice


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value.
    It essentially functions as a callable predicate
    for whether a `CloseApproach` object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` class method to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a `AttributeFilter` from an binary predicate and a  value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest,
        comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Representation of the filter in human readable format.

        :return: A human readable representation of this filter
        """
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}," \
               f" value={self.value})"


class DateFilter(AttributeFilter):
    """A subclass of AttributeFilter that represents date based filters."""

    @classmethod
    def get(cls, approach):
        """Get the date value of the approach`CloseApproachObject`.

        This function Overrides the super class AttributeFilter get function

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of approach's `CloseApproachObject` date.
        """
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """A subclass of AttributeFilter that represents distance based filters."""

    @classmethod
    def get(cls, approach):
        """Get the distance value of the approach`CloseApproachObject`.

        This function Overrides the super class AttributeFilter get function

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of approach's `CloseApproachObject` distance.
        """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """A subclass of AttributeFilter that represents velocity based filters."""

    @classmethod
    def get(cls, approach):
        """Get the velocity value of the approach`CloseApproachObject`.

        This function Overrides the super class AttributeFilter get function

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of approach's `CloseApproachObject` velocity.
        """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """A subclass of AttributeFilter that represents diameter based filters."""

    @classmethod
    def get(cls, approach):
        """Get the diameter value of the approach`CloseApproachObject`.

        This function Overrides the super class AttributeFilter get function

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of approach's `CloseApproachObject` diameter.
        """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """A subclass of AttributeFilter represents hazardous based filters."""

    @classmethod
    def get(cls, approach):
        """Get the hazardous value of the approach`CloseApproachObject`.

        This function Overrides the super class AttributeFilter get function

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The hazardous of approach's `CloseApproachObject`,
         whether it is hazardous or not.
        """
        return approach.neo.hazardous


@dataclass
class Filter:
    """General filter class that encapsulates all filters.

    Attributes:
    date         : a DateFilter class
    start_date   : a DateFilter class
    end_date     : a DateFilter class
    distance_min : a DistanceFilter class
    distance_max : a DistanceFilter class
    velocity_min : a VelocityFilter class
    velocity_max : a VelocityFilter class
    diameter_min : a DiameterFilter class
    diameter_max : a DiameterFilter class
    hazardous    : a HazardousFilter class
    """
    date         : DateFilter
    start_date   : DateFilter 
    end_date     : DateFilter 
    distance_min : DistanceFilter
    distance_max : DistanceFilter
    velocity_min : VelocityFilter
    velocity_max : VelocityFilter
    diameter_min : DiameterFilter
    diameter_max : DiameterFilter
    hazardous    : HazardousFilter

    def __call__(self, approach):
        """Check if the approach`CloseApproachObject` satisfy all filters.

        :param approach: approach`CloseApproachObject` being tested
        :return result : a True or False value represents
        the result of the check
        """
        result = True
        for _, filter_ in vars(self).items():
            if filter_.value is not None:
                result = (result and filter_(approach))
        return result


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from
    the user's options at the command line. Each one corresponds to a different
    type of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that
    occurred on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of
     `NEODatabase` because the main module directly passes this result
     to that method.
    For now, this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching
     `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching
     `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance
    for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance
    for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity
    for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity
    for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching
     `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching
    `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach`
    is potentially hazardous.
    :return filter: A collection of filters for use with `query`.
    """
    filters = Filter(DateFilter(operator.eq, date),
                     DateFilter(operator.ge, start_date),
                     DateFilter(operator.le, end_date),
                     DistanceFilter(operator.ge, distance_min),
                     DistanceFilter(operator.le, distance_max),
                     VelocityFilter(operator.ge, velocity_min),
                     VelocityFilter(operator.le, velocity_max),
                     DiameterFilter(operator.ge, diameter_min),
                     DiameterFilter(operator.le, diameter_max),
                     HazardousFilter(operator.eq, hazardous))
    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n == 0:
        n = None
    return islice(iterator, n)
