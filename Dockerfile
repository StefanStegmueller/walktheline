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
RUN git clone git://git.drogon.net/wiringPi
RUN cd wiringPi && ./build
RUN git clone https://github.com/miloyip/rapidjson.git
RUN cp -a /rapidjson/include/rapidjson /usr/local/include

CMD cd "BrickPi/Setup Files" && chmod +x install.sh && ./install.sh