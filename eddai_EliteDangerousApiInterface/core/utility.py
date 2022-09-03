from datetime import datetime
from typing import Any, Tuple
from django.shortcuts import _get_queryset
from django.core.exceptions import ObjectDoesNotExist

from django.db import models

def equal_list_models(list1:list[models.Model], list2:list[models.Model], fields_exclus:list[str]=['id','pk','updated']) -> bool:
    """
    dato che la funzione __eq__ della classe models.Model ugualia solo per pk,
    ho creato questa funzione per conflontare l'ugualianza tra i fils della istanza
    al interno della lista
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

def in_list_models(instanze:models.Model, list:list[models.Model], fields_exclus:list[str]=['id','pk','updated']) -> bool:
    """
    dato che la funzione __eq__ della classe models.Model ugualia solo per pk,
    ho creato questa funzione per verificare se una istanza è presente in una lista
    """
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

def equal_models(instanze1:models.Model, instanze2:models.Model, fields_exclus:list[str]=['id','pk','updated']) -> bool:
    """
    dato che la funzione __eq__ della classe models.Model ugualia solo per pk,
    ho creato questa funzione per conflontare l'ugualianza tra i fils della istanza
    """
    if not isinstance(instanze1, instanze2.__class__):
        return False
    filds = [f.name for f in instanze1._meta.get_fields() if not f.name in fields_exclus]
    for fild in filds:
        if getattr(instanze1, fild) != getattr(instanze2, fild):
            return False
    return True

def get_values_list_or_default(klass, default=None, expected_exc=(Exception,), *args, **kwargs):
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

def get_or_instance(klass, default:dict={},*args, **kwargs) -> Tuple[Any, bool]:
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

def update_or_create_if_time(klass, time:datetime, defaults:dict, update_function=None, create_function=None, *args, **kwargs) -> Tuple[Any, bool]:
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get_or_create"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to update_or_create_if_time() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    instance, create = queryset.get_or_create(defaults, *args, **kwargs)
    if (not create):
        if instance.updated < time:
            for attr, value in defaults.items():
                setattr(instance, attr, value)
            instance.save()
            if update_function != None:
                update_function(instance)
    else:
        if create_function != None:
            create_function(instance)
    return (instance, create)  