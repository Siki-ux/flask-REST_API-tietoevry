import sqlite3 as sql

from flask import request, jsonify, abort, Flask

from api.utils import get_one_line


def register_routes(app: Flask):
    db_file = app.config['DATABASE']

    @app.route('/movies', methods=['GET', 'POST'])
    def movies():
        """
        Handles requests related to the movies resource.

        Returns:
            str: JSON string representing the response message.

        Raises:
            Exception: If an exception occurs during the processing of the request.
        """
        try:
            # Establish a connection to the database
            with sql.connect(db_file) as conn:
                
                match request.method:
                    case 'POST':
                        # Extract data from the request JSON
                        data = request.json
                        title = str(data["title"])
                        description = str(data['description'])
                        release_year = int(data['release_year'])

                        # Construct the SQL query to insert the movie information
                        exec_string = f'INSERT INTO movies(title,description,release_year) VALUES ("{title}","{description}","{release_year}")'
                        # Execute the SQL query
                        conn.execute(exec_string)

                        # Get the newly inserted movie information
                        msg = get_one_line(conn, None, title)
                    case 'GET':
                        # Configure the row factory to return rows as dictionaries
                        conn.row_factory = sql.Row
                        cur = conn.cursor()
                        
                        # Retrieve all rows from the movies table
                        rows = cur.execute("SELECT * FROM movies").fetchall()
                        # Convert the rows to a list of dictionaries
                        msg = [dict(ix) for ix in rows]

        except ValueError as e:
            abort(400, e)
        except KeyError:
            abort(400, 'Missing key in the request JSON data')
        except sql.Error:
            # Error occurs during the processing of the request
            abort(500)

        return jsonify(msg)

    @app.route('/movies/<int:id>', methods=['GET', 'PUT'])
    def movie(id):
        """
        Handles requests related to a specific movie identified by its ID.

        Args:
            id (int): The ID of the movie.

        Returns:
            str: JSON string representing the response message.

        Raises:
            KeyError: If there is a missing key in the request JSON data.
            Exception: If an exception occurs during the processing of the request.
        """
        try:
            # Establish a connection to the database
            with sql.connect(db_file) as conn:

                # Get the movie information for the given ID
                msg = get_one_line(conn, id, None)

                if request.method == 'PUT':
                    # Extract data from the request JSON
                    data = request.json
                    title = str(data['title'])
                    description = str(data['description'])
                    release_year = int(data['release_year'])

                    # Construct the SQL query to update the movie information
                    exec_string = f'UPDATE movies SET title="{title}",description="{description}",release_year="{release_year}" WHERE id={id}'
                    # Execute the SQL query
                    conn.execute(exec_string)
                    # Get the updated movie information
                    msg = get_one_line(conn, id, None)

        except ValueError as e:
            abort(400, e)
        except KeyError:
            abort(400, 'Missing key in the request JSON data')
        except sql.Error:
            # Error occurs during the processing of the request
            abort(500)

        return jsonify(msg)
