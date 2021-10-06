tutorial on struturing unittests with flask restplus and sqlalchemy

from https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

### NOTES ###
- not using flask-script since we have flask cli providing that functionality oob
- set FLASK_RUN=entrypoint.py and FLASK_ENVIRONMENT=development
- flask db init; flask db migrate -m "initial migration"; flask db upgrade; (all baked in via "flask db" commands)
- not using flask-restplus as it is not maintained, replace with flask_restx