from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import edc_action_item_admin
from ..forms import ActionTypeForm
from ..models import ActionType
from .modeladmin_mixins import ModelAdminMixin


@admin.register(ActionType, site=edc_action_item_admin)
class ActionTypeAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ActionTypeForm

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'display_name',
                'model',
                'show_on_dashboard',
                'create_by_action',
                'create_by_user',
                'instructions',
            )},
         ),
        audit_fieldset_tuple
    )

    list_display = ('display_name', 'show_on_dashboard',
                    'create_by_action', 'create_by_user')

    list_filter = ('create_by_action', 'create_by_user', 'show_on_dashboard')

    search_fields = ('name', 'display_name', 'model')

    date_hierarchy = None

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        fields = fields + ('name',
                           'display_name',
                           'model',
                           'show_on_dashboard',
                           'create_by_action',
                           'create_by_user',
                           'instructions',
                           )
        return fields
