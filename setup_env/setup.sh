#!/bin/bash

DIR=$( dirname "${BASH_SOURCE[0]}" )
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh
export PYTHONUSERBASE=${DIR}
PY_VER=`python -c "import sys; print('python{0}.{1}'.format(*sys.version_info))"`
export PYTHONPATH=$PYTHONUSERBASE/lib/$PY_VER/site-packages:$PYTHONPATH
PATH=$PYTHONUSERBASE/bin:$PATH

if [[ ${1} == "--install" ]]
then
  echo "now installing pip pkgs"
  pip install git+git://github.com/singh-ramanpreet/pyroot_cms_scripts.git@0.3.1#egg=pyroot_cms_scripts
fi
