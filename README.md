# Tails Python Coding Test

## Instructions for running the application

### installs the dependencies based on the requirements file

```
make restore
```

### Code style. To run pylint

```
make lint
```

### To run unit tests

```
make test
```

### Complete unit testing. To run both Lint and unit test

```
make check
```

### To run the application

```
make run
```

### Help

```
make help
```

## URLs to access application

### To display complete store list with latitude and longitude

```
http://localhost:5000/tails/stores
```

### To display stores within radius of 25 km from Reading

```
http://localhost:5000/tails/stores_in_radius?radius=25&store_name=Reading
```

### To display stores within 15 km radius from Hatfield

```
http://localhost:5000/tails/stores_in_radius?radius=15&store_name=Hatfield
```
