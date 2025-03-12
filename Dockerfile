FROM fedora:40

RUN dnf install -y ncurses python3-pip python3-pandas python3-tqdm python3-plotly

RUN pip3 install dash

RUN pip3 install kaleido

COPY . /cqsimplus

WORKDIR /cqsimplus

ENTRYPOINT ["/cqsimplus/container_entry.sh"] 
