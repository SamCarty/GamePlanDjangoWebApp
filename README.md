![GamePlan logo](https://user-images.githubusercontent.com/22345452/82842874-1ffa3200-9ed3-11ea-8435-25e9e62fdafe.png)

# GamePlan: A Video Games Recommendation System
> Copyright Sam Carty 2020

## About
GamePlan is a web application written in **[Python](https://www.python.org/)** using **[Django](https://www.djangoproject.com/)**, **[Scikit-Learn](https://scikit-learn.org/stable/)**, **[Pandas](https://pandas.pydata.org/)** and **[NumPy](https://numpy.org/)** which aims to provide gamers with relevant and dynamic game suggestions based on their play history and what they previously enjoyed.

The project provides a single point of entry for users to find information, release dates and of course, machine learning-based suggestions for what they should play next.

Both personalised and non-personalised recommendations will be used to provide a rich experience for all users, even if they haven't signed up for the service.

![GamePlan home page](https://user-images.githubusercontent.com/22345452/82844677-4622d080-9ed9-11ea-853d-3ff8f30e6986.png)

> Home page of the web application showing recommendations for the signed-in user.

## Implementation
The system is made up of three main APIs - the evidence gatherer, recommendations and content:

![Top-level architecture](https://user-images.githubusercontent.com/22345452/82843207-55ebe600-9ed4-11ea-87e6-e4e750abcb02.png)

### Evidence Gatherer
This component logs user actions which can be used to determine what users are interested in so that the recommendations API can suggest relevant content. This evidence is stored in a SQL database table with the corresponding user ID. 

**Explicit events** are evidence that is obtained through direct user action such as rating a piece of content.

**Implicit events** are evidence that is obtained though monitoring user actions such as clicking the 'add to wishlist' button. Each action is weighted differently depending on the impact it has on user satisfaction with a given title.

![Game details page](https://user-images.githubusercontent.com/22345452/82844713-766a6f00-9ed9-11ea-9b5c-e03c920e2118.png)

### Recommendations
This component provides users with game recommendations based on their preferences and the logs obtained by the evidence gatherer. Using both content-based (cosine similarities) and collaborative filtering (association rules), accurate recommendations can be generated for any given user. 

| **Recommender category** | **Type** | **Description** | **Location** |
| --- | --- | --- | --- |
| Because you viewed _[game]_ | Content-based | Selects games that are similar to the last game the user looked at according to the content-based algorithm. Based on evidence gatherer data. | Home |
| Because you like _[genre]_ | Content-based | Selects games in genres that the user enjoys according to the content-based algorithm. Based on evidence gatherer data. | Home |
| Because you like _[game]_ | Content-based | Selects games that are similar to games the user enjoys according to the content-based algorithm. Based on evidence gatherer data. | Home |
| Similar to _[game]_ | Content-based | Selects games that are similar to [game] according to the content-based algorithm. | Details |
| People like you | Association rules | Selects games that similar users enjoyed based on the current user&#39;s browsing activity. | Home |
| Frequently bought with _[game]_ | Association rules | Selects the other games that have purchased in the same session as _[game]._ | Details |
| Releasing soon | Non-personalised | All games ordered by their release date from today&#39;s date. | Home |
| Random | Non-personalised | Selects completely random titles from the database. | Home |
| Top rated | Non-personalised | Selects the highest rated games from the database. | Home |
| Popular now | Non-personalised | Selects the most popular games from the database. | Home |

## Recommendation Generation
The process of generating these suggested titles is made up of three parts, **candidate generation**, **scoring** and **re-ranking**.

### Candidate Generation
This is where the large dataset is transformed to a smaller subset of items based on the a relevance factor for a given user. 

For content-based recommendations, this process was done using the cosine similarity function which maps items and queries to structures known as **embedding vectors**, calculated by a similarity measure. This measure was implemented by converting each game's summary, storyline and genres to a **TF-IDF** (Term Frequency-Inverse Document Frequency) representation. This algorithm which handles this functionality will also remove any punctuation, capitalisation and any word within a pre-defined list of **stop-words**.

Association rules are used to provide collaborative filtering to the project by collating items into **item pairings** according to the frequency of them appearing in the same 'transaction'. In other words, if a user added both "Battlefield V" and "Call of Duty: Modern Warfare" to their wishlist, we can be reasonably confident that they like shooter games. 

### Scoring
The **confidence** and **support** metrics can be calculated for a given recommendation and this is used when scoring the suggestions by relevance.

### Re-ranking
The system ensures that any title the user has **explicitly disliked** is removed from their recommendation feed. This ensures users have control over the content they see and means that the system can learn more precisely what titles they enjoy.

![Frequently bought together](https://user-images.githubusercontent.com/22345452/82844716-779b9c00-9ed9-11ea-8261-3c3b4ced5000.png)

## Acknowledgements
Game data kindly provided by  [IGDB](https://www.igdb.com/api). It's a great API and even allows you to build a competing application for free!

### Libraries Used
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Scikit-Learn](https://scikit-learn.org/stable/)
* [Pandas](https://pandas.pydata.org/)
* [NumPy](https://numpy.org/)
* [pytz](https://pypi.org/project/pytz/)
* [django-filter](https://pypi.org/project/django-filter/)
* [Plotly](https://plotly.com/)
