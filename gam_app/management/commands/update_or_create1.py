from django.db import transaction


@transaction.atomic
def update_or_create1(model, **kwargs):
    """
    Looks up an object with the given kwargs, updating one if it exists,
    otherwise creates a new one.

    This implementation differs from Django `update_or_create()` function.

    In contrast to the native implementation, this function supports
    related field lookup (`ForeignKey`, `ManyToManyField`) and uses the
    models constraints (`unique`, `unique_together`) to fetch the object
    from the database.
    """
    # object instance we'll work with
    instance = None

    # holds whether the object has been created or not
    created = False

    # pk field name
    pk = model._meta.pk.name

    # remove fields without value (None or an empty string/list/dict)
    fields = {key: val for key, val in kwargs.items() if val or val == False}

    # resolve pk
    if 'pk' in fields:
        fields[pk] = fields.pop('pk')

    # resolve related objects
    for key, val in fields.items():
        if isinstance(val, dict):
            # update field with the resolved object
            fields[key] = update_or_create(model._meta.get_field(key).rel.to, **val)[0]

    # unique fields
    unique_fields = list(
        set(
            field.name
            for field in model._meta.get_fields()
            if getattr(field, 'unique', False) and field.name != pk
        ).intersection(fields.keys())
    )

    # if available, prepend pk
    if pk in fields:
        unique_fields.insert(0, pk)

    # iterate trough unique fields
    for key in unique_fields:
        try:
            # try to query a single object
            instance = model.objects.get(**{key: fields[key]})
        except model.DoesNotExist:
            pass  # didn't match, continue
        else:
            break  # matched, we got the object

    # if instance didn't match any unique field
    if not instance:
        # iterate trough model constraints
        for constraint in model._meta.unique_together:
            try:
                # try to query a single object
                instance = model.objects.get(
                    **{key: val for key, val in fields.items() if key in constraint}
                )
            except model.DoesNotExist:
                pass  # didn't match, continue
            else:
                break  # matched, we got the object

    # if instance didn't match any model constraint
    if not instance:
        # if fields is empty, we'll return None
        if fields:
            # create the object
            instance = model.objects.create(**fields)
            created = True
    # if at least two fields are provided, try to update the object
    elif len(fields) > 1:
        changed = False
        # iterate trough fields
        for key, val in fields.items():
            old_val = getattr(instance, key, None)
            # if the value differs from the instance's value
            if not old_val or old_val != val:
                # update object field
                setattr(instance, key, val)
                changed = True
        # if anything changed, save the object
        if changed:
            instance.save()

    return instance, created
