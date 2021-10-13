Song Oracle
===========

Song Oracle is an application designed to show you information about your favorite songs from your favorite artists. Simply search for your favorite artist, add it to your saved artists, and the application will suggest new and relevant artists to grow your collection. Every refresh of the website will show you a slightly different selection of artists and songs, so you'll never run out of selections to choose from. You can even select a song or an album that you like, and Song Oracle will present you with all of the relevant information about it, including the album name and art, the artists of the song, and even a song preview and a link to the lyrics (if applicable). The application uses Python/Flask to serve the application, PostgreSQL to store user data, the Spotify API to retrieve song and artist information, and the Genius API to retrieve lyric information. An example instance of this application has been set up and deployed via Heroku, which you can find [here](https://whispering-depths-18811.herokuapp.com/).

Project Questions
-----------------
1. What are at least 3 technical issues you encountered with your project? How did you fix them? - For this project I had the greatest technical difficulty with database linking, UI element positioning, and database formatting. Heroku, which is the platform I used to host the project, has a system to install a PostgreSQL server automatically. Consequently, it also provides the user with a URL to access the PostgreSQL database which is contained in an environment variable, however the URL it provides is invalid and must be altered to work correctly with SQLAlchemy. Unfortunately, Heroku does not allow the user to modify this environment variable through any normal means, so I had to improvise a fix within Python as a temporary solution. Another challenge was positioning UI elements on a given page, of which the biggest issues were centering elements and ensuring elements had the correct sizes. Recent updates to most popular browsers provided access to a CSS feature known as a flexbox display format, which was able to solve most of the issues, however there were still minor technicalities that the flexbox alone could not fix, of which had to be manually adjusted. Database formatting was the other big technical issue, which primarily involved ensuring the representation of the database in the Python code matched the representation in the actual PostgreSQL database. If there were any minor discrepancy between these two schemas, the application would fail to connect to the database and cause difficult to trace errors, however these were solved by ensuring the two schemas exactly matched one another.
2. What would you do to improve your project in the future? - In the future I would like to create a better UI experience overall for the application (to make the elements flow together better) and make page load times faster, as right now they are mostly bottlenecked by the speed of the Spotify API calls. In terms of new features, I would like to add the ability to remove saved artists and password authentication for users to make accounts more secure, as well as the ability to delete an account altogether.
3. How did your experience working on this milestone differ from what you pictured while working through the planning process? What was unexpectedly hard? Was anything unexpectedly easy? - With this project I mainly expected the database interfacing to be the most challenging part, and for the most part I was correct, however not exectly in the way I initially thought. I thought the hardest part would be sending and receiving data from the database, which was a challenge at first, but the hardest part of this process was making Heroku interface properly with the database. Making GET and POST requests both within the application as well as to external sources was unexpectedly easy, as on the Javascript side JQuery/AJAX greatly streamlines the process, and on the Python/Flask side the Requests library simplifies these request types to relatively few function calls.

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
- PostgreSQL
- psycopg2
- SQLAlchemy
- Flask Login
- Flask SQLAlchemy

Installation
------------
To get set up, you'll need Python 3 or greater and PIP installed. Then, all you need to do is download the project and from the project root directory, run the following command:

```bash
pip install -r requirements.txt
```

This will install all of the necessary Python libraries required by this project, including [flask](https://flask.palletsprojects.com/en/2.0.x/), [dotenv](https://github.com/theskumar/python-dotenv), [requests](https://docs.python-requests.org/en/latest/), and more. From there, you will need to obtain a Spotify developer account and a Genius developer account. From your Spotify account, you will need to obtain your client ID and your client secret, and from your Genius account, you will need to obtain an access token. These should then be stored as environment variables in a file called `.env` in the project root directory, which should look something like this:

```bash
export SPOTIFY_CLIENT_ID=<your-spotify-client-id>
export SPOTIFY_CLIENT_SECRET=<your-spotify-client-secret>
export GENIUS_ACCESS_TOKEN=<your-genius-access-token>
export DATABASE_URL=<your-postgresql-database-url>
export FLASK_SECRET_KEY=<your-flask-secret-key>
```

The `DATABASE_URL` variable is the URL to access your PostgreSQL database. If installing with Heroku, this variable will be provided for you.

The `FLASK_SECRET_KEY` variable should be a randomly generated sequence of characters and numbers of any length. For mine, I chose to generate an 86 character string of randomly generated lowercase letters, uppercase letters, numbers, and hyphens. This variable can be anything so long as it is in accordance with the [Flask standard](https://explore-flask.readthedocs.io/en/latest/configuration.html#secret-keys).

This project requires a PostgreSQL database to store user data. Install [PostgreSQL](https://www.postgresql.org/) and create a database with any name. You'll then need to create two tables to store the user data. The commands to create them are described below:

```sql
create table db_user(
    id int generated always as identity,
    username varchar(80) unique not null,
    status int not null default 1,
    creation_date timestamp not null default CURRENT_TIMESTAMP,
    last_login_date timestamp,
    last_logout_date timestamp,
    primary key(id)
);

create table db_artist(
    id int generated always as identity,
    user_id int,
    artist_id varchar(100) not null,
    artist_name varchar(255),
    primary key(id),
    constraint fk_user foreign key(user_id) references db_user(id)
);
```

Then simply run `python3 main.py`, and the server will be up and running. By default, the app will be bound to 0.0.0.0 on port 8080, however this can be changed by setting the `IP` and `PORT` environment variables, respectively.