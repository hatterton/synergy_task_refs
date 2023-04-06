# Synergy test task about refs

## Requirements
* Docker
* Make


## Running

To build container:
```bash
make build
```

Before running you may open `.envfile` and setup path to json file with test's refs with `USER_GRAPH_DATA_PATH`.

To run project enter:
```
make run
```

Project will be uped on `127.0.0.1:8000` with docker.

## API

* `/refs/<user_id>` - all information about user
    * `pk` - a user primary key
    * `ref_level` - level of a user in a referal system
    * `team_size` - size of a user's team
    * `balance` - amount of money after adding 120 to all users and all ref-payments

* `/refs/` - all information about all user - the same as previous but for all user. Be careful

## Tests

There are a few [tests](/src/synergy_refs/refs/tests.py) which can be run with:
```
make tests
```
