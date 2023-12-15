# Explanation of scripts

`aws_secret_scraper.py` -- scrapes aws secrets and uses regex patterns to replace values

`clean_up.py` -- cleans up the files in a said directory into their appropiate file types

`new_stop_ec2.py` -- stops an ec2 instance ( does not terminate ) or starts an instance

`start_rds.py` -- starts or stops an rds instance 

`get_kube_ami.py` -- gets the latest ami, linux or windows, checks if theres a diff and outputs