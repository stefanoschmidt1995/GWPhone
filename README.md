# How does this work

This repo host the software to stream the sensor data from your phone to your computer. These will be used eventually to plot in real time the gravitational waves signal that your moving phone emits.

Below is some notes on what I've done so far

## Stream data from your phone

You will need the Android App [SensorStream](https://github.com/yaqwsx/SensorStreamer).

Once it's installed in you phone, you need to configure it by specifying:

- A **connection**: this configure the client or server socket to stream the data. You want to choose a server on your favourite port. Make sure that you know your phone IP address as it will be used for later
- A **packet**: this specify which data will be streamed. You just need to stream the accelerometer data and to include the timestamps. Make sure to choose the JSON format

## Install kafka

This is the most tricky part. Luckily, after some digging, I found a nice [repo](https://github.com/mtpatter/time-series-kafka-demo) that tells you how to do that.
It is related to this nice [article](https://towardsdatascience.com/make-a-mock-real-time-stream-of-data-with-python-and-kafka-7e5e23123582): it basically creates a docker image with `kafka` and `Zookeeper`. This does all the magic for you and allows for the whole thing to work.

In details, you can follows this steps:

- Install [`docker`](https://docs.docker.com/engine/install/)
- Create an image for kafka and Zookeeper with `docker compose up --build`. This may take a while. This will install the docker images as defined in `docker-compose.yml` (thanks to [time-series-kafka-demo](https://github.com/mtpatter/time-series-kafka-demo)!)
- Start a local python environment and type: `pip install -r requirements.txt`

## Dealing with Docker

This is another tricky part!

The command `docker compose up` creates and _starts_ the containers specified in the `docker-compose` file. The option `--build` will be needed to build the images (downloading them if required), before doing the actual container creation. This command is equivalent to an installation of the kafka+zookeeper code. It will create two containers, which are the item that actually execute the software, and it will _activate_ it. (still shady why it takes so long for no reason... do we see logs? or are we just stopping the installation?)

The available images can be listed with `docker image ls`. The available _containers_ (built from images) are listed with `docker container ls`. You need to make sure you have two containers running before moving forward: one for zookeeper and another one for kafka.

In short, `docker compose` is a way to manage with a single interface several containers that needs to be together (in our case, kafka and zookeeper). It is based on the `docker-compose` file, which defines the environment: this file must be in the same folder you're working on. You can check this with `docker compose ls`, which lists the compose set being running: you should see one named after the directory of your `docker-compose`.

To stop the execution of the docker compose, you need to type `docker compose stop`: this will shut down the two containers you have previously created.
To start the execution of the environment just type:
```
docker compose start
```

Of course, you could also stop the two containers by hand with `docker container stop [CONTAINER ID]`, where `[CONTAINER ID]` is listed by `docker container ls`.
Clearly, stopping the two containers is equivalent to `docker compose stop`.


## Checking if everything works

To test whether everything works, you can use the two scripts `producer.py` and `consumer.py`.

- Start the compose enviroment (i.e. the required containers) with `docker compose start`.
- Start streaming the data from your phone
- Start the kafka producer with `python producer.py --hostname ip:port` with the appropriate values.
- Start the kafka consumer with `python consumer.py`.

If everything works (and that maybe be not trivial) you should see the streamed data appearing both in the producer and consumer.

## What's next?

In the next days, I will develop the machinery to parse the data and polish them in a nice timeseries from which we can compute the GW signal emitted by your phone. This pipeline could be done with `faust` or maybe with `kafka` itself. Hopefully this should be the _easy_ part :)






