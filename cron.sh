#!/bin/bash
source ~/env/pydata/bin/activate
/home/oliver/bin/wpcmd import
python /home/oliver/src/blue-meth/ipynb/rapnet_loader.py
python /home/oliver/Dropbox/whitepine/lib/cron.py
