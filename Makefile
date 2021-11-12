
# build docker image with python app inside

build:
	docker build -t gapp .

# run docker container image
run:
	docker run -it gapp -s btcusd -t all -p 10

# all in one,  both build and run
all: build run
