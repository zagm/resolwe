"""Resolwe custom serializer fields."""
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from rest_framework import exceptions, relations

from resolwe.permissions.shortcuts import get_objects_for_user
from resolwe.permissions.utils import get_full_perm


class DictRelatedField(relations.RelatedField):
    """
    Field representing the target of the relationship by using dict.

    A read-write field that represents the target of the relationship by
    a dictionary, where objects are uniquely defined by ``id`` or
    ``slug`` keys in the dictionary. If ``id`` is provided the uniquness
    of object is arbitrary. If ``id`` is not in the dict, object is
    determined by slug. Since multiple objects can have same slug, we
    filter objects by slug, by permissions and return object with
    highest version.
    """

    default_error_messages = {
        'slug_not_allowed': ('Use id (instead of slug) for update requests.'),
        'null': ('At least one of id, slug must be present in field {name}.'),
        'does_not_exist': ('Invalid {model_name} value: {value} - object does not exist.'),
        'permission_denied': ("You do not have {permission} permission for {model_name}: {value}."),
    }

    def __init__(self, serializer, write_permission='view', **kwargs):
        """Initialize attributes."""
        self.serializer = serializer
        self.write_permission = write_permission
        super().__init__(**kwargs)

    @property
    def model_name(self):
        """Get name of queryset model."""
        return self.get_queryset().model._meta.model_name  # pylint: disable=protected-access

    def to_internal_value(self, data):
        """Convert to internal value."""
        # Allow None values only in case field is not required.
        if 'id' in data and data['id'] is None and not self.required:
            return
        elif data.get('id', None) is not None:
            kwargs = {'id': data['id']}
        elif data.get('slug', None) is not None:
            if self.root.instance:
                # ``self.root.instance != None`` means that an instance is
                # already present, so this is not "create" request.
                self.fail('slug_not_allowed')
            kwargs = {'slug': data['slug']}
        else:
            self.fail('null', name=self.field_name)

        user = getattr(self.context.get('request'), 'user')
        queryset = self.get_queryset()
        permission = get_full_perm(self.write_permission, queryset.model)
        try:
            return get_objects_for_user(user, permission, queryset.filter(**kwargs)).latest('version')
        except ObjectDoesNotExist:
            # Differentiate between "user has no permission" and "object does not exist"
            view_permission = get_full_perm('view', queryset.model)
            if permission != view_permission:
                try:
                    get_objects_for_user(user, view_permission, queryset.filter(**kwargs)).latest('version')
                    raise exceptions.PermissionDenied("You do not have {} permission for {}: {}.".format(
                        self.write_permission, self.model_name, data))
                except ObjectDoesNotExist:
                    pass

            self.fail('does_not_exist', value=smart_text(data), model_name=self.model_name)

    def to_representation(self, obj):
        """Convert to representation."""
        serializer = self.serializer(obj, required=self.required, context=self.context)

        # Manually bind this serializer to field.parent as field projection
        # relies on parent/child relations between serializers.
        serializer.bind(self.field_name, self.parent)

        return serializer.data
