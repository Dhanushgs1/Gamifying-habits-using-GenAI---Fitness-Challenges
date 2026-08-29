# Fitness Challenges

A small Flask app for tracking fitness challenges. Add a challenge with a name,
a description and a duration in days, and it is stored in SQLite and listed on
the home page.

## Stack

| Layer    | Choice                      |
| -------- | --------------------------- |
| Web      | Flask + Jinja templates     |
| Database | SQLAlchemy over SQLite      |
| Styling  | One plain stylesheet        |

## Running it

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

Open `http://127.0.0.1:5000`. `db.create_all()` runs at startup, so `app.db` is
created on first launch with no migration step.

## Data model

One table:

| Column        | Type         | Notes                    |
| ------------- | ------------ | ------------------------ |
| `id`          | Integer      | Primary key.             |
| `name`        | String(100)  | Required.                |
| `description` | String(200)  | Required.                |
| `duration`    | Integer      | Required, in days.       |

## Routes

| Method | Route   | Does                                                     |
| ------ | ------- | -------------------------------------------------------- |
| GET    | `/`     | Lists every challenge.                                   |
| POST   | `/add`  | Adds one. Missing fields flash an error and redirect back. |

## Configuration

`config.py` holds the settings, loaded via `app.config.from_object('config')`:

| Setting                   | Value                        |
| ------------------------- | ---------------------------- |
| `SECRET_KEY`              | `'your_secret_key'`          |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///app.db` next to the project |

`SECRET_KEY` is still the placeholder from the template. It signs the session
cookie that carries flash messages, so replace it, ideally reading it from the
environment rather than committing it.

## Before it runs

`index.html` sits in the repository root, but `render_template('index.html')`
looks in a `templates/` directory. Move it there:

```bash
mkdir -p templates && git mv index.html templates/index.html
```

`styles.css` needs the same treatment, into `static/`, and the template should
reference it with `url_for('static', filename='styles.css')`.

`app.py` also calls `db.create_all()` outside an application context, which
newer Flask-SQLAlchemy versions reject. `requirements.txt` pins
`Flask==2.1.2` and `Flask-SQLAlchemy==2.5.1`, where it still works; if you
upgrade, wrap it:

```python
with app.app_context():
    db.create_all()
```

## Layout

```
app.py             Model, routes, startup
config.py          Secret key and database URI
index.html         Challenge list and add form
styles.css         Styling
requirements.txt
```

## Known gaps

- There is no edit or delete route; challenges can only be added.
- `duration` is cast with `int()` without validation, so a non-numeric value
  raises a 500 instead of flashing an error.
- The app runs with `debug=True`. Turn that off before deploying.
