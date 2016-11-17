FROM ubuntu:latest
MAINTAINER Ryszard Cetnarski "cetnarski.ryszard@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libpq-dev libncurses5-dev lib32ncurses5-dev python-tk
COPY . /allegro_project
WORKDIR /allegro_project
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]