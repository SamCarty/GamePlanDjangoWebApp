function getContentRecommendations(gameName, element) {
    url = '/recommender/content-based/' + gameName + '/' + 60;
    fetchRecommendations(url, element);
}

function fetchRecommendations(url, section) {
    $.getJSON(url, function (result) {
        if (result.data != null) {
            section.style.display = 'block';
            Object.values(result.data).forEach(function (key) {
                addRecommendation(key, section);
            });
            createSlider(section);
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

function createSlider(section) {
    new Flickity(section, {
        cellAlign: 'left',
        initialIndex: 0,
        lazyLoad: 9,
        prevNextButtons: true,
        pageDots: false,
        setGallerySize: true,
        wrapAround: true
    });
}