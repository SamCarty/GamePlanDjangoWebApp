import pytz
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from gatherer.models import Log


@ensure_csrf_cookie
def log_event(request):
    if request.method == 'POST':
        date = datetime.now(pytz.utc)
        event_type = request.POST['event_type']
        content_id = request.POST['content_id']
        session_id = request.POST['session_id']

        log = Log(
            created=date,
            event_type=event_type,
            content_id=content_id,
            session_id=session_id)

        if request.user.id is not None:
            user_id = request.user.id
            log.user_id = user_id

        log.save()
    else:
        return HttpResponse('Log only possible with a POST request!')

    return HttpResponse('ok')