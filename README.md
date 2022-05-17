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
- Create an image for kafka and Zookeeper with `docker compose up`. This may take a while. This will install the docker images as defined in `docker-compose.yml` (thanks to [time-series-kafka-demo](https://github.com/mtpatter/time-series-kafka-demo)!)
- Start a local python environment and type: `pip install -r requirements.txt`


## Checking if everything works

To test whether everything works, you can use the two scripts `producer.py` and `consumer.py`.

- Start streaming the data from your phone
- Start the kafka producer with `python producer.py --hostname ip:port` with the appropriate values.
- Start the kafka consumer with `python consumer.py`.

If everything works (and that maybe be not trivial) you should see the streamed data appearing both in the producer and consumer.

## What's next?

In the next days, I will develop the machinery to parse the data and polish them in a nice timeseries from which we can compute the GW signal emitted by your phone. This pipeline could be done with `faust` or maybe with `kafka` itself. Hopefully this should be the _easy_ part :)






