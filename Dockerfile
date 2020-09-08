FROM python:3.8

# create the app folder
RUN mkdir -p /app

# make it as working directory
WORKDIR /app

# copy requirements.txt to the current working directory
COPY requirements.txt ./

# execute the pip install
RUN pip install --no-cache-dir -r requirements.txt


# copy the content of the current directory to the working directory
COPY . .

CMD [ "python" ]