Base Skeleton to start your application using Flask-AppBuilder
--------------------------------------------------------------

- Install it::

	pip install flask-appbuilder
	git clone https://github.com/dpgaspar/Flask-AppBuilder-Skeleton.git

- Run it::

    $ pyenv shell 3.8.5
    $ export FLASK_APP=app
    # Create an admin user
    $ flask fab create-admin
    # Run dev server
    $ flask run



That's it!!

This project should create the basic structure in your airflow project to start using airdraw.

- so we are going to create a typer app to manage our commands
- create a Dockerfile to containerize our app
- create a docker-compose.yml to orchestrate our app with a Postgres database
- create a Makefile to help with common tasks
- create a .env file to manage environment variables