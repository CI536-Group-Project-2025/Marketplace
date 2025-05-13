# Marketplace

To run and develop this project, you'll need to install [Docker](https://docs.docker.com/desktop/).

Once docker is installed, you can run the project with `docker compose up --build` in the command line. It's important to use the `--build` flag when you've updated code, otherwise the marketplace container **will not be rebuilt**, and **won't use your new code**.

You can kill the currently running containers with Ctrl-C and `docker compose down` in the terminal where they were running.

Docker will start PgAdmin (for viewing and administrating the Database) on http://localhost:80, and the site will be viewable at http://localhost:8000.

If you are at all not sure about anything do not hesitate to message me (Ben) about things. Generally speaking, I will have the answer or know where to find it.

There is example code of how to set up an API endpoint in both `__main__.py` and `users.py` (for interacting with the DB.
