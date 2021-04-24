FROM python:3.8-slim-buster
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r ./requirements.txt
COPY ./src ./
CMD [ "python3", "app.py"]