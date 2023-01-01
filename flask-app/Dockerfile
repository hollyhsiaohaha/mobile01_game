FROM python:3

# set a directory for the app
WORKDIR /code

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python3", "./app.py"]
