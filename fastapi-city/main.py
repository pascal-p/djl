from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import requests


app = FastAPI()

# in memory  db
db = [
    {
        "name": "Las Vegas",
        "timezone": "America/Los_Angeles"
    },
    {
        "name": "Miami",
        "timezone": "America/New_York"
    },
    {
        "name": "San Fransisco",
        "timezone": "America/Los_Angeles"
    },
]

class City(BaseModel):
    name: str
    timezone: str


#
# Endpoints
#

@app.get('/')
def index():
    return 'Hello FastAPI'

@app.get('/cities')
def get_cities():
    res = []
    for city in db:
        cur_time = get_cur_time(city)
        res.append({
            'name': city['name'],
            'timezone': city['timezone'],
            'current_time': cur_time
        })
    return res                     ## FastAPI takes care of json-ify the output!

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    if not check_id(city_id, db):
        return 'no such city to display'
    #
    city = db[city_id - 1 if city_id > 0 else 0]
    cur_time = get_cur_time(city)
    return {
        'name': city['name'],
        'timezone': city['timezone'],
        'current_time': cur_time
    }

@app.post('/cities')              ## Using type annotation
def create_city(city: City):
    db.append(city.dict())
    return db[-1]                 ## return the created city

@app.put('/cities/city_id')
def update_city(city_id: int, city: City):
    if not check_id(city_id, db):
        return 'No such city to update...'
    #
    db[city_id - 1] = city.dict()
    return db[city_id - 1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    if not check_id(city_id, db):
        return 'No such city to delete..'
    #
    db.pop(city_id - 1)
    return {}

#
# Internal
#
def check_id(city_id: int, db: Dict):
    return len(db) >= 0 and 0 <= city_id < len(db)

def get_cur_time(city: str):
    r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    return r.json()['datetime']
