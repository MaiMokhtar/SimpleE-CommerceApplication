# Simple E-Commerce Application

## System Description ##
This is a very simple e-commerce application.

## Technologies ##
* Python (3.9)
* Django (4.1)


## Requirements ##
* For development
    * Install `requirements.txt` file
  
## Quick Start ##
1. Clone the repository: `git clone https://github.com/MaiMokhtar/simple-e-commerce-application.git`.
1. Change directory to `cd simple-e-commerce-application/`.
1. Create a virtual environment `python3 -m venv env`.
1. Activate the virtual environment `source env/bin/activate`.
1. Install `requirements.txt` file `pip install -r requirements.txt`.
1. Seed the database `python -m _db_seed`.
1. Run instance of redis `docker run -p 6379:6379 -d redis:5`, otherwise the event-based notifications will not work.
1. Start up Django's development server `python manage.py runserver`
1. Brows the project at http://127.0.0.1:8000

