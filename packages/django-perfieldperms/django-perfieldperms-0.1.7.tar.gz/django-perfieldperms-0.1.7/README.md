Implements permissions for model fields in Django

## Requirements
* Python 3.4+
* Django 1.11+ 

## Installation
`pip install django-perfieldperms`

Add perfieldperms to INSTALLED_APPS and AUTHENTICATION_BACKENDS:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'perfieldperms.apps.PerfieldpermsConfig',
    ]

AUTHENTICATION_BACKENDS = [
    'perfieldperms.backends.PFPBackend',
    ]
```

Run `manage.py migrate`

## Configuration
perfieldperms is configurable via ``settings.py`` or via internal models.

Once configured you will need to run `./manage.py pfp-makeperms` to create
field permissions.

### settings.py
PFP_MODELS - an iterable of two tuples `[(app_label, model_name)]` of models you
want perfieldpermissions (pfps) created for.

PFP_IGNORE_PERMS - a dict of dicts of iterables of permissions you want
ignored when creating pfps. Structured:
```python
{app_label:
    {model name: [<perm codename>, <perm codename>,..]}
    }
```

PFP_IGNORE_DELETE - By default perfieldperms doesn't create field level delete
permissions as this doesn't necessarily make sense. Set to False if you want to
create delete pfps.

PFP_IGNORE_VIEW - By default perfieldperms doesn't create field level view 
permissions as this doesn't necessarily make sense. Set to False if you want to
create view pfps.

### Internal models
PFPContentType - Django ContentTypes you want to create pfps for. This setting is
merged with PFP_MODELS from ``settings.py``.

## Management commands
pfp-makeperms - Create field permissions for configured models.

## Forms
`perfieldperms.forms.PFPModelForm` extends `django.forms.ModelForm` to apply
field permissions to a ModelForm. Fields can be disabled or removed entirely
based on class attributes/parameters, or by passing in a user to check
permissions against at form creation.

## Use
After configuring which models you want to creats pfps for run the management
command `./manage.py pfp-makeperms`.

PerFieldPermission subclasses Permission so pfps can be accessed, allocated and
tested as normal Permission objects. PerFieldPermissions are linked to a parent
model permission to create the appropriate hierarchy. Depending on needs you
may not need to access the actual PerFieldPermission objects.

Perfieldperms tries to take a Principle of Least Astonishment approach to
testing permissions, while attempting to support reasonably complicated
permission structures:
* If a user has a model level permission but no field permissions, they
  are deemed to have all equivalent field permissions (all field permissions
  linked to that model permission).
* Model permissions remain additive as in out of the box Django.
* Field permissions allocated to groups are additive, so field permissions for
  all a user's groups are merged.
* Field permissions allocated to a user override those allocated to groups they
  are a member of. The effect is to explicitly set the fields the user has
  access to. This allows for the creation of limited exceptions within groups.
* Possession of a field permission implies access to the model, so testing
  access to a model via e.g. ModelAdmin `had_add_permission()` will succeed if
  the user has any applicable field permission.

## Admin interface
Two ModelAdmins `PFPModelAdmin` and `PFPInlineAdmin` are provided that
extend the appropriate ModelAdmin, disabling fields in forms as appropriate.
These can be used as is or as Mixins to extend other ModelAdmin classes.

There is a permissions management view accessible under
*/admin/perfieldperms/perfieldpermission/manage/*. It provides an alternative
interface to allocating permissions based on a set of filters for
permissions/roles (where a role is a user or group,) and generates a table
based form listing permissions against users. It is terrible and needs
replacing :)

## Tests
Use `runtests.py` to run tests. Test sub-modules and individual tests can be
targetted by supplying the appropriate python module address as an argument to
the script.
