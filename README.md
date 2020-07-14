# Error Logging and Searching
This is a production grade RESTful API service which is used to receive, store and search through JavaScript errors produced by visitors on multiple websites. Each of the services used are horizontally scalable.

## Logging errors
Logging errors can be performed by making a post to the `logs/site_id` endpoint as follows:

```bash
curl --header "Content-Type: application/json" \
  --header "Referer: http://localhost" \
  --request POST \
  --data '{"message":"Some log message"}' \
  http://localhost:5000/api/v1/logs/site1
```

The `site_id` would be provided to the user when signing up for tha application and is used to verify requests. In the above example the Referer header is set explicitly, but this would be set by the client making the requests. For demo purposes there is a list of known sites can be found [here](app/dataprovider/site_dataprovider.py).

When a log message is sent to the API, the following data is stored:

Field | Data Type | Source | Info
--- | --- | --- | ---
browser | keyword | User-Agent | Supports exect matches
country | keyword | Geo Lookup from IP | Supports exect matches
url | text | Referer |Supports fuzzy search
message | test | POST | Supports fuzzy search


## Searching for errors:
Searching for errors requires authenticating first. Logging in can be performed as follows:

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"email":"site1@test.com", "password":"test"}' \
  http://localhost:5000/api/v1/auth/login
```

This will return an JWT `Authorization` token as follows:
```bash
{
    "Authorization": "some_jwt_token"
}
```

After logging in you will be able to query the logs, for example:
```bash
curl --header 'Authorization: auth_token_here'
  --request GET \
  'http://0.0.0.0:5000/api/v1/logs/site1?limit=10&page=1&query=some_urlencoded_query'

```

### Query format
In order to search for logs, the query has to be constructed in a specific manner:

```
[NOT] FIELD <IS | CONTAINS> 'search' [<AND | OR> ... ]
```

Where the `[]` represents optional, the `<>` represents required and `|` separates options. These queries can be grouped with parenthesis in order to control the order of precedence. `FIELD` can be any of the fields listed in the table above.

#### Examples
```
1. message contains 'error in foo'
2. browser is 'Internet Explorer'
3. url contains 'something'
4. country is not 'South Africa'
5. not (browser is 'Chrome' or browser is 'Safari') and message contains 'frogs'
```

## Installation and Running

### Installation
1. Clone out the repo.
2. `cd backend-task-david/`
3. `make run`

At this point you should see all of the services starting up in the terminal. If there are any Docker images that you do not have locally they will automatically be downloaded first. Wait a couple of seconds until Elasticsearch is running.

### Services started:
1. Elasticsearch
2. Redis
3. Nginx
4. API


## Running the Unit and Integration Tests
They can be run as follows:
1. `cd backend-task-david/app`
2. `pipenv shell`
3. `pipenv install`
4. `cd ..`
2. `make test`

## Running Smoke Tests
This will start up the system in docker, and then once it's up it 
will ensure that a log can be sent, a user can authenticate, logs can
be queried and that the rate limiting kicks in.

They can be run as follows:
1. `cd backend-task-david/app`
2. `pipenv shell`
3. `pipenv install`
4. `cd ..`
2. `make test_smoke`
