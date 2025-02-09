from django.contrib import messages

def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    return {}