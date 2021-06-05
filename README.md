# Near Earth Objects (Python Udacity Nanodegree)
### Overview
In this project, a command-line tool is implemented to inspect and query a data-set of NEOs and their close approaches to Earth.

First, the data is read from both a CSV file and a JSON file. Then, it is converted into structured Python objects. Based on the query or the inspection of the user, filtering operations are performed on the data and the result(full or limited size) is either printed or written into a file in a structured format, such as CSV or JSON.

This project adheres to pycode, pydoc and PEP257.

##### Available Filters
- Occurs on a given date.
- Occurs on or after a given start date.
- Occurs on or before a given end date.
- Approaches Earth at a distance of at least (or at most) X astronomical units.
- Approaches Earth at a relative velocity of at least (or at most) Y kilometers per second.
- Has a diameter that is at least as large as (or at least as small as) Z kilometers.
- Is marked by NASA as potentially hazardous (or not).


### Testing
#### Manually
```
# Query for close approaches on 2020-01-01
$ python3 main.py query --date 2020-01-01

# Query for close approaches in 2020.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31

# Query for close approaches in 2020 with a distance of <=0.1 au.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --max-distance 0.1

# Query for close approaches in 2020 with a distance of >=0.3 au.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --min-distance 0.3

# Query for close approaches in 2020 with a velocity of <=50 km/s.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --max-velocity 50

# Query for close approaches in 2020 with a velocity of >=25 km/s.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --min-velocity 25

# Query for close approaches of not potentially-hazardous NEOs between 500m and 600m in diameter.
$ python3 main.py query --min-diameter 0.5 --max-diameter 0.6 --not-hazardous

# Query for close approaches of potentially-hazardous NEOs larger than 2.5km passing within 0.1 au at a speed of at least 35 km/s
$ python3 main.py query --max-distance 0.1 --min-velocity 35 --min-diameter 2.5 --hazardous
```
#### Unit Testing
```
python3 -m unittest -v
```

#### Project Tree

```
.
├── data
│   ├── cad.json
│   └── neos.csv
├── helpers.py
├── Information.md
├── LICENSE
├── main.py
├── neo
│   ├── database.py
│   ├── extract.py
│   ├── filters.py
│   ├── __init__.py
│   └── models.py
├── README.md
├── tests
│   ├── __init__.py
│   ├── test-cad-2020.json
│   ├── test_database.py
│   ├── test_data_files.py
│   ├── test_extract.py
│   ├── test_limit.py
│   ├── test-neos-2020.csv
│   ├── test_python_version.py
│   ├── test_query.py
│   └── test_write.py
└── write.py

```
