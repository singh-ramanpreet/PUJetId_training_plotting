#!/bin/bash

DIR=$( dirname "${BASH_SOURCE[0]}" )

cd $DIR

source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

export PYTHONUSERBASE=`pwd`

PY_VER=`python -c "import sys; print('python{0}.{1}'.format(*sys.version_info))"`

export PYTHONPATH=$PYTHONUSERBASE/lib/$PY_VER/site-packages:$PYTHONPATH

PATH=$PYTHONUSERBASE/bin:$PATH

echo "now installing pip pkgs"

#pip install --user --upgrade pip

if [ ! -d pyroot_cms_scripts ]; then
    git clone https://github.com/singh-ramanpreet/pyroot_cms_scripts.git --quiet
    cd pyroot_cms_scripts
    git checkout 0.1
    pip install --user .
    cd ..
fi

cd -

