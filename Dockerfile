FROM alpine:3.11

WORKDIR /tmp

RUN apk --no-cache add python ffmpeg tzdata bash python3 \
&& apk --no-cache add --virtual=builddeps autoconf automake libtool git ffmpeg-dev wget tar build-base

ADD http://prdownloads.sourceforge.net/argtable/argtable2-13.tar.gz .
RUN tar xzf argtable2-13.tar.gz \
    && cd argtable2-13/ && ./configure && make && make install

WORKDIR /tmp
RUN git clone https://github.com/erikkaashoek/Comskip \
    && cd Comskip && ./autogen.sh && ./configure && make && make install \

RUN apk del builddeps \
    && rm -rf /var/cache/apk/* /tmp/* /tmp/.[!.]*

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY webserver.py .

COPY comskip.ini .

CMD ["python3", "webserver.py"]
