from django.forms import MultiWidget, NumberInput, ValidationError
from django.contrib.gis.geos import Point
from typing import Type

class Point3DWidget(MultiWidget):
    """
    A widget for inputting 3D points.
    Args:
        attrs (dict, optional): Additional attributes for the widget. Defaults to None.
    Methods:
        __init__(self, attrs: dict = None) -> None:
            Initializes the Point3DWidget.
        decompress(self, value: Point) -> Type[float]:
            Decompresses the value of the widget.
        value_from_datadict(self, data, files, name) -> Point:
            Retrieves the value of the widget from the data dictionary.
    """
    
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
        try:
            x, y, z, = map(float, super().value_from_datadict(data, files, name))
        except ValueError as e:
            raise ValidationError(e)
        else:
            return Point(x, y, z)