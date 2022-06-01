import logging

import pymqi

logging.basicConfig(level=logging.INFO)

queue_manager = 'PRODQM_WCS'
channel = 'CLOUD.APP.SVRCONN'
host = 'prodqm-wcs-9fbb.qm.aws-eu-west-1.mq.appdomain.cloud'
port = '32459'
queue_name = 'LIVE_TO_WCS_SERIAL'
conn_info = '%s(%s)' % (host, port)
ssl_cipher_spec = 'TLS_RSA_WITH_AES_256_CBC_SHA'
key_repo_location = '/Users/mmoreira/key'
message = 'Hello from Python!'

cd = pymqi.CD()
cd.ChannelName = channel
cd.ConnectionName = conn_info
cd.ChannelType = pymqi.CMQC.MQCHT_CLNTCONN
cd.TransportType = pymqi.CMQC.MQXPT_TCP
cd.SSLCipherSpec = ssl_cipher_spec

sco = pymqi.SCO()
sco.KeyRepository = key_repo_location

qmgr = pymqi.QueueManager(None)
qmgr.connect_with_options(queue_manager, cd, sco)

put_queue = pymqi.Queue(qmgr, queue_name)
put_queue.put(message)

get_queue = pymqi.Queue(qmgr, queue_name)
logging.info('Here is the message again: [%s]' % get_queue.get())

put_queue.close()
get_queue.close()
qmgr.disconnect()