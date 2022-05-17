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
It is related to this nice [article](https://towardsdatascience.com/make-a-mock-real-time-stream-of-data-with-python-and-kafka-7e5e23123582): it basically creates a docker image with `kafka` and `Zookeeper`. This does all the magin for you and allows for the whole thing to work.

In details, you can follows this steps:

- Install [`docker`](https://docs.docker.com/engine/install/)
- Create an image for kafka and Zookeeper with `docker compose up`. This may take a while
- Start a local python environment and type: `pip install -r requirements.txt`




