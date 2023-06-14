import sqlite3 as sql

from flask import Flask


def register_commands(app: Flask):
    db_file = app.config['DATABASE']

    @app.cli.command('db_init')
    def db_init_command():
        """
        Initializes the database.
        """
        with sql.connect(db_file) as conn:
            conn.execute(
                'CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, description TEXT, release_year INT)')

        print('Initialized the database.')

    @app.cli.command('db_drop')
    def db_drop_command():
        """
        Drops the database.
        """
        with sql.connect(db_file) as conn:
            conn.execute('DROP TABLE movies')

        print('Dropped the database.')

    @app.cli.command('db_seed')
    def db_seed_command():
        """
        Seeds the database.
        """
        with sql.connect(db_file) as conn:
            conn.execute(
                'INSERT INTO movies(title,description,release_year) VALUES ("The Matrix","The Matrix is a computer-generated dream world designed to...","1999")')
            conn.execute(
                'INSERT INTO movies(title,description,release_year) VALUES ("The Matrix Reloaded","Continuation of cult clasic The Matrix...","2003")')
        print('Seeded the database.')
