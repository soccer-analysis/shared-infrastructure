FROM amazon/aws-lambda-python:3.9

COPY install-browsers.sh /tmp/
RUN yum install xz atk cups-libs gtk3 libXcomposite alsa-lib tar \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel unzip bzip2 -y -q
RUN chmod +x /tmp/install-browsers.sh && /tmp/install-browsers.sh

RUN pip install --user --upgrade pip
RUN pip install pipenv
COPY Pipfile .
RUN pipenv lock --clear
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
COPY src/ ${LAMBDA_TASK_ROOT}/src
