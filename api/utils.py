# Script containing routes methods
# Author: Jakub Sikula

# Import the necessary modules
import sqlite3 as sql
from flask import abort


def get_one_line(conn, id=None, title=None):
    """
    Retrieves a single line (row) from the 'movies' table in the database based on the provided ID or title.

    Args:
        conn (Connection): The SQLite database connection object.
        id (int): The ID of the movie to retrieve. Defaults to None.
        title (str): The title of the movie to retrieve. Defaults to None.

    Returns:
        dict: A dictionary representing the retrieved row, where column names are mapped to row values.

    Raises:
        Exception: If no row is found based on the provided ID or title.
    """
    try:
        exec_string = ""
        # Construct the SQL query based on the provided parameters
        if title is None and id is not None:
            exec_string = "SELECT * FROM movies WHERE id=" + str(id)
        elif id is None and title is not None:
            exec_string = "SELECT * FROM movies WHERE title='" + str(title) + "'"

        # Create a cursor object and execute the SQL query
        cur = conn.cursor()
        row = cur.execute(exec_string).fetchone()

        # Check if a row is returned
        if row is not None:
            # Extract column names from the cursor's description
            columns = [description[0] for description in cur.description]
            # Create a dictionary mapping column names to row values
            return dict(zip(columns, row))
        else:
            # If no row is found
            abort(404, 'Movie not found')
    except sql.Error:
        # Error occurs during the processing of the request
        abort(500)
