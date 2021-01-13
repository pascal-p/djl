from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        #
        # Write permissions are only allowed to the author of a post
        return obj.author == request.user

class AuthIsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for authenticated users only, and foir that specific user (unless admin)
        if (request.method in permissions.SAFE_METHODS and obj.id == request.user.id) \
           or request.user.is_superuser:
            return True
        #
        # Write permissions are only allowed to the admin (superuser)
        return request.user.is_superuser


# dir(request)
# ['DATA', 'FILES', 'POST', 'QUERY_PARAMS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_auth', '_authenticate', '_authenticator', '_content_type', '_data', '_default_negotiator', '_files', '_full_data', '_load_data_and_files', '_load_stream', '_not_authenticated', '_parse', '_request', '_stream', '_supports_form_parsing', '_user', 'accepted_media_type', 'accepted_renderer', 'auth', 'authenticators', 'content_type', 'csrf_processing_done', 'data', 'force_plaintext_errors', 'negotiator', 'parser_context', 'parsers', 'query_params', 'stream', 'successful_authenticator', 'user', 'version', 'versioning_scheme']


# dir(user)
# ['DoesNotExist', 'EMAIL_FIELD', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_legacy_get_session_auth_hash', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'auth_token', 'check', 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'emailaddress_set', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'post_set', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'socialaccount_set', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_unique']
