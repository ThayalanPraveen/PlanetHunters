# A dockerfile must always start by importing the base image.
# We use the keyword 'FROM' to do that.
# In our example, we want import the python image.
# So we write 'python' for the image name and 'latest' for the version.
# do this to get the latest version of docker

#### Follow these instructions ###
# go to UI_Test folder in the terminal
# docker pull python
# $ docker build -t planethunters . 

# try this :
# $ docker run planethunters

# if error try this :
# chmod +x ./run.sh
# ./run.sh

FROM python:latest

RUN pip install lightkurve
RUN pip install tk
RUN pip install PySimpleGUI
RUN pip install matplotlib==3.4


# In order to launch our python code, we must import it into our image.
# We use the keyword 'COPY' to do that.
# The first parameter 'main.py' is the name of the file on the host.
# The second parameter '/' is the path where to put the file on the image.
# Here we put the file at the image root folder.

COPY main.py /

# We need to define the command to launch when we are going to run the image.
# We use the keyword 'CMD' to do that.
# The following command will execute "python ./main.py".

CMD [ "python", "./main.py" ]


