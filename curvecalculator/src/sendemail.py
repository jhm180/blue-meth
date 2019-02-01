import utils as utils
from datetime import datetime

receiver_email = "whitepinedvt@gmail.com"  # Enter receiver address
message = """\
Subject: Message from INSIDE the container!

YOUR CONTAINER IS RUNNING."""


#shut down instance and email response to white pine dvt
# git merge test 
# merge test 2
# merge test 3
utils.send_email(receiver_email, message)

