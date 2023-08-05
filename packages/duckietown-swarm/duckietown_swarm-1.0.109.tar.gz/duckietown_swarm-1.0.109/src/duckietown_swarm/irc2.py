#! /usr/bin/env python
import argparse
import os
import time
from multiprocessing import Queue

from contracts import contract
from contracts.utils import indent

from .constants import DSwarmConstants
from .crypto import get_key
from .dcache import Envelope
from .directory_watcher_imp import directory_watcher
from .ipfs_utils import IPFSInterface
from .irc_talker import start_irc
from .pinner import pinner, verifier
from .process_manager import ProcessManager
from .pubsub_friends import connecting_to_peer, pubsub_friendship
from .pubsub_processes import pubsub_reader_process, pubsub_writer_process
from .shell import shell_access
from .spawn_ipfs import check_ipfs_executable, run_ipfs, initialize_ipfs
from .summary import publish_ipns
from .synthetic_data import synthetic_data_writer
from .tcpendpoint import tcplisten
from .udp_interface import get_suitable_udp_interfaces, \
    udp_broadcaster, udp_listener
from .utils import get_all_available, get_at_least_one

DSC = DSwarmConstants


class Dispatcher(object):

    def __init__(self, prefix):
        self.prefix = prefix
        self.name2queue = {}
        self.my_maddr = None

    @contract(envelope=Envelope)
    def dispatch(self, envelope, sign=False):
        n = 0
        if not envelope.maddr_to:
            em = 'The address is empty.'
            em += "\n" + envelope.verbose()
            raise Exception(em)
        #        print('dispatch %s' % envelope.maddr_to)

        for name, q in self.name2queue.items():
            is_match, rest = prefix_match(address=envelope.maddr_to, x=name)
            if is_match:
                #                print('Sending %r to pipe %r with rest %r' % (envelope.maddr_to, name, rest))
                maddr_to = rest
                maddr_from = self.my_maddr + envelope.maddr_from
                e = Envelope(maddr_from, maddr_to, envelope.contents)
                if sign:
                    #                    if 'signature' in envelope.contents:
                    #                        em = 'Will not sign a signature: %s' % envelope
                    #                        raise Exception(em)
                    msg_sign = self.key.generate_sign_message(envelope.contents)
                    e_sign = Envelope(maddr_from, maddr_to, msg_sign)
                    q.put(e_sign)
                q.put(e)
                #                print('forward to queue %s orig: %s\nforw: %s' % (name, envelope, e))
                n += 1

        if n == 0:
            msg = 'Could not find channel for %r' % envelope.maddr_to
            msg += '\n\n' + indent("\n".join(sorted(self.name2queue)), '  ')
            msg += '\n\nEnvelope:'
            msg += '\n\n' + indent(envelope.verbose(), '  ')
            raise CouldNotDispatch(msg)

    def get_ipfsi(self):
        return IPFSInterface(self.ipfs_path)

    @contract(returns=Envelope)
    def get_next_for_me(self):
        q = self.name2queue[self.my_maddr]
        return q.get()

    @contract(returns='list($Envelope)')
    def get_many_for_me(self, timeout):
        q = self.name2queue[self.my_maddr]
        return get_at_least_one(q, timeout=timeout)

    @contract(returns='list($Envelope)')
    def get_all_available_for_me(self):
        q = self.name2queue[self.my_maddr]
        return get_all_available(q)


class CouldNotDispatch(Exception):
    pass


def prefix_match(address, x):
    '''

    Examples:

        /irc/host/channel /irc/host/channel
        True, ''
        /irc/host/channel/b /irc/host/channel
        True, '/b'
        /irc/*/channel /irc/host/channel
        True, ''

        /irc/*/channel/b /irc/host/channel
        True, '/b'

    '''
    ta = address.split('/')
    tx = x.split('/')

    #    print('ta: %s' % ta)
    #    print('tx: %s' % tx)

    def match(A, B):
        assert not '*' in B, (A, B)
        return A == B or ('*' == A)

    #    for lm in reversed(range(len(tx) + 1)):
    lm = len(tx)
    if len(ta) < len(tx):
        return False, None
    for i in range(lm):
        a = ta[i]
        x = tx[i]
        if not match(a, x):
            #                print('not matched with %s because %s != %s' % (lm, a, x))
            return False, None
            break
    else:
        #            print('matched up to %s: %r %r' % (lm, ta[:lm], tx[:lm]))
        remain = ta[lm:]
        if remain:
            rest = '/' + '/'.join(remain)
        else:
            rest = ''
        return True, rest


class MessagingInterface(Dispatcher):

    def __init__(self, key, ipfs_path):
        prefix = '/dswarm' + '/' + key.hash
        Dispatcher.__init__(self, prefix)

        self.key = key
        self.ipfs_path = ipfs_path

        APP = prefix
        self.MADDR_BRAIN = APP + '/brain'
        self.MADDR_PINNER = APP + '/pinner'
        self.MADDR_CONNECTOR = APP + '/connector'
        self.MADDR_VERIFIER = APP + '/verifier'
        self.MADDR_IPNS = APP + '/ipns'
        self.MADDR_DIRWATCHER = APP + '/dirwatcher'
        self.MADDR_PUBSUBFRIENDS = APP + '/pubfriends'
        self.MADDR_IRC = '/dns4/%s/tcp/6667/irc' % DSC.IRC_SERVER
        self.IRC_CHANNEL = DSC.IRC_CHANNEL
        self.MADDR_PUBSUBWRITER = APP + '/pubsubwriter'
        self.MADDR_READ_SUMMARIES = APP + '/read_summaries'
        self.MADDR_TCP_SERVER = APP + '/tcpserver'

        self.pubsub_topic = DSC.PUBSUB_TOPIC

        self.MADDR_PUBSUBWRITER = '/ipfs-pubsub/' + self.pubsub_topic

        self.name2queue = {}
        self.name2queue[self.MADDR_PINNER] = Queue()
        self.name2queue[self.MADDR_BRAIN] = Queue()
        self.name2queue[self.MADDR_VERIFIER] = Queue()
        self.name2queue[self.MADDR_IPNS] = Queue()
        self.name2queue[self.MADDR_IRC] = Queue()
        self.name2queue[self.MADDR_PUBSUBWRITER] = Queue()
        self.name2queue[self.MADDR_READ_SUMMARIES] = Queue()
        self.name2queue[self.MADDR_CONNECTOR] = Queue()
        self.name2queue[self.MADDR_TCP_SERVER] = Queue()

        self.udps = []

        for name, x in get_suitable_udp_interfaces().items():
            #            _address = x['address']
            broadcast = x['broadcast']
            #            a = '/ip4/%s/udp/%s' % (broadcast, UDP_PORT)
            a = '/udp/%s/%s/%s' % (name, broadcast, DSwarmConstants.port_udp_broadcast)
            self.name2queue[a] = Queue()
            self.udps.append(a)

    def broadcast_to_all_brains(self, msg, sign):

        for c in self._get_broadcasting_channels():
            new_to = c + DSC.ALL_BRAINS
            envelope = Envelope(maddr_from='', maddr_to=new_to, contents=msg,
                                comment='process: ' + self.my_maddr)
            self.dispatch(envelope, sign=sign)

    def _get_broadcasting_channels(self):
        return [
                   self.MADDR_PUBSUBWRITER,
                   self.MADDR_IRC + '/' + self.IRC_CHANNEL,
               ] + self.udps

    def copy_as(self, my_maddr):
        c = MessagingInterface(self.key, self.ipfs_path)
        c.name2queue.update(self.name2queue)
        c.my_maddr = my_maddr
        return c

    @contract(from_channel=str, msg=str)
    def send_to_brain(self, from_channel, msg, sign=False):
        e = Envelope(from_channel, self.MADDR_BRAIN, msg)
        self.dispatch(e, sign=sign)

    @contract(mh='multihash')
    def send_to_pinner(self, mh):
        e = Envelope('', self.MADDR_PINNER, mh)
        self.dispatch(e)

    def send_to_connector(self, address):
        e = Envelope('', self.MADDR_CONNECTOR, address)
        self.dispatch(e)

    @contract(mh='multihash')
    def send_to_readsummaries(self, mh):
        e = Envelope('', self.MADDR_READ_SUMMARIES, mh)
        self.dispatch(e)

    @contract(mh=str)
    def send_to_verifier(self, mh):
        e = Envelope('', self.MADDR_VERIFIER, mh)
        self.dispatch(e)

    @contract(key=str, mh=str)
    def send_to_ipns_publisher(self, key, mh):
        assert mh.startswith('Qm'), (key, mh)
        e = Envelope('', self.MADDR_IPNS, (key, mh))
        self.dispatch(e)


def duckietown_swarm_main(args=[]):
    from . import __version__
    print('dt-swarm %s' % __version__)
    #    print '''
    #
    # Security note: this program opens the SSH port to the swarm.
    #
    #
    # '''
    ##It is designed to be used in a friendly environment.
    ##
    ##DO NOT use on production machines.
    #
    #    time.sleep(3)
    #    print('ready?')
    #    time.sleep(1)
    #    print('go!')
    #    time.sleep(1)

    parser = argparse.ArgumentParser(description='Daemon options')
    parser.add_argument('--low-power', default=False,
                        action='store_true',
                        dest='low_profile',
                        help='Activates low profile (for RPI)')
    parser.add_argument('--ipfs-dir',
                        default=DSwarmConstants.IPFS_STORAGE_DIR,
                        type=str,
                        dest='ipfs_dir',
                        help='Default IPFS path (Also set with env %s)' % DSwarmConstants.DEFAULT_DIR_V)
    parsed = parser.parse_args(args=args)

    watch_dir = os.path.expanduser(DSwarmConstants.DEFAULT_DIR)
    ipfs_path = os.path.expanduser(parsed.ipfs_dir)
    low_profile = parsed.low_profile

    npinners = 10
    nconnectors = 10
    nverifiers = 5
    do_ipns = True
    do_watch = True

    if low_profile:
        print('activate low profile')
        # no file
        npinners = 0
        nverifiers = 0
        nconnectors = 3
        do_ipns = False
        do_watch = False

    print('nverifiers: %s' % nverifiers)
    print('npinners: %s' % npinners)
    print('do ipns: %s' % do_ipns)
    print('Use watch dir = %s ' % watch_dir)
    print('Use IPFS path = %s ' % ipfs_path)

    if not os.path.exists(watch_dir):
        os.makedirs(watch_dir)

    cache_dir = os.path.join(watch_dir, '.cache')

    check_ipfs_executable(ipfs_path)
    initialize_ipfs(ipfs_path)
    ipfsi = IPFSInterface(ipfs_path)

    try:
        print(ipfsi.stats_bw())
        print('OK - ipfs was running')
    except:
        print('Now starting ipfs')
        run_ipfs(ipfs_path, DSwarmConstants.use_pubsub)
        while True:
            time.sleep(1)
            try:
                print(ipfsi.stats_bw())
                break
            except:
                pass

    identity = ipfsi.ipfs_id()

    print('%s Identity: %s' % (ipfs_path, identity))

    ipfsi.p2p_listener_open('p2p-ssh', '/ip4/127.0.0.1/tcp/22')
    ipfsi.p2p_listener_open('p2p-dswarm', '/ip4/127.0.0.1/tcp/%s' % DSwarmConstants.port_dswarm)
    ipfsi.p2p_listener_open('p2p-shell', '/ip4/127.0.0.1/tcp/%s' % DSwarmConstants.port_shell)

    key = get_key(cache_dir)
    key.hash = identity
    print('You can put any log file in the directory\n\n\t%s\n\n'
          'and it will be shared with the swarm.\n\n' % watch_dir)

    '''
        incoming -> [brain] -> outgoing
                               pinner_queue
                    publisher_queue


            pinner_queue -> [pinner] -> pinner

            publisher_queue -> [publisher] -> incoming



        outgoing[0] -> [irc server]
        outgoing[1]
    '''

    mi = MessagingInterface(key, ipfs_path)
    interfaces = get_suitable_udp_interfaces()
    if DSwarmConstants.use_udp:
        for x in mi.udps:
            interface = x.split('/')[2]
            assert interface in interfaces, (interface, x.split('/'))

            print('starting udp listening on %r %r' % (interface, x))
            pm = ProcessManager(udp_broadcaster,
                                (mi.copy_as(x), interface, DSwarmConstants.port_udp_broadcast), x,
                                restart=True)
            pm.start()

            pm = ProcessManager(udp_listener,
                                (mi.copy_as(x), interface, DSwarmConstants.port_udp_broadcast), x,
                                restart=True)
            pm.start()

    pm = ProcessManager(publish_ipns,
                        (mi.copy_as(mi.MADDR_IPNS),), 'publish_ipns',
                        restart=True)
    pm.start()

    if DSwarmConstants.use_pubsub:
        pm = ProcessManager(pubsub_reader_process,
                            (mi.copy_as(mi.MADDR_PUBSUBWRITER), mi.pubsub_topic), 'pubsub_reader',
                            restart=True)
        pm.start()

        pm = ProcessManager(pubsub_writer_process,
                            (mi.copy_as(mi.MADDR_PUBSUBWRITER), mi.pubsub_topic), 'pubsub_writer',
                            restart=True)
        pm.start()

    for i in range(npinners):
        pm = ProcessManager(pinner, (mi.copy_as(mi.MADDR_PINNER),), 'pinner%d' % i, restart=True)
        pm.start()

    for i in range(nconnectors):
        pm = ProcessManager(connecting_to_peer, (mi.copy_as(mi.MADDR_CONNECTOR),), 'connector%d' % i, restart=True)
        pm.start()

    for i in range(nverifiers):
        pm = ProcessManager(verifier, (mi.copy_as(mi.MADDR_VERIFIER),), 'verifier%d' % i, restart=True)
        pm.start()

    from .brain import brain

    # server = ('frankfurt.co-design.science', 6667)
    server = (DSC.IRC_SERVER, 6667)
    channel = '#duckiebots'
    if DSwarmConstants.use_irc:
        pm = ProcessManager(start_irc,
                            (mi.copy_as(mi.MADDR_IRC), server, channel),
                            'irc1',
                            restart=True)
        pm.start()

    #    if False:
    #        servers = [('irc.freenode.net', 6667), ]
    #        pm = ProcessManager(start_irc,
    #                            ('to_irc2', servers, mi), 'irc2',
    #                            restart=True)
    #        pm.start()

    brainp = ProcessManager(brain,
                            (mi.copy_as(mi.MADDR_BRAIN), cache_dir), 'brain',
                            restart=True)
    brainp.start()

    if do_watch:
        pm = ProcessManager(directory_watcher,
                            (mi.copy_as(mi.MADDR_DIRWATCHER), watch_dir), 'directory_watcher',
                            restart=True)
        pm.start()

    from .offline import read_nodes_summaries

    for i in range(1):
        pm = ProcessManager(read_nodes_summaries,
                            (mi.copy_as(mi.MADDR_READ_SUMMARIES),), 'read_nodes_summaries%d' % i,
                            restart=True)
        pm.start()

    pm = ProcessManager(pubsub_friendship,
                        (mi.copy_as(mi.MADDR_PUBSUBFRIENDS),), 'pubsub_friendship',
                        restart=True)
    pm.start()

    pm = ProcessManager(tcplisten,
                        (mi.copy_as(mi.MADDR_TCP_SERVER), DSwarmConstants.port_dswarm),
                        'tcplisten%s' % DSwarmConstants.port_dswarm,
                        restart=True)
    pm.start()

    if DSwarmConstants.activate_shell_access:
        pm = ProcessManager(shell_access,
                            (DSwarmConstants.port_shell,), 'shell%s' % DSwarmConstants.port_shell,
                            restart=True)
        pm.start()

    if False:
        pm = ProcessManager(synthetic_data_writer, (watch_dir,), 'synthetic', restart=True)
        pm.start()

    #    pm = ProcessManager(publisher_summary,
    #                        (mi, '/dswarm/summary'), 'publisher_summary',
    #                        restart=True)
    #    pm.start()

    brainp.p.join()


if __name__ == "__main__":
    duckietown_swarm_main()
