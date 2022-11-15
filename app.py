import flask
from flask import Flask, request
import json
import requests
import random
import statistics
import numpy as np

app = Flask(__name__)

pokemon = ['togekiss', 'cyndaquil', 'charmander', 'dragonite', 'lugia']
base_url = "https://pokeapi.co/api/v2/pokemon/"


@app.route('/')
def hello_world():
    """
        Hello world function that displays a simple pokemon-related text.

    """
    return 'Hello World, Charmander is 50lbs'


@app.route('/v1/health')
def health():
    """
        A health endpoint as confidence check for API access.

    """

    try:
        force_error = request.args.get('forceServerError')
        if force_error:
            response = flask.jsonify("forceServerError present, please contact the help desk.")
            response.status_code = 500
        else:
            response = flask.jsonify('forceServerError not present, this endpoint is healthy.')
            response.status_code = 200

    except Exception as e:
        print(e)
        response = flask.jsonify("Response is null.")
        response.status_code = 400

    return response


@app.route('/v1/favorites')
def pokemon_data():
    """

        An endpoint that displays formatted Pokemon data on name, height, weight,
        base happiness, color, and 2 random moves. Extends to include aggregated
        base_happiness data if any value is passed into query parameter "includeHappiness".

    """

    try:
        include_happiness = request.args.get('includeHappiness')
        to_jsonify = pokemon_favorites()
        status_code = 200
        if include_happiness:
            to_jsonify['aggregated base happiness data'] = happy_stats()

    except Exception as e:
        print(e)
        to_jsonify = "No pokemon data found, inputs likely incorrect"
        status_code = 400

    response = flask.jsonify(to_jsonify)
    response.status_code = status_code
    return response


def pokemon_favorites() -> dict:
    """
        Returns formatted name, height, weight, 2 random moves, color, and base happiness of my top 5 favorite pokemon.

    """

    favorites = []

    for mon in pokemon:
        result = pokemon_return(mon)
        favorites.append(result)

    favorites_json = {"pokemon": favorites}

    return favorites_json


def happy_stats() -> dict:
    """

        Returns the arithmetic mean (average), geometric mean, and median base happiness for my top 5 favorite pokemon.

    """
    total_base_happiness = []

    for mon in pokemon:
        url = base_url + mon
        response = requests.get(url=url)
        species_url = response.json().get('species').get('url')
        species_response = requests.get(url=species_url)
        base_happiness = int(species_response.json().get('base_happiness'))
        total_base_happiness.append(base_happiness)

    happy_average = statistics.mean(total_base_happiness)
    happy_median = statistics.median(total_base_happiness)
    a = np.array(total_base_happiness)
    n = len(total_base_happiness)
    happy_geo_mean = a.prod() ** (1 / n)

    result = {
        "average": happy_average,
        "median": happy_median,
        "geometric mean": happy_geo_mean
    }

    return result


def pokemon_return(mon: str) -> dict:
    """

        A helper method for pokemon_favorites() method.

    """
    url = base_url + mon
    response = requests.get(url=url)
    species_url = response.json().get('species').get('url')
    species_response = requests.get(url=species_url)

    base_happiness = species_response.json().get('base_happiness')
    color = species_response.json().get('color').get('name')

    name = response.json().get('name')
    height = response.json().get('height')
    weight = response.json().get('weight')
    moves = response.json().get('moves')

    moves_set = set()
    for item in moves:
        moves_set.add(item.get('move').get('name'))

    moves_final = [str(x) for x in random.sample(moves_set, 2)]

    result = {
        "name": name,
        "height": height,
        "height units": "decimeters",
        "weight": weight,
        "weight units": "hectograms",
        "moves": moves_final,
        "color": color,
        "base happiness": base_happiness
    }

    return result


if __name__ == "__main__":
    app.run(debug=True)
