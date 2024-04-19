from .models import Customer, UserInfo, logHistory


def detect_changes(request, model_instance):
    """
    Detect changes and update the model instance with new data from the request.

    Args:
    request: The HTTP request containing the new data.
    model_instance: The instance of the model to update.

    Returns:
    A dictionary of changes with keys as field names and values as tuples (old_value, new_value).
    """

    # customer.name = request.POST.get('username')
    #             customer.email = request.POST.get('email')
    #             customer.age = request.POST.get('age')
    #             customer.address = request.POST.get('address')
    #             customer.phone_number = request.POST.get('phone_Number')
    #             customer.orders = request.POST.get('order')
    #             customer.vip_status = request.POST.get('vip_status')
    # Define which fields to check from the request
    fields = ['name', 'email', 'age', 'address', 'phone_number', 'orders', 'vip_status']
    changes = {}

    # Iterate through each field and compare with the instance's current values
    for field in fields:
        if field in request.POST:
            new_value = request.POST[field]
            old_value = getattr(model_instance, field)
            # print('.................. Test,,,,,,,,,,,,,,,,,,',field, new_value, getattr(model_instance, field))
            if str(old_value) != str(new_value):
                changes[field] = (old_value, new_value)
                setattr(model_instance, field, new_value)

    # Save the model instance only if there are changes
    if changes:
        # model_instance.save()
        return changes
