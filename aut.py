import logging
import re
import pymqi

logging.basicConfig(level=logging.INFO)

#test settings
queue_manager = 'TESTQM_WCS'
channel = 'CLOUD.APP.SVRCONN'
host = 'testqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
port = '31075'
#host = 'perfqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
#port = '31510'

users = ['cogtestsoa', 'mqreader', 'mqwriter', 'mqtestuser',]
#DR settings
queue_manager = 'PRODQM_WCS'
host = 'prodqm-wcs-9fbb.qm.aws-eu-west-1.mq.appdomain.cloud'
port = '32459'

#PRD settings
queue_manager = 'PRODQM_WCS'
#host = 'prodqm-wcs-0f87.qm2.eu-gb.mq.appdomain.cloud'
#port = '30112'

conn_info = '%s(%s)' % (host, port)

ssl_cipher_spec = 'TLS_RSA_WITH_AES_256_CBC_SHA'
key_repo_location = '/home/ec2-user/key'


#user = 'mqtestuser'
#password = 'eiz8M9rzDlXFmyTlJ8a8ul5_RZfkeO5TyiKVe4xkh-Qt'

user = 'mmoreira'
password = 'FRwPWuJvMlunGghyr7PnhGyy46npSDRzanaQLTzZmzNd'

prefix = '*'
queue_type = pymqi.CMQC.MQQT_LOCAL

args = {pymqi.CMQC.MQCA_Q_NAME: prefix,
        pymqi.CMQC.MQIA_Q_TYPE: queue_type}

#args = {pymqi.CMQC.MQCA_Q_NAME: prefix}
qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

pcf = pymqi.PCFExecute(qmgr)

response = pcf.MQCMD_INQUIRE_Q(args)

try:
    response = pcf.MQCMD_INQUIRE_Q(args)
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
        logging.info('No queues matched given arguments.')
    else:
        raise
else:
    #print response
    for queue_info in response:
        queue_name = queue_info[pymqi.CMQC.MQCA_Q_NAME]

        if (re.match('^SYSTEM', queue_name) or re.match('^AMQ', queue_name) or re.match('^MQ', queue_name)):
            pass
        #logging.info('Found queue `%s`' % queue_name)
        else:
            for u in users:
                print 'dspmqaut -m ' + queue_manager + ' -n ' + queue_name + ' -t q -p ' 
 
qmgr.disconnect()
