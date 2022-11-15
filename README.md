# PokeAPI Wrapper 
[Official PokeAPI Documentation](https://pokeapi.co/docs/v2)

### Description
A simple Python Flask app that serves as an API wrapper for the official Pokemon API.
This was completed as a take home assessment. 

### Endpoints
There are three endpoints: 
1. '/': A simple hello world. 
2. '/v1/health': A health endpoint that displays simple text. This has an optional query parameter "forceServerError" that, when any value is passed in, will return a 500 response with some text.
3. /v1/favorites': Displays name, height, weight, 2 random moves, and base happiness of my top 5 pokemon. This has an optional query parameter "includeHappiness" that, when any value is passed in, extends the endpoint to display additional aggregated information on the base_happiness attribute of the favorited pokemon.


### Quick Start

1. git clone git@github.com:marielaquino/pythonProject.git
2. cd pythonProject/
3. docker build -t pokeapi-wrapper .
4. docker run -p 14420:5000 pokeapi-wrapper

Port 14420 can be changed to any port if currently in use. 

### Accessing endpoints from CLI 

1. curl -v http://127.0.0.1:5000/ : displays hello world text 
2. curl -v http://127.0.0.1:5000/v1/health : displays health endpoint text
3. curl -v http://127.0.0.1:5000/v1/health?forceServerError={anyvalue} : displays error message 
4. curl -v http://127.0.0.1:5000/v1/favorites : displays favorite pokemon data
5. curl -v http://127.0.0.1:5000/v1/favorites?includeHappiness={anyvalue} : displays favorite pokemon data with base happiness aggregated data 

### Thanks for your time! 🙏 