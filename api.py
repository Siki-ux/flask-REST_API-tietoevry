# Simple scrpit for API of DB about movies 
# Author: Jakub Sikula

# Import the necessary modules
from flask import Flask, request, abort, jsonify
import sqlite3 as sql

app = Flask(__name__)
@app.route('/movies', methods=['GET','POST'])
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
        conn = sql.connect('database.db')
        

        if request.method == 'POST':
            # Extract data from the request JSON
            data = request.json
            title = data["title"]
            description = data['description']
            release_year = data['release_year']

            # Construct the SQL query to insert the movie information
            exec_string = 'INSERT INTO movies(title,description,release_year) VALUES ("'+title+'","'+description+'","'+release_year+'")'  
            # Execute the SQL query
            conn.execute(exec_string)
            
            # Get the newly inserted movie information
            msg = get_one_line(conn,None,title)
        else:
            # Configure the row factory to return rows as dictionaries
            conn.row_factory = sql.Row
            cur = conn.cursor()
            # Retrieve all rows from the movies table
            rows = cur.execute("SELECT * FROM movies").fetchall()
            # Convert the rows to a list of dictionaries
            msg = [dict(ix) for ix in rows]
    except KeyError:
        # If there is a missing key in the request JSON data, return a 400 error
        abort(400)
    except sql.Error:
        # If any SQLite error occurs during the processing of the request, return a 500 error
        abort(500)
    except:
        # If any exception occurs during the processing of the request and return a 404 error
        abort(404)
    # Return the JSON response
    return jsonify(msg)

@app.route('/movies/<int:id>',methods=['GET','PUT'])
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
        with sql.connect('database.db') as conn:

            # Get the movie information for the given ID
            msg = get_one_line(conn,id,None)

            if request.method == 'PUT':
                # Extract data from the request JSON
                data = request.json
                title = data['title']
                description = data['description']
                release_year = data['release_year']

                # Construct the SQL query to update the movie information
                exec_string = 'UPDATE movies SET title="'+title+'",description="'+description+'",release_year="'+release_year+'" WHERE id='+str(id)
                # Execute the SQL query
                conn.execute(exec_string)
                # Get the updated movie information
                msg = get_one_line(conn,id,None)
    except KeyError:
        # If there is a missing key in the request JSON data, return a 400 error
        abort(400)
    except sql.Error:
        # If any SQLite error occurs during the processing of the request, return a 500 error
        abort(500)
    except:
        # If any exception occurs during the processing of the request and return a 404 error
        abort(404)

   # Return the JSON response
    return jsonify(msg)



def get_one_line(conn,id=None,title=None):
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
            exec_string = "SELECT * FROM movies WHERE id="+str(id)
        elif id is None and title is not None:
            exec_string = "SELECT * FROM movies WHERE title='"+str(title)+"'"

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
            # If no row is found, raise an exception
            raise Exception()
    except sql.Error:
        # If any SQLite error occurs during the processing of the request, return a 500 error
        abort(500)
    except:
        # If any exception occurs, abort the request with a 404 status code
        abort(404)
    

@app.route('/movies/init',methods=['GET'])
def db_init():
    try:
        # Establish a connection to the database
        with sql.connect('database.db') as conn:
            # Initialize movie table and add some data to movie table
            conn.execute('DROP TABLE IF EXISTS movies')
            conn.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, description TEXT, release_year INT)')
            conn.execute('INSERT INTO movies(title,description,release_year) VALUES ("The Matrix","The Matrix is a computer-generated dream world designed to...","1999")')  
            conn.execute('INSERT INTO movies(title,description,release_year) VALUES ("The Matrix Reloaded","Continuation of cult clasic The Matrix...","2003")')
    except sql.Error:
        # If any SQLite error occurs during the processing of the request, return a 500 error
        abort(500)
    except:
        # If any exception occurs during the processing of the request and return a 404 error
        abort(404)
    return "done"

if __name__ == '__main__':
   app.run(debug = True)