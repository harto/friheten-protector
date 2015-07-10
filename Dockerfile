FROM ubuntu:14.10

RUN apt-get update && \
    apt-get install -y build-essential \
                       cmake \
                       git \
                       libgtk2.0-dev \
                       pkg-config \
                       libavcodec-dev \
                       libavformat-dev \
                       libswscale-dev \
                       unzip

RUN curl -L -o /tmp/opencv.zip http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/3.0.0/opencv-3.0.0.zip
RUN unzip -d /tmp /tmp/opencv.zip
RUN cd /tmp/opencv-3.0.0 && \
    mkdir release && \
    cd release && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local .. && \
    make && \
    make install
