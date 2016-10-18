FROM resin/rpi-raspbian:jessie

ENV INITSYSTEM on

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get -y update && apt-get install -y \
git-core \
build-essential \
python-dev \
python-pip \
libi2c-dev

RUN pip install pyserial
RUN git clone https://github.com/DexterInd/BrickPi.git
RUN cd "BrickPi/Setup Files"
RUN chmod +x install.sh
RUN ./install.sh
RUN git clone git://git.drogon.net/wiringPi
RUN cd wiringPi && ./build
RUN git clone https://github.com/miloyip/rapidjson.git
RUN cp -a /rapidjson/include/rapidjson /usr/local/include

#CMD modprobe i2c-dev && chmod +x runApp.sh && ./runApp.sh