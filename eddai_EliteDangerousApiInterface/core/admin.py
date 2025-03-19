from django.contrib import admin
from django.forms import ModelForm

class BaseOwnerModelsTabularInline(admin.TabularInline):
    """
    A custom TabularInline class for Django admin that automatically sets 
    `created_by` and `updated_by` fields based on the current request user.

    This class includes a custom ModelForm and FormSet to pass the request 
    object to the form, enabling the automatic assignment of user-related 
    fields during save operations.

    Inner Classes:
        - BaseOwnerModelsTabularInlineModelForm: A custom ModelForm that 
          overrides the `save` method to set `created_by` and `updated_by` 
          fields if they are not already set.
        - CustomFormSet: A custom FormSet that injects the request object 
          into the form's keyword arguments.

    Methods:
        - get_formset(request, obj=None, **kwargs): Returns a custom formset 
          that includes the request object in the form's initialization 
          arguments.

    Usage:
        Subclass this TabularInline in your admin classes to enable automatic 
        handling of `created_by` and `updated_by` fields for related models.
    """

    class BaseOwnerModelsTabularInlineModelForm(ModelForm):
        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop("request", None)
            super().__init__(*args, **kwargs)

        def save(self, commit=True):
            if not self.instance.pk and not self.instance.created_by_id:
                self.instance.created_by = self.request.user
            self.instance.updated_by = self.request.user
            return super().save(commit)

    form = BaseOwnerModelsTabularInlineModelForm

    def get_formset(self, request, obj=None, **kwargs):
        BaseFormSet = kwargs.pop("formset", self.formset)

        class CustomFormSet(BaseFormSet):
            def get_form_kwargs(self, index):
                kwargs = super().get_form_kwargs(index)
                kwargs["request"] = request
                return kwargs

        kwargs["formset"] = CustomFormSet
        return super().get_formset(request, obj, **kwargs)