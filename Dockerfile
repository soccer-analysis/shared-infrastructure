ARG CHROMEDRIVER_DIR="/chromedriver"

# setup chromedriver
FROM ubuntu:18.04
ARG CHROMEDRIVER_DIR
RUN apt-get update -y && apt-get install -y wget xvfb unzip gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y && apt-get install -y google-chrome-stable
RUN mkdir $CHROMEDRIVER_DIR
ENV CHROMEDRIVER_VERSION 112.0.5615.28
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

FROM amazon/aws-lambda-python:3.9
ARG CHROMEDRIVER_DIR
COPY --from=0 $CHROMEDRIVER_DIR $CHROMEDRIVER_DIR
ENV PATH $CHROMEDRIVER_DIR:$PATH
COPY Pipfile .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv lock --clear
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
COPY src/ ${LAMBDA_TASK_ROOT}/src
RUN ls -l $CHROMEDRIVER_DIR