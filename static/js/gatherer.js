function log_detail_view_event(content_id, csrf_token) {
    add_event(content_id, 'detail_view_event', csrf_token)
}

function log_wishlist_event(content_id, csrf_token) {
    add_event(content_id, 'wishlist_event', csrf_token)
}

function log_purchase_event(content_id, csrf_token) {
    add_event(content_id, 'purchase_event', csrf_token)
}

function log_recommendation_view_event(content_id, csrf_token) {
    add_event(content_id, 'rec_view_event', csrf_token)
}

function log_genre_view_event(content_id, csrf_token) {
    add_event(content_id, 'genre_view_event', csrf_token)
}

function log_screenshot_view_event(content_id, csrf_token) {
    add_event(content_id, 'screenshot_view_event', csrf_token)
}

function add_event(content_id, event_type, csrf_token) {
    $.ajax({
        type: 'POST',
        url: '/gatherer/log-event/',
        data: {
            'event_type': event_type,
            'content_id': content_id,
            'csrfmiddlewaretoken': csrf_token
        },
        fail: function () {
            console.log('Event failed to log: ' + event_type)
        }
    });
}
