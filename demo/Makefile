start:
	docker-compose up -d --build

build-producer:
	docker build -f producer/Dockerfile -t mnist-producer:latest producer

produce: build-producer
	docker run --rm --network=host --name=mnist_producer mnist-producer:latest \
	--filepath data/mnist.npz \
	--entity mnist \
	--limit 10000

stop:
	docker-compose down

clean: stop
	docker container prune && docker network prune && docker volume prune
