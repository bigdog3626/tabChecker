from .models import Members, Organization
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget




class MemberResource(resources.ModelResource):
    class Meta:
        model = Members
        skip_unchanged = True
        exclude = ('id',)
        import_id_fields = ('email', 'phone',)
        fields = ('first_name', 'last_name', 'organization', 'email', 'phone')

