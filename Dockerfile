FROM python:3.6-alpine3.7
#Copy all project files
COPY . /sabthrottle

#Set current directory
WORKDIR /sabthrottle

RUN \
  echo "** BRANCH: ${BRANCH} COMMIT: ${COMMIT} **" && \
  echo "** Upgrade all packages **" && \
  apk --no-cache -U upgrade && \
  echo "** Install PIP dependencies **" && \
  pip install --no-cache-dir --upgrade pip setuptools && \
  pip install --no-cache-dir --upgrade -r /sabthrottle/requirements.txt

ENTRYPOINT [ "python", "./throttle.py" ]
