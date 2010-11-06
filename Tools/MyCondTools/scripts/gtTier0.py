#!/usr/bin/env python
import commands
from os import environ
#environ["http_proxy"]="http://cmsproxy.cms:3128"

if __name__ == "__main__":



    dasinfo = eval(commands.getoutput("wget -qO- 'http://vocms115.cern.ch:8304/tier0/express_config?run=&stream=Express'"))

    run = dasinfo[0]['run_id']
    globaltag = dasinfo[0]['global_tag']

    print "Express GT: " + globaltag
