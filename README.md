# URL Shortener

A modern, minimal URL shortener built with Flask and Bootstrap 5.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

## Features

- **RESTful API** - Shorten, retrieve, and delete URLs
- **Modern UI** - Bootstrap 5 with glass-morphism design

## API Endpoints

| Method | Endpoint         | Description         |
|--------|------------------|---------------------|
| GET    | `/api/url`       | Get all URLs        |
| POST   | `/api/url`       | Create short URL    |
| DELETE | `/api/url/{id}`  | Delete short URL    |
| GET    | `/api/url/{id}`  | get orignal URL     |

## Project Structure

```
├── app.py              # Main Flask app
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
└── .gitignore          # Git ignore rules
```

## Next Steps

- Add database (SQLAlchemy + PostgreSQL)
- Implement user authentication
- Add URL shortening functions
- Deploy to cloud platform

## License

MIT License - feel free to customize! 