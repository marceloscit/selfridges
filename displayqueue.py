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

#DR settings
queue_manager = 'PRODQM_WCS'
host = 'prodqm-wcs-9fbb.qm.aws-eu-west-1.mq.appdomain.cloud'
port = '32459'

#PRD settings
queue_manager = 'PRODQM_WCS'
host = 'prodqm-wcs-0f87.qm2.eu-gb.mq.appdomain.cloud'
port = '30112'

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
            print 'Foundqueue,`%s`' % queue_name
            print queue_name+'->MQCA_Q_DESC,%s' % queue_info[pymqi.CMQC.MQCA_Q_DESC]
            print '---more important ----'
            print queue_name+'->MQIA_DEF_INPUT_OPEN_OPTION,%s' % queue_info[pymqi.CMQC.MQIA_DEF_INPUT_OPEN_OPTION]
            print queue_name+'->MQIA_DEF_PERSISTENCE,%s' % queue_info[pymqi.CMQC.MQIA_DEF_PERSISTENCE]
            print queue_name+'->MQIA_SHAREABILITY,%s' % queue_info[pymqi.CMQC.MQIA_SHAREABILITY]
            print queue_name+'->MQIA_INHIBIT_GET,%s' % queue_info[pymqi.CMQC.MQIA_INHIBIT_GET]
            print queue_name+'->MQIA_INHIBIT_PUT,%s' % queue_info[pymqi.CMQC.MQIA_INHIBIT_PUT]
            print queue_name+'->MQIA_MAX_Q_DEPTH,%s' % queue_info[pymqi.CMQC.MQIA_MAX_Q_DEPTH]
            print '---others---'
            print queue_name+'->MQIA_ACCOUNTING_Q,%s' % queue_info[pymqi.CMQC.MQIA_ACCOUNTING_Q ]
            print queue_name+'->MQCA_CLUSTER_NAME %s ' % queue_info[pymqi.CMQC.MQCA_CLUSTER_NAME]
            print queue_name+'->MQIA_CURRENT_Q_DEPTH ,%s' % queue_info[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]
            print queue_name+'->MQIA_DEF_PUT_RESPONSE_TYPE,%s' % queue_info[pymqi.CMQC.MQIA_DEF_PUT_RESPONSE_TYPE]
            print queue_name+'->MQIA_DEF_READ_AHEAD,%s' % queue_info[pymqi.CMQC.MQIA_DEF_READ_AHEAD]
            print queue_name+'->MQIA_DEFINITION_TYPE,%s' % queue_info[pymqi.CMQC.MQIA_DEFINITION_TYPE]
            print queue_name+'->MQIA_DIST_LISTS,%s' % queue_info[pymqi.CMQC.MQIA_DIST_LISTS]
            print queue_name+'->MQIA_HARDEN_GET_BACKOUT,%s' % queue_info[pymqi.CMQC.MQIA_HARDEN_GET_BACKOUT]
            print queue_name+'->MQIA_MAX_MSG_LENGTH,%s' % queue_info[pymqi.CMQC.MQIA_MAX_MSG_LENGTH]
            print queue_name+'->MQIA_MONITORING_Q,%s' % queue_info[pymqi.CMQC.MQIA_MAX_Q_DEPTH]
            print queue_name+'->MQIA_MSG_DELIVERY_SEQUENCE,%s' % queue_info[pymqi.CMQC.MQIA_MAX_Q_DEPTH]
            print queue_name+'->MQIA_NPM_CLASS,%s' % queue_info[pymqi.CMQC.MQIA_NPM_CLASS]
            print queue_name+'->MQIA_OPEN_INPUT_COUNT,%s' % queue_info[pymqi.CMQC.MQIA_OPEN_INPUT_COUNT]
            print queue_name+'->MQIA_OPEN_OUTPUT_COUNT,%s' % queue_info[pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT]
            print queue_name+'->MQIA_PROPERTY_CONTROL,%s' % queue_info[pymqi.CMQC.MQIA_PROPERTY_CONTROL]
            print queue_name+'->MQIA_Q_DEPTH_HIGH_EVENT,%s' % queue_info[pymqi.CMQC.MQIA_Q_DEPTH_HIGH_EVENT]
            print queue_name+'->MQIA_Q_DEPTH_HIGH_LIMIT,%s' % queue_info[pymqi.CMQC.MQIA_Q_DEPTH_HIGH_LIMIT]
            print queue_name+'->MQIA_Q_DEPTH_LOW_EVENT,%s' % queue_info[pymqi.CMQC.MQIA_Q_DEPTH_LOW_EVENT]
            print queue_name+'->MQIA_Q_DEPTH_LOW_LIMIT,%s' % queue_info[pymqi.CMQC.MQIA_Q_DEPTH_LOW_LIMIT]
            print queue_name+'->MQIA_Q_DEPTH_MAX_EVENT,%s' % queue_info[pymqi.CMQC.MQIA_Q_DEPTH_MAX_EVENT]
            print queue_name+'->MQIA_Q_SERVICE_INTERVAL,%s' % queue_info[pymqi.CMQC.MQIA_Q_SERVICE_INTERVAL]
            print queue_name+'->MQIA_Q_TYPE,%s' % queue_info[pymqi.CMQC.MQIA_Q_TYPE]
            print queue_name+'->MQIA_RETENTION_INTERVAL,%s' % queue_info[pymqi.CMQC.MQIA_RETENTION_INTERVAL]
            print queue_name+'->MQIA_SCOPE,%s' % queue_info[pymqi.CMQC.MQIA_SCOPE]
            print queue_name+'->MQIA_STATISTICS_Q,%s' % queue_info[pymqi.CMQC.MQIA_STATISTICS_Q]
            print queue_name+'->MQIA_TRIGGER_DEPTH,%s' % queue_info[pymqi.CMQC.MQIA_TRIGGER_DEPTH]
            print queue_name+'->MQIA_TRIGGER_MSG_PRIORITY,%s' % queue_info[pymqi.CMQC.MQIA_TRIGGER_MSG_PRIORITY]
            print queue_name+'->MQIA_USAGE,%s' % queue_info[pymqi.CMQC.MQIA_USAGE]
            print '----end-----'

qmgr.disconnect()
