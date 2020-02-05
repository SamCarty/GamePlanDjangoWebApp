function logDetailViewEvent(content_id, csrf_token, session_id) {
    addEvent(content_id, 'detail_view_event', csrf_token, session_id)
}

function logWishlistEvent(content_id, csrf_token, session_id) {
    addEvent(content_id, 'wishlist_event', csrf_token, session_id)
}

function logPurchaseEvent(content_id, csrf_token, session_id) {
    addEvent(content_id, 'purchase_event', csrf_token, session_id)
}

function logRecommendationViewEvent(content_id, csrf_token, session_id) {
    addEvent(content_id, 'rec_view_event', csrf_token, session_id)
}

function logGenreViewEvent(content_id, csrf_token, session_id) {
    addEvent(content_id, 'genre_view_event', csrf_token, session_id)
}

function logScreenshotViewEvent(content_id, csrf_token, session_id) {
    addEvent(content_id, 'screenshot_view_event', csrf_token, session_id)
}

function addEvent(content_id, event_type, csrf_token, session_id) {
    $.ajax({
        type: 'POST',
        url: '/gatherer/log-event/',
        data: {
            'event_type': event_type,
            'content_id': content_id,
            'csrfmiddlewaretoken': csrf_token,
            'session_id': session_id
        },
        fail: function () {
            console.log('Event failed to log: ' + event_type)
        },
    });
}
