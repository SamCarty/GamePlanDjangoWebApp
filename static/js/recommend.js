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

function getTopGenreRecommendations(genre_id, element) {
    url = '/recommender/top-genre/' + genre_id + '/' + 50;
    fetchRecommendations(url, element)
}

function getRandomRecommendations(element) {
    url = '/recommender/random/' + 50;
    fetchRecommendations(url, element)
}

function getComingSoonRecommendations(element) {
    url = '/recommender/coming-soon/' + 50;
    fetchRecommendations(url, element)
}

function fetchRecommendations(url, section) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function (result) {
            if (result != null && result.data != null && Object.values(result.data).length > 0) {
                section.style.display = 'block';

                let heading = section.getElementsByTagName('h2')[0];
                let slider = section.getElementsByTagName('div')[0];

                if (result.based_on_title != null) {
                    heading.innerHTML = "Because you viewed " + result.based_on_title
                }

                Object.values(result.data).forEach(function (key) {
                    addRecommendation(key, slider);
                });

                createGameRecommendationSlider(slider);

            } else {
                section.style.display = 'none';
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
