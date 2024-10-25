FROM alpine:3.11

WORKDIR /tmp

RUN apk --no-cache add python ffmpeg tzdata bash python3 \
&& apk --no-cache add --virtual=builddeps autoconf automake libtool git ffmpeg-dev wget tar build-base \
&& wget http://prdownloads.sourceforge.net/argtable/argtable2-13.tar.gz \
&& tar xzf argtable2-13.tar.gz \
&& cd argtable2-13/ && ./configure && make && make install \
&& cd /tmp && git clone https://github.com/erikkaashoek/Comskip \
&& cd Comskip && ./autogen.sh && ./configure && make && make install \
&& apk del builddeps \
&& rm -rf /var/cache/apk/* /tmp/* /tmp/.[!.]*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY webserver.py .

ADD https://gist.githubusercontent.com/vdrover/af5a7e6e38aff14c4ab86db1fee327b5/raw/7bdfdefbafd8de7d916958316f99324dc01a5f6e/comskip.ini .

RUN ["python3", "webserver.py"]