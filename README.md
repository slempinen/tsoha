## Fun forum - a simple forum app

This application is a very simple and unpolished forum website made with [flask](https://flask.palletsprojects.com/en/2.1.x/). It was made for the university of helsinki course [Tietokantasovellus](https://hy-tsoha.github.io/materiaali/) and as such follows the code practises recommended on the course.

### Usage

The forum app has 2 types of forums: public and private. Private forums can be password protected or invite only.
A user can join an invite only if an admin adds the user.

**An anonymous user** can view public forums and topics.

**A registered user** anything an anonymous user can, comment on topics, edit their comment and create topics on public forums and private forums if they are a member of that private forum.

**An admin** can do all of the above, view all forums, create forums, add members to private forums and delete topics.

Comments and forums can not be deleted. 

### Requirements and setup for local development

Project depends on python, docker and docker-compose for local development.

Project was tested with the following dependency versions.

* Python3.8.10
* Docker version 20.10.14
* docker-compose version 1.29.2

Run the following commands inside project root directory to run the project locally:

```sh
# Start postgres with docker-compose
docker-compose up --build --detach

# Setup python virtual environment
python -m venv .venv
source .venv/bin/activate

# Install python dependencies and set env vars for development
pip install -r requirements.txt
export FLASK_APP=flaskr
export FLASK_ENV=development

#Run app
flask run
```

### Creating an admin account locally

The app doesn't have any admin accounts by default.

To create an admin account you must manually run the following command after you have registered an account in the app.

```sh
# Replace [username] with your username
docker exec pg_container psql -U postgres -c 'UPDATE account SET is_admin = true WHERE username = [username]'
```



