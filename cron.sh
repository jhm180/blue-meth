#!/bin/bash
source ~/env/pydata/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/oliver/Dropbox/whitepine/lib;
export PATH=/home/oliver/bin:/home/oliver/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/go/bin:/home/oliver/src/julia/usr/bin:/home/oliver/bin:/home/oliver/android_sdk/platform-tools:/home/oliver/android_sdk/tools:/usr/local/go/bin:/home/oliver/src/julia/usr/bin:/home/oliver/bin:/home/oliver/android_sdk/platform-tools:/home/oliver/android_sdk/tools:/usr/local/go/bin:/home/oliver/src/julia/usr/bin:/home/oliver/bin:/home/oliver/android_sdk/platform-tools:/home/oliver/android_sdk/tools
export PYTHONPATH=$PYTHONPATH:/home/oliver/Dropbox/whitepine/lib;
date
ulimit -d unlimited
ulimit -m unlimited
ulimit -s unlimited
/home/oliver/bin/wpcmd import
#python /home/oliver/src/blue-meth/ipynb/rapnet_loader.py
date
#python /home/oliver/Dropbox/whitepine/lib/cron.py
#date
python /home/oliver/Dropbox/whitepine/lib/newcron.py
date
