Song Oracle
===========

Song Oracle is an application designed to show you information about your favorite songs from your favorite artists. Simply search for your favorite artist, select one of their top songs, and the application will present you with all of the relevant information about it, including its album name and art, the artists of the song, its duration, and even a song preview and a link to the lyrics (if applicable). The application uses Python/Flask to serve the application, the Spotify API to retrieve song and artist information, and the Genius API to retrieve lyric information. An example instance of this application has been set up and deployed via Heroku, which you can find [here](https://boiling-hollows-64005.herokuapp.com/).

Project Questions
-----------------
1. What are at least 3 technical issues you encountered with your project? How did you fix them? - The three most challenging issues with this project were retrieving information from the 3rd-party APIs, relative page redirects, and page formatting via CSS. Requests for information from 3rd-party APIs must be handled in a specific manner using a REST-ful approach, so finding the correct ways to retrieve the access tokens to get the data and then trying to format the requests correctly involved searching the internet for situations where other people may have come across similar problems and then applying a mixture of their solutions, along with reading the documentation for the APIs, to solve my own problems. This was also the same approach I took to solving the issue of how to handle redirects to other pages, such as redirecting to the song information page from the index page, and formatting the pages with CSS so every element aligned correctly.
2. What are known problems (still existing), if any, with your project? - The primary problems with this project currently are insufficient formatting and possible search input corruption. Aside from the problem of minimal page formatting with CSS (I'm not a great designer so this problem is fairly unsolvable for me), there is the possibility of a user entering malformed text into the search field, through which bad requests could potentially be made. The requests are formatted to be acceptable to send over HTTP requests (i.e. special characters like ampersand literals are properly escaped), however I don't know how Spotify handles the request once it reaches their end, so there is the possibility of something like a SQL injection if it is not handled correctly.
3. What would you do to improve your project in the future? - To improve this project, I would format the pages better by adding custom animations and better fonts, as well as adding more features such as a feature that allows you to connect your Spotify account so that the website can suggest songs it thinks the user might like.

Project Dependencies
--------------------
- Python 3.0 or greater
- PIP
- Flask
- python-dotenv
- Requests
- Spotify API
- Genius API
- JQuery

Installation
------------
To get set up, you'll need Python 3 or greater and PIP installed. Then, all you need to do is download the project and from the project root directory, run the following command:

```bash
pip install -r requirements.txt
```

This will install all of the necessary Python libraries required by this project, including [flask](https://flask.palletsprojects.com/en/2.0.x/), [dotenv](https://github.com/theskumar/python-dotenv), and [requests](https://docs.python-requests.org/en/latest/). From there, you will need to obtain a Spotify developer account and a Genius developer account. From your Spotify account, you will need to obtain your client ID and your client secret, and from your Genius account, you will need to obtain an access token. These should then be stored as environment variables in a file called `.env` in the project root directory, which should look something like this:

```bash
export SPOTIFY_CLIENT_ID=<your-spotify-client-id>
export SPOTIFY_CLIENT_SECRET=<your-spotify-client-secret>
export GENIUS_ACCESS_TOKEN=<your-genius-access-token>
```

Then simply run `python3 main.py`, and the server will be up and running. By default, the app will be bound to 0.0.0.0 on port 8080, however this can be changed by setting the `IP` and `PORT` environment variables, respectively.