from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from gatherer.models import Log


@ensure_csrf_cookie
def log_event(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            date = datetime.now()
            user_id = request.user
            event_type = request.POST['event_type']
            content_id = request.POST['content_id']

            log = Log(
                created=date,
                user=user_id,
                event_type=event_type,
                content_id=content_id)

            log.save()
    else:
        return HttpResponse('Log only possible with a POST request!')

    return HttpResponse('ok')
