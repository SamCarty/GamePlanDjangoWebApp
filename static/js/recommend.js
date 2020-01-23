function getTopChartRecommendations() {
    url = '/recommender/top-charts';
    $.ajax({
        type: 'GET',
        url: url,
        success: function (result) {
            if (result.data != null) {
                Object.values(result.data).forEach(function (key) {

                });
            }
        }
    });
}

function getContentRecommendations(gameId, element) {
    url = '/recommender/content-based/' + gameId + '/' + 60;
    fetchRecommendations(url, element, gameId);
}

function getBoughtTogetherRecommendations(gameId, element) {
    url = '/recommender/bought-together/' + gameId + '/' + 60;
    fetchRecommendations(url, element, gameId)
}

function getUsersLikeYouRecommendations(element) {
    url = '/recommender/like-you/' + 50;
    fetchRecommendations(url, element)
}

function getSimilarToRecentRecommendations(element) {
    url = '/recommender/similar-to-recent/' + 50;
    fetchRecommendations(url, element)
}

function fetchRecommendations(url, section) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function (result) {
            if (result.data != null) {
                section.style.display = 'block';
                Object.values(result.data).forEach(function (key) {
                    addRecommendation(key, section);
                });

                if (result.based_on_title != null) {
                    heading = document.getElementById('heading-rec-content-based');
                    heading.innerHTML = "Because you viewed " + result.based_on_title
                }
                createGameRecommendationSlider(section);
            }
        }
    });
}

function addRecommendation(game, section) {
    itemDiv = document.createElement('div');
    itemDiv.setAttribute('class', 'slider-cell');

    itemImage = document.createElement('img');
    itemImage.setAttribute('class', 'title-image');
    itemImage.setAttribute('data-flickity-lazyload', 'https://' + game['cover']);
    itemImage.setAttribute('title', game['title']);

    itemTitle = document.createElement('p');
    itemTitle.setAttribute('class', 'title-name');
    itemTitle.innerHTML = game['title'];

    itemLink = document.createElement('a');
    itemLink.setAttribute('href', '/games/' + game['game_id']);
    itemLink.appendChild(itemImage);
    itemLink.appendChild(itemTitle);
    itemDiv.appendChild(itemLink);
    section.appendChild(itemDiv);
}

function createGameRecommendationSlider(section) {
    let slider = new Flickity(section, {
        cellAlign: 'left',
        initialIndex: 0,
        lazyLoad: 9,
        prevNextButtons: true,
        pageDots: false,
        setGallerySize: true,
        wrapAround: true
    });

    /*
    slider.on('change', function (index) {
        logRecommendationViewEvent(game_id, csrftoken, sessionid)
    })
     */
}
