from django.db.models import Func

from django.contrib.gis.geos import Point
from django.db.models import FloatField


class Distanza3D(Func):
    """
    Distanza3D is a custom Django database function that calculates the 3D distance between a given point and a set of expressions.

    Attributes:
        function (str): The name of the SQL function to use for calculating the 3D distance.
        template (str): The SQL template to use for the function.
        output_field (FloatField): The type of field that the function returns.

    Methods:
        __init__(*expressions, point: Point, **extra): Initializes the Distanza3D function with the given expressions and point.

    Args:
        *expressions: The expressions to calculate the distance from.
        point (Point): The reference point to calculate the distance to.
        **extra: Additional keyword arguments to pass to the parent class.
    """
    function = 'ST_3DDistance'
    template = "%(function)s(%(expressions)s, ST_GeomFromText('POINT(%(x)s %(y)s %(z)s)', %(srid)s))"
    output_field = FloatField()

    def __init__(self, *expressions, point:Point, **extra):
        x, y, z, srid = point.x, point.y, point.z, point.srid
        super().__init__(*expressions, x=x, y=y, z=z, srid=srid, **extra)