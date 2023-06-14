# flusk-REST_API-tietoevry

This is a simple Flask-based API for managing a movie database. The API allows you to perform CRUD (Create, Read, Update, Delete) operations on movie records stored in an SQLite database.<br>
this repository serves to present the development and understanding of REST API service in python


## Features

- Retrieve a list of all movies
- Retrieve information about a specific movie
- Add a new movie to the database
- Update information for an existing movie

## Requirements

- Python 3.x
- Flask
- SQLite3

## API Endpoints
### GET /movies
Returns a list of all movies in the database.<br>
```bash
curl -X GET http://127.0.0.1:5000/movies/
```
Example Response:
```json
[
  {
    "id": 1,
    "title": "Movie 1",
    "description": "Description of Movie 1",
    "release_year": 2021
  },
  {
    "id": 2,
    "title": "Movie 2",
    "description": "Description of Movie 2",
    "release_year": 2022
  }
]
```
### GET /movies/{int:id}
Returns information about a specific movie identified by the {id} parameter.<br>
```bash
curl -X GET http://127.0.0.1:5000/movies/1
```
Example Response:
```json
{
  "id": 1,
  "title": "Movie 1",
  "description": "Description of Movie 1",
  "release_year": 2021
}
```

### POST /movies
Adds a new movie to the database. The movie information should be provided in the request body as a JSON object.<br>
```bash
curl -X POST http://127.0.0.1:5000/movies -H 'Content-Type: application/json' -d '{"title": "The cars", "description":"Set in a world populated entirely by anthropomorphic 
```
Example Response:
```json
{
  "title": "The cars",
  "description": "Set in a world populated entirely by anthropomorphic talking cars and other vehicles,...",
  "release_year": 2010
}
```

### PUT /movies{id}
Updates the information of a specific movie identified by the {id} parameter. The updated movie information should be provided in the request body as a JSON object<br>
```bash
curl -X PUT http://127.0.0.1:5000/movies/1 -H 'Content-Type: application/json' -d '{"title": "The cars", "description":"Set in a world populated entirely by anthropomorphic talking cars and other vehicles,...", "release_year":"2011"}'
```
Example Response:
```json
{
  "title": "The cars",
  "description": "Set in a world populated entirely by anthropomorphic talking cars and other vehicles,...",
  "release_year": 2011
}
```

### GET /movies/init
Initialize table movies in database and fill it with some data. Drops existing table.
```bash
curl -X GET http://127.0.0.1:5000/movies/init
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/movie-database-api.git
```

2. Run script:

```bash
python3 api.py
```

3. Initialize the database:
```bash
curl -X GET http://127.0.0.1:5000/movies/init
```

4. Enjoy





