FROM python:latest

COPY . /usr/src/genetic_maze_generator

WORKDIR /usr/src/genetic_maze_generator

RUN pip install -r requirements.txt

CMD ["python", "GenAlg.py"]