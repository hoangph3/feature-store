## Feature Store demo with Mnist dataset

1. Deploy:
```sh
make start
```

2. Produce logs to kafka:
```sh
make produce
```

3. Sink jobs:
```sh
make sink
```

4. Access the UI:
* [Kafdrop ui](http://localhost:9000)
* [Transformations spark ui](http://localhost:4040/StreamingQuery)
* [Mongodb ui](http://localhost:8081)
* [Redis ui](http://localhost:8082)

5. Clean:
```sh
make clean
```