from django.contrib.gis.db.models.functions import DistanceResultMixin,OracleToleranceMixin, GeoFunc
from django.db.models import (
    BinaryField,
    BooleanField,
    FloatField,
    Func,
    IntegerField,
    TextField,
    Transform,
    Value,
)
from django.db.models.functions import Cast
from django.contrib.gis.db.models.fields import BaseSpatialField, GeometryField

class Distance3D(DistanceResultMixin, OracleToleranceMixin, GeoFunc):
    geom_param_pos = (0, 1)
    spheroid = None

    def __init__(self, expr1, expr2, spheroid=None, **extra):
        expressions = [expr1, expr2]
        if spheroid is not None:
            self.spheroid = self._handle_param(spheroid, "spheroid", bool)
        super().__init__(*expressions, **extra)

    def as_postgresql(self, compiler, connection, **extra_context):
        clone = self.copy()
        function = None
        expr2 = clone.source_expressions[1]
        geography = self.source_is_geography()
        if expr2.output_field.geography != geography:
            if isinstance(expr2, Value):
                expr2.output_field.geography = geography
            else:
                clone.source_expressions[1] = Cast(
                    expr2,
                    GeometryField(srid=expr2.output_field.srid, geography=geography),
                )

        if not geography and self.geo_field.geodetic(connection):
            # Geometry fields with geodetic (lon/lat) coordinates need special
            # distance functions.
            if self.spheroid:
                # DistanceSpheroid is more accurate and resource intensive than
                # DistanceSphere.
                function = connection.ops.spatial_function_name("DistanceSpheroid")
                # Replace boolean param by the real spheroid of the base field
                clone.source_expressions.append(
                    Value(self.geo_field.spheroid(connection))
                )
            else:
                function = connection.ops.spatial_function_name("DistanceSphere")

        return super(Distance3D, clone).as_sql(
            compiler, connection, function=function, **extra_context
        )

    def as_sqlite(self, compiler, connection, **extra_context):
        if self.geo_field.geodetic(connection):
            # SpatiaLite returns NULL instead of zero on geodetic coordinates
            extra_context[
                "template"
            ] = "COALESCE(%(function)s(%(expressions)s, %(spheroid)s), 0)"
            extra_context["spheroid"] = int(bool(self.spheroid))
        return super().as_sql(compiler, connection, **extra_context)