# pull official base image
#FROM python:3.8.2-buster
FROM python:3.8.2-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV bCIRT_ROOT=/bCIRT/
ENV bCIRT_VIRTUAL_ENV_HOME=${bCIRT_ROOT}/venvs/
ENV bCIRT_VENV=django_venv
ENV bCIRT_VIRTUAL_ENV=${bCIRT_VIRTUAL_ENV_HOME}/$bCIRT_VENV
ENV bCIRT_HOME=/bCIRT/var/www/bCIRT/
ENV bCIRT_VENV_ACTIONS_v2=actions_v2
ENV bCIRT_VENV_ACTIONS_v3=actions_v3
ENV PATH="$bCIRT_VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR ${bCIRT_HOME}

# install psycopg2 dependencies
RUN apk update \
    && apk add nano postgresql-dev gcc python3-dev musl-dev \
    libffi-dev build-base py2-pip python2-dev

# create django home virtual environment
RUN mkdir -p ${bCIRT_VIRTUAL_ENV_HOME}
WORKDIR ${bCIRT_VIRTUAL_ENV_HOME}
RUN python3 -m venv ${bCIRT_VENV}

# install dependencies
RUN source $bCIRT_VIRTUAL_ENV/bin/activate && $bCIRT_VIRTUAL_ENV/bin/pip3 install --upgrade pip wheel

# wget https://github.com/bl305/bCIRT/raw/master/bCIRT_PackageReleases/0113_bCIRT_v203_20200418.zip
COPY ./requirements.txt ${bCIRT_HOME}/requirements.txt
RUN source $bCIRT_VIRTUAL_ENV/bin/activate && $bCIRT_VIRTUAL_ENV/bin/pip3 install --no-cache-dir -r ${bCIRT_HOME}/requirements.txt

# create actions virtual environments v3
RUN mkdir -p ${bCIRT_VIRTUAL_ENV_HOME}
RUN python3 -m venv ${bCIRT_VENV_ACTIONS_v3}
# install dependencies
RUN source ${bCIRT_VIRTUAL_ENV_HOME}/${bCIRT_VENV_ACTIONS_v3}/bin/activate && ${bCIRT_VIRTUAL_ENV_HOME}/${bCIRT_VENV_ACTIONS_v3}/bin/pip3 install --upgrade pip wheel

# # create actions virtual environments v2
# RUN apt install py2-virtualenv
# RUN mkdir -p ${bCIRT_VIRTUAL_ENV_HOME}
# #WORKDIR ${bCIRT_VIRTUAL_ENV_HOME}/${bCIRT_VENV_ACTIONS_v2}
# #RUN python2 -m venv ${bCIRT_VENV_ACTIONS_v2}
# RUN virtualenv ${bCIRT_VENV_ACTIONS_v2}
# # install dependencies
# RUN source ${bCIRT_VIRTUAL_ENV_HOME}/${bCIRT_VENV_ACTIONS_v2}/bin/activate && ${bCIRT_VIRTUAL_ENV_HOME}/${bCIRT_VENV_ACTIONS_v2}/bin/pip install --upgrade pip wheel


# copy entrypoint.sh
COPY ./entrypoint.sh ${bCIRT_HOME}/entrypoint.sh

# copy project
COPY . ${bCIRT_HOME}

WORKDIR ${bCIRT_HOME}

# run entrypoint.sh
ENTRYPOINT ["/bCIRT/var/www/bCIRT/entrypoint.sh"]
