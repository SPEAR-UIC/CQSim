FROM fedora:40

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN dnf install -y ncurses python3-pip python3-pandas python3-tqdm python3-plotly

RUN dnf install -y unzip

RUN pip3 install dash

RUN pip3 install kaleido

COPY . /cqsimplus

WORKDIR /cqsimplus