
# Spotify-Automatization

Automatization on spotify because I lost too many liked songs (I'm a braindead)

## Deployment

To deploy this project using SQLite

```bash
  python main_sqlite.py
```

And using PostgreSQL

```bash
  python main_post.py
```



## Run locally
Clone the project
```bash
  git clone https://github.com/LucasdeOliveira03/Spotify-Automatization.git
```

Go to your desire database

```bash
  cd postgres
  # or
  cd sqlite
```
Create and activate Virtual Environment

```bash
  python -m venv venv
  .\venv\Scripts\activate
```

Install dependencies

```bash
  pip install -r .\requirements.txt
```

Start the application

```bash
  python main_sqlite.py
  # or
  python main_post.py
```


## Environment Variables
For SQLite database
```bash
  CLIENT_ID = "your CLIENT_ID"
  CLIENT_SECRET = "your CLIENT_SECRET"
  REDIRECT_URI = "http://127.0.0.1:8888/callback"
```

And for PostgreSQL database
```bash
  CLIENT_ID = "your CLIENT_ID"
  CLIENT_SECRET = "your CLIENT_SECRET"
  REDIRECT_URI = "http://127.0.0.1:8888/callback"

  DATABASE = "Your DATABASE"
  USER = "Your USER"
  PASSWORD = "Your PASSWORD"
  HOST = "Your HOST"
  PORT = Your PORT
```
