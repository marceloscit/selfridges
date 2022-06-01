import logging
import re
import pymqi

logging.basicConfig(level=logging.INFO)

# Readme first - this code retrieve all queued from  a queue manager, connecting with or without tls. It retrieves most important settings
# to be compared between envs
# Env Settings, uncomment accordingly

#TODO transform connection settings into parameter
#test environemt settings
#queue_manager = 'TESTQM_WCS'
#channel = 'CLOUD.APP.SVRCONN'
#host = 'testqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
#port = '31075'
#host = 'perfqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
#port = '31510'

#DR environment settings
channel = 'CLOUD.APP.SVRCONN'
queue_manager = 'CMPRODQM_WCS'
host = 'prodqm-wcs-9fbb.qm.aws-eu-west-1.mq.appdomain.cloud'
port = '32028'

#PRD environment settings
#queue_manager = 'CMPRODQM_WCS'
#host = 'cmprepqm-wcs-0f87.qm2.eu-gb.mq.appdomain.cloud'
#port = '30726'

conn_info = '%s(%s)' % (host, port)

#cipher acepted by ibm cloud TLS 1.2 or Higher
#ref https://www.ibm.com/docs/en/ibm-mq/9.0?topic=jms-tls-cipherspecs-ciphersuites-in-mq-classes
ssl_cipher_spec = 'TLS_RSA_WITH_AES_256_CBC_SHA256'
key_repo_location = '/home/ec2-user/key'

#user = 'mqtestuser'
#password = 'eiz8M9rzDlXFmyTlJ8a8ul5_RZfkeO5TyiKVe4xkh-Qt'

#TODO put it on secrets
user = '<MQ User admin display access for this case>'
password = '<ibm key>'


#Bellow code official reference
#Pymqi
#https://dsuch.github.io/pymqi/index.html#

#Ibm cloud developer example on how to use pymq
#https://developer.ibm.com/tutorials/mq-secure-msgs-tls/

prefix = '*'
queue_type = pymqi.CMQC.MQQT_LOCAL

args = {pymqi.CMQC.MQCA_Q_NAME: prefix,
        pymqi.CMQC.MQIA_Q_TYPE: queue_type}


cd = pymqi.CD()
cd.ChannelName = channel
cd.ConnectionName = conn_info
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP
cd.SSLCipherSpec = ssl_cipher_spec

sco = pymqi.SCO()
sco.KeyRepository = key_repo_location

#SSL connection
qmgr = pymqi.QueueManager(None)
qmgr.connect_with_options(queue_manager, user = user, password = password, cd=cd, sco=sco)
#NO SSL
#qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

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

        #skip system queues
        if (re.match('^SYSTEM', queue_name) or re.match('^AMQ', queue_name) or re.match('^MQ', queue_name)):
            pass
        #logging.info('Found queue `%s`' % queue_name)
        else:
            print (queue_name.strip()+'->MQCA_Q_DESC,%s' % queue_info[pymqi.CMQC.MQCA_Q_DESC])
            print (queue_name.strip()+'->MQIA_DEF_INPUT_OPEN_OPTION,%s' % queue_info[pymqi.CMQC.MQIA_DEF_INPUT_OPEN_OPTION])
            print (queue_name.strip()+'->MQIA_DEF_PERSISTENCE,%s' % queue_info[pymqi.CMQC.MQIA_DEF_PERSISTENCE])
            print (queue_name.strip()+'->MQIA_SHAREABILITY,%s' % queue_info[pymqi.CMQC.MQIA_SHAREABILITY])
            print (queue_name.strip()+'->MQIA_INHIBIT_GET,%s' % queue_info[pymqi.CMQC.MQIA_INHIBIT_GET])
            print (queue_name.strip()+'->MQIA_INHIBIT_PUT,%s' % queue_info[pymqi.CMQC.MQIA_INHIBIT_PUT])
            print (queue_name.strip()+'->MQIA_MAX_Q_DEPTH,%s' % queue_info[pymqi.CMQC.MQIA_MAX_Q_DEPTH])
           

qmgr.disconnect()
