from django.contrib import admin
from django.forms import ModelForm

class BaseOwnerModelsInlineModelAdmin:
    """
    A base class for creating inline model admins with ownership tracking.

    This class provides functionality to automatically set the `created_by` 
    and `updated_by` fields of a model instance based on the current user 
    making the request. It also customizes the formset to pass the request 
    object to each form.

    Inner Classes:
        BaseOwnerModelsTabularInlineModelForm (ModelForm):
            A custom form that sets the `created_by` and `updated_by` fields 
            of the model instance during save.

    Methods:
        get_formset(request, obj=None, **kwargs):
            Returns a customized formset class that injects the request object 
            into the form's keyword arguments.
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

class BaseOwnerModelsTabularInline(BaseOwnerModelsInlineModelAdmin, admin.TabularInline):
    pass

class BaseOwnerModelsStackedInline(BaseOwnerModelsInlineModelAdmin, admin.StackedInline):
    pass

class BaseOwnerModelsModelAdmin(admin.ModelAdmin):
    """
    A custom ModelAdmin class that automatically sets the `created_by` and `updated_by` 
    fields for models based on the currently logged-in user.
    Methods:
        get_form(request, obj, change, **kwargs):
            Overrides the default `get_form` method to pre-fill the `created_by` and 
            `updated_by` fields with the current user. If the object is being created, 
            both fields are initialized to the current user. If the object is being 
            updated, only the `updated_by` field is initialized.
        save_model(request, obj, form, change):
            Overrides the default `save_model` method to ensure that the `created_by` 
            field is set to the current user when the object is created, and the 
            `updated_by` field is updated to the current user whenever the object is saved.
    """

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        else:
            form.base_fields['updated_by'].initial = request.user
        return form 
    
    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)