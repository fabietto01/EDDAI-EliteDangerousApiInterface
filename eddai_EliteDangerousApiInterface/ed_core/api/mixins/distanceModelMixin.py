from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet

class DistanceModelMixin:
    """
    A mixin class for Django Rest Framework views to handle rendering with two different serializers.
    This is useful for views that need to provide both classic information and calculated information from the database.
    Attributes:
        serializer_class (class): The default serializer class for classic information.
        distance_serializer_class (class): The serializer class for calculated information.
        filter_param_distance (str): The query parameter used to determine which serializer to use.
    Methods:
        get_filter_param_distance():
            Ensures that the `filter_param_distance` attribute is set and returns its value.
        get_serializer_class():
            Determines which serializer class to use based on the presence of the `filter_param_distance` query parameter.
    """
    
    serializer_class = None
    filterset_class:BaseDistanceFilterSet = ImportWarning
    distance_serializer_class = None
    filter_param_distance:str = None

    def get_filter_param_distance(self) -> str:
        """
        Ensures that the `filter_param_distance` attribute is set and returns its value.
        Returns:
            str: The value of the `filter_param_distance` attribute.
        Raises:
            AssertionError: If `filter_param_distance` is not set.
        """
        assert self.filter_param_distance is not None, (
            "'%s' should include a `filter_param_distance` attribute."
            % self.__class__.__name__
        )

        return self.filter_param_distance
    
    def get_serializer_class(self):
        """
        Determines which serializer class to use based on the presence of the `filter_param_distance` query parameter.
        Returns:
            class: The appropriate serializer class (`distance_serializer_class` if the query parameter is present, otherwise `serializer_class`).
        Raises:
            AssertionError: If either `serializer_class` or `distance_serializer_class` is not set.
        """
        assert self.serializer_class is not None, (
            "'%s' should include a `serializer_class` attribute."
            % self.__class__.__name__
        )

        assert self.distance_serializer_class is not None, (
            "'%s' should include a `distance_serializer_class` attribute."
            % self.__class__.__name__
        )

        param = self.get_filter_param_distance()

        if self.request.query_params.get(param):
            return self.distance_serializer_class
        return self.serializer_class
    