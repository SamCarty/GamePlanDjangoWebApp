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
