import os
import time

from dateutil.parser import parse


class DSwarmConstants(object):
    port_dswarm = 8000
    #    port_ssh = 8001
    port_shell = 8002
    port_ipfs_api = 6001
    port_ipfs_gw = 6080
    port_ipfs_swarm = 6002

    port_udp_broadcast = 1240

    IPFS_STORAGE_DIR_V = 'DSWARM_DIR_IPFS'
    IPFS_STORAGE_DIR = os.environ.get(IPFS_STORAGE_DIR_V, "~/.ipfs-dswarm")
    DEFAULT_DIR_V = 'DSWARM_DIR_STORAGE'
    DEFAULT_DIR = os.environ.get(DEFAULT_DIR_V, '~/shared-logs')
    # docker -H tcp://tl47.local:2375 run -p 8000 -p 8001 -p 8002 -p 6001 -p 6080 -p 6002 -it duckietown/rpi-duckietown-swarm dt-swarm daemon

    DELTA_PEER = 10 * 60
    SDELTA_MAKE_SUMMARY = '5m'

    SDELTA_INFO = '5d'

    ALL_BRAINS = '/dswarm/*/brain'

    IPFS_ADDRESSES = 'ipfs_addresses'
    IPFS_PEERS = 'ipfs_peers'



    PRI = 'pri'

    # IRC_SERVER = 'irc.freenode.net'
    IRC_SERVER = 'frankfurt.co-design.science'
    IRC_CHANNEL = '#duckiebots'

    PUBSUB_TOPIC = 'duckiebots'

    PUBSUB_FRIENDS_GREETING = 'duckiebots\n'

    SHARE = 'share'
    DLC_BUCKET_PEER = 'peer'
    DLC_BUCKET_NETWORKS = 'networks'

    DLC_BUCKET_FILES = (SHARE, 'files')
    DLC_BUCKET_VERIFIED = (SHARE, 'verified')
    DLC_BUCKET_SAFE = (SHARE, 'safe')
    DLC_BUCKET_DISCARD = (SHARE, 'discard')

    BOOTSTRAP_PATTERNS = ['/peers', '*/summaries', '*/ipfs_addresses',
                          #                          '*/info/*', '*/versions/*'
                          ]

    use_irc = True
    use_pubsub = True
    use_udp = True
    activate_shell_access = False

    date = "Sat Mar  3 10:17:50 CET 2018"
    ignore_before = time.mktime(parse(date).timetuple())
