import pymqi
from pymqi import CMQC
from pymqi import CMQCFC


#test settings
queue_manager = 'TESTQM_WCS'
channel = 'CLOUD.APP.SVRCONN'
host = 'testqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
port = '31075'
#host = 'perfqm-wcs-9fbb.qm2.eu-de.mq.appdomain.cloud'
#port = '31510'

#DR settings
queue_manager = 'PRODQM_WCS'
host = 'prodqm-wcs-9fbb.qm.aws-eu-west-1.mq.appdomain.cloud'
port = '32459'


conn_info = '%s(%s)' % (host, port)

ssl_cipher_spec = 'TLS_RSA_WITH_AES_256_CBC_SHA'
key_repo_location = '/home/ec2-user/key'


inq_user = 'mqtestuser'
#password = 'eiz8M9rzDlXFmyTlJ8a8ul5_RZfkeO5TyiKVe4xkh-Qt'

user = 'mmoreira'
password = 'FRwPWuJvMlunGghyr7PnhGyy46npSDRzanaQLTzZmzNd'
""" 
qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password)

pcf = pymqi.PCFExecute(qmgr)

auth_args = {CMQCFC.MQIACF_AUTH_OPTIONS:  CMQCFC.MQAUTHOPT_NAME_ALL_MATCHING + CMQCFC.MQAUTHOPT_ENTITY_EXPLICIT +CMQCFC.MQAUTHOPT_NAME_AS_WILDCARD,
                      CMQCFC.MQCACF_AUTH_PROFILE_NAME: "*",
                      CMQCFC.MQIACF_OBJECT_TYPE: CMQC.MQOT_ALL}

auth_args = {}
auth_args[CMQCFC.MQIACF_AUTH_OPTIONS] =  CMQCFC.MQAUTHOPT_ENTITY_EXPLICIT + CMQCFC.MQAUTHOPT_NAME_ALL_MATCHING
auth_args[CMQCFC.MQCACF_AUTH_PROFILE_NAME ] = "*"
auth_args[CMQCFC.MQIACF_OBJECT_TYPE] =  CMQC.MQOT_Q

response = pcf.MQCMD_INQUIRE_AUTH_RECS(auth_args)

qmgr.disconnect()
 """