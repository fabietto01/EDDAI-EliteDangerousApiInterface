from datetime import datetime
from typing import Any, Tuple
from django.shortcuts import _get_queryset

from django.db import models

def equal_list_models(list1:list[models.Model], list2:list[models.Model], fields_exclus:list[str]=['id','pk','updated_at', 'created_at', 'created_by','updated_by']) -> bool:
    """
    Check if two lists of models are equal based on specified fields.

    Args:
        list1 (list[models.Model]): The first list of models.
        list2 (list[models.Model]): The second list of models.
        fields_exclus (list[str], optional): List of fields to exclude from comparison. Defaults to ['id','pk','updated_at', 'created_at', 'created_by','updated_by'].

    Returns:
        bool: True if the lists are equal, False otherwise.
    """
    if len(list1) != len(list2):
        return False
    for index in range(len(list1)):
        if isinstance(list1[index], list2[index].__class__):
            filds = [f.name for f in list1[index]._meta.get_fields() if not f.name in fields_exclus]
            for fild in filds:
                if getattr(list1[index], fild) != getattr(list2[index], fild):
                    return False
        else:
            return False
    return True

def in_list_models(instanze:models.Model, list:list[models.Model], fields_exclus:list[str]=['id','pk','updated_at', 'created_at', 'created_by','updated_by'], fields_include:list[str]=[]) -> bool:
    """
    Check if an instance is present in a list of models.

    Args:
        instanze (models.Model): The instance to check.
        list (list[models.Model]): The list of models to search in.
        fields_exclus (list[str], optional): List of fields to exclude from comparison. Defaults to ['id','pk','updated_at', 'created_at', 'created_by','updated_by'].
        fields_include (list[str], optional): List of fields to include in comparison. Defaults to [].

    Returns:
        bool: True if the instance is found in the list, False otherwise.
    """
    if fields_include:
        filds = [f.name for f in instanze._meta.get_fields() if f.name in fields_include]
    else:
        filds = [f.name for f in instanze._meta.get_fields() if not f.name in fields_exclus]
    for index in range(len(list)):
        if isinstance(instanze, list[index].__class__):
            equal = True
            for fild in filds:
                equal = getattr(instanze, fild) == getattr(list[index], fild) and equal
            if equal:
                return True
        else:
            return False
    return False

def equal_models(instanze1:models.Model, instanze2:models.Model, fields_exclus:list[str]=['id','pk','updated_at', 'created_at', 'created_by','updated_by']) -> bool:
    """
    Check if two instances of models.Model are equal based on their field values.

    Args:
        instanze1 (models.Model): The first instance to compare.
        instanze2 (models.Model): The second instance to compare.
        fields_exclus (list[str], optional): A list of field names to exclude from the comparison. Defaults to ['id','pk','updated_at', 'created_at', 'created_by','updated_by'].

    Returns:
        bool: True if the instances are equal, False otherwise.
    """
    if not isinstance(instanze1, instanze2.__class__):
        return False
    filds = [f.name for f in instanze1._meta.get_fields() if not f.name in fields_exclus]
    for fild in filds:
        if getattr(instanze1, fild) != getattr(instanze2, fild):
            return False
    return True

def get_values_list_or_default(klass, default=None, expected_exc=(Exception,), *args, **kwargs):
    """
    Retrieve a list of values from a Model, Manager, or QuerySet, or return a default value.

    Args:
        klass: The Model, Manager, or QuerySet object to retrieve values from.
        default: The default value to return if the retrieved list is empty.
        expected_exc: The expected exception types to catch.

    Returns:
        A list of values retrieved from the given object, or the default value if the list is empty.

    Raises:
        ValueError: If the first argument is not a Model, Manager, or QuerySet object.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "values_list"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_list_or_default() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    try:
        obj_list = list(queryset.values_list(*args, **kwargs))
        if not obj_list:
            return default
        return obj_list
    except expected_exc:
        return default

def get_or_instance(klass, default: dict = {}, *args, **kwargs) -> Tuple[Any, bool]:
    """
    Get an instance of a model from the given queryset based on the provided arguments,
    or create a new instance if it doesn't exist.

    Args:
        klass: The model, manager, or queryset to retrieve the instance from.
        default: A dictionary of default attribute values to set on the created instance.
        *args: Additional positional arguments to pass to the `get` method of the queryset.
        **kwargs: Additional keyword arguments to pass to the `get` method of the queryset.

    Returns:
        A tuple containing the retrieved or created instance and a boolean indicating
        whether the instance was created or not.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_or_instance() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    create = False
    try:
        instance = queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        create = True
        instance = queryset.model()
        for attr, value in default.items():
            setattr(instance, attr, value)
    finally:
        return (instance, create)

def get_or_none(klass, *args, **kwargs) -> Any:
    """
    Retrieve a single instance of a model from the database, or return None if it doesn't exist.

    Args:
        klass: The model class, manager, or queryset to retrieve the instance from.
        *args: Positional arguments to pass to the `get` method of the queryset.
        **kwargs: Keyword arguments to pass to the `get` method of the queryset.

    Returns:
        An instance of the model if found, or None if it doesn't exist.

    Raises:
        ValueError: If the first argument is not a Model, Manager, or QuerySet.

    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_or_none() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

def create_or_update_if_time(
        klass, time:datetime, 
        defaults:dict,
        defaults_update:dict={},
        defaults_create:dict={},
        update_function=None, create_function=None, 
        *args, **kwargs
) -> Tuple[Any, bool]:
    """
    This function creates or updates an instance of a model, depending on whether the data is more recent.

    Args:
        klass (Any): The class of the model.
        time (datetime): The date and time when the data was retrieved.
        defaults (dict): The default data to create or update the instance.
        defaults_update (dict, optional): The default data to update the instance. Defaults to {}.
        defaults_create (dict, optional): The default data to create the instance. Defaults to {}.
        update_function (Any, optional): The function to call when updating the instance. Defaults to None.
        create_function (Any, optional): The function to call when creating the instance. Defaults to None.
    
    Returns:
        Tuple[Any, bool]: The instance and a flag indicating whether the instance was created.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get_or_create"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to create_or_update_if_time() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    defaults_create.update(defaults)
    instance, create = queryset.get_or_create(defaults_create, *args, **kwargs)
    if (not create):
        if instance.updated_at < time:
            defaults_update.update(defaults)
            for attr, value in defaults_update.items():
                setattr(instance, attr, value)
            instance.save()
            if update_function != None:
                update_function(instance)
    else:
        if create_function != None:
            create_function(instance)
    return (instance, create)