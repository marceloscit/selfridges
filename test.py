import logging
import pymqi
from pymqi import CMQC
from pymqi import CMQCFC
import argparse
import sys
import os

logging.basicConfig(level=logging.INFO)

# Readme first - this code retrieve all queued from  a queue manager, connecting with or without tls. It retrieves most important settings
# to be compared between envs
# Env Settings, uncomment accordingly
 
parser = argparse.ArgumentParser(description="Inquire and print Queue parameters from a queue manager",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-e", "--environment", help="valid values TST, DR or PRD", nargs='?', default='DR')
parser.add_argument("-u", "--user", help="user")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-q", "--queuemanager", help="Queue manager to enquire", nargs='?', default="CMPRODQM_WCS")
parser.add_argument("-c", "--channel", help="Channel to enquire", nargs='?', default="CLOUD.APP.SVRCONN")
parser.add_argument("-f", "--full", help="full parameter list", action='store_true')
parser.add_argument("-t", "--tls", help="disable tls", action="store_false")
args = parser.parse_args()

if(args.environment == 'DR'):
    host = 'prodqm-wcs-9fbb.qm.aws-eu-west-1.mq.appdomain.cloud'
    port = '32028'
    queue_manager = 'CMPRODQM_WCS'
elif(args.environment == 'PRE'):
    host = 'cmprepqm-wcs-0f87.qm2.eu-gb.mq.appdomain.cloud'
    port = '31510'
    queue_manager = 'PREPQM_WCS'
elif(args.environment == 'PRD'):
    host = 'prodqm-wcs-0f87.qm2.eu-gb.mq.appdomain.cloud'
    port = '30112'
    queue_manager = 'PRODQM_WCS'    
elif(args.environment == 'TST'):
    host = 'testqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
    port = '31075'
    queue_manager = 'TESTQM_WCS'
elif(args.environment == 'D02'):
    host = 'sdevqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
    port = '31466'
    queue_manager = 'SDEVQM_WCS'
        
else:
    print("Invalid environment")
    sys.exit()

channel = args.channel


conn_info = '%s(%s)' % (host, port)

#cipher acepted by ibm cloud TLS 1.2 or Higher
#ref https://www.ibm.com/docs/en/ibm-mq/9.0?topic=jms-tls-cipherspecs-ciphersuites-in-mq-classes
ssl_cipher_spec = 'TLS_RSA_WITH_AES_256_CBC_SHA256'
key_repo_location = os.getenv('HOME') + '/key'

user = args.user
password = args.password


#Bellow code official reference
#Pymqi
#https://dsuch.github.io/pymqi/index.html#

#Ibm cloud developer example on how to use pymq
#https://developer.ibm.com/tutorials/mq-secure-msgs-tls/

prefix = '*'
queue_type = pymqi.CMQC.MQQT_LOCAL

inquire_args = {pymqi.CMQC.MQCA_Q_NAME: prefix,
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
if(args.tls):
    qmgr = pymqi.QueueManager(None)
    qmgr.connect_with_options(queue_manager, user = user, password = password, cd=cd, sco=sco)
else:
    #NO SSL
    qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

pcf = pymqi.PCFExecute(qmgr)

response = pcf.MQCMD_INQUIRE_Q(inquire_args)

pcf = pymqi.PCFExecute(qmgr)

auth_args = {pymqi.CMQCFC.MQIACF_AUTH_OPTIONS: pymqi.CMQCFC.MQAUTHOPT_ENTITY_EXPLICIT + 
pymqi.CMQCFC.MQAUTHOPT_NAME_ALL_MATCHING + CMQCFC.MQAUTHOPT_NAME_AS_WILDCARD, 
pymqi.CMQCFC.MQCACF_AUTH_PROFILE_NAME: '*', 
pymqi.CMQCFC.MQIACF_OBJECT_TYPE: CMQC.MQOT_Q, 
pymqi.CMQCFC.MQCACF_ENTITY_NAME: 'CLOUD.ADMIN.SVRCONN', 
pymqi.CMQCFC.MQIACF_ENTITY_TYPE: pymqi.CMQZC.MQZAET_PRINCIPAL, 
pymqi.CMQCFC.MQIACF_AUTH_PROFILE_ATTRS: pymqi.CMQCFC.MQIACF_ALL} 

authrec_response = pcf.MQCMD_INQUIRE_AUTH_RECS(auth_args) 
print(authrec_response)

for queue_authrec_info in authrec_response: 
    profile_name = queue_authrec_info[pymqi.CMQCFC.MQCACF_AUTH_PROFILE_NAME].decode('utf-8') 
    if 'SYSTEM' not in profile_name: 
        print('queue_authrec_info = ',queue_authrec_info, '\n')

qmgr.disconnect()
