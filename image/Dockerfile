FROM ubuntu
RUN apt-get -y --fix-missing update
RUN apt-get install -y curl vim unzip telnet netcat net-tools

#RUN apt-get -y -qq update && \
#	apt-get install -y -qq curl && \
#	apt-get clean
#RUN curl -o /usr/local/bin/jq http://stedolan.github.io/jq/download/linux64/jq && \
#  chmod +x /usr/local/bin/jq

#RUN DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql
RUN apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN python3 -m pip install pg8000
#RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#RUN unzip awscliv2.zip
#RUN ./aws/install
#RUN mkdir /root/.aws
#COPY config /root/.aws
#RUN curl -f -s -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
#    chmod +x /usr/local/bin/kubectl && \
#    kubectl version --client
ADD start-srv.py /start-srv.py
RUN chmod +x /start-srv.py
ADD start-cli.sh /start-cli.sh
RUN chmod +x /start-cli.sh
