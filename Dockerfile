FROM resin/rpi-raspbian:jessie

ENV INITSYSTEM on

# Install dependencies
RUN apt-get update && apt-get install -y \
    git-core \
    build-essential \
    gcc \
    python \
    python-dev \
    python-pip \
    python-virtualenv \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*


# RUN  apt-get install python-serial
# RUN  apt-get install python-rpi.gpio

RUN pip install pyserial
RUN git clone git://git.drogon.net/wiringPi
RUN cd wiringPi && ./build
RUN pip install wiringpi2

RUN pip install Brickpi
RUN pip install web.py

RUN git clone https://github.com/DexterInd/BrickPi_Python.git


COPY config.txt /boot/
COPY ir_receiver_check.py /BrickPi_Python/Sensor_Examples/ 
COPY BrickPi.py /BrickPi_Python/Sensor_Examples/

# Brickpi LED test file
COPY docker-LED-test/*.py /BrickPi_Python/Sensor_Examples/


# Define working directory
WORKDIR /data
VOLUME /data

# This command turns on the LED
CMD python /BrickPi_Python/Sensor_Examples/pi-brickpi-soundintensity-threshold-breach-indicator.py