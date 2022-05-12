FROM ubuntu:jammy

RUN apt-get update
RUN apt-get -y install python3 scour make inkscape graphicsmagick optipng pngquant python3-pip

RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone
RUN apt-get -y install python3-jinja2 nodejs wget curl
RUN wget https://npmjs.com/install.sh -O /tmp/install.sh && bash /tmp/install.sh
RUN npm install -g sass
#RUN pip3 install jinja2

RUN mkdir /code
WORKDIR /code

CMD make clean && make -j8 && make polished-site -j8
