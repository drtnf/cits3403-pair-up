# Pair Up!

A simple flask app for allocating student pairs in the [CITS3403 project](https://teaching.csse.uwa.edu.au/units/CITS3403/).

## Getting Started

Activate the python virtual environment:
`$source virtual-environment/bin/activate`

To run the app:
`$flask run`

To stop the app:
`$^C`

To exit the environment:
`$deactivate`

### Prerequisites

Requires python3, flask, venv, and sqlite

```
Give examples
```

### Installing

Install python3, sqlite3

1. Set up a virtual environment:
 - use pip or another package manager to install virtualenv package `pip install virtualenv`
 - start the provided virtual environment
   `source virtual-environment/bin/activate`
 - This should include flask and all the required packages
2. Install sqlite
 - [Windows instructions](http://www.sqlitetutorial.net/download-install-sqlite/)
 - In \*nix, `sudo apt-get install sqlite`
3. Build the database: `flask db init`
4. `flask run`

This should start the app running on localhost at port 5000, i.e. [http://localhost:5000/index](http://localhost:5000/index)

## Running the tests

A few tests now:

To run unit tests
`python -m tests.unittest`

To run selenium tests, make sure that you have the 
appropriate web driver installed. In this case it should be geckodriver for Firefox, 
and it assumes that it is installed in the test directory.
Then start the webserver in TestingConfig, and run
`python -m tests.systemtest`

## Deployment

via localhost

## Built With

vim and git

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

## Authors

* **Tim French** - *Initial work* - [drtnf](https://github.com/drtnf)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Built following the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by **Miguel Grinberg**.

