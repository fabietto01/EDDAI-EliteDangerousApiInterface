from django.forms import MultiWidget, NumberInput
from django.contrib.gis.geos import Point
from typing import Type

class Point3DWidget(MultiWidget):
    
    def __init__(self, attrs:dict = None ) -> None:
        if not attrs:
            attrs = {"style": "margin:10px"}
        else:
            attrs.update({"style": attrs.get("style", "margin:10px")})
        widgets = {
            "x": NumberInput, "y": NumberInput, "z": NumberInput
        }
        super().__init__(widgets, attrs)
    
    def decompress(self, value: Point) -> Type[float]:
        if value:
            return [value.x, value.y, value.z]
        return [None, None, None]
    
    def value_from_datadict(self, data, files, name) -> Point:
        x, y, z, = map(float, super().value_from_datadict(data, files, name))
        return Point(x, y, z,)