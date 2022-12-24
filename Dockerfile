FROM python:3.10

ARG TZ=Asia/Taipei

WORKDIR /workspace
COPY . /workspace

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -qq graphviz graphviz-dev

RUN pip install -r requirements.txt

CMD ["python3", "server.py"]
