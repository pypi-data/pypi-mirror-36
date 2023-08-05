import os
import shutil
import time
from collections import OrderedDict
from datetime import datetime
from tempfile import mkdtemp

from conf_tools.utils import locate_files
from system_cmd import CmdException

from .constants import DSwarmConstants
from .dcache_wire import create_propose_message
from .ipfs_utils import IPFSInterface
from .utils import as_seconds, now_until, yaml_dump_omaps


def directory_watcher(mi, watch_dir):
    ipfsi = IPFSInterface(mi.ipfs_path)
    seen = {}
    tmpdir = mkdtemp(prefix='swarm')

    def look_for_files(d, pattern='*'):
        if not os.path.exists(d):
            msg = 'Logs directory does not exist: %s' % d
            raise ValueError(msg)

        filenames = locate_files(d, pattern)
        for f in filenames:
            if 'cache' in f:
                continue
            if f.startswith('.'):
                continue

            if not f in seen:
                seen[f] = True  # XXX

                try:
                    hashed = _add_file(f)
                except Exception as e:
                    print('error adding %s:\n%s' % (f, e))
                    continue

                print('found local %s %s' % (hashed, f))

                interval = now_until(as_seconds('7d'))
                msg = create_propose_message(DSwarmConstants.DLC_BUCKET_FILES, hashed, interval)
                mi.send_to_brain('', msg, sign=True)

    def _add_file(filename):
        d = setup_dir_for_file(ipfsi, tmpdir, filename)
        try:
            hashed = ipfsi.add_ipfs_dir(d)
            return hashed
        except CmdException as e:
            raise Exception(str(e))

    while True:
        look_for_files(watch_dir)
        time.sleep(59)


def setup_dir_for_file(ipfsi, tmpdir, filename):
    b0 = os.path.basename(filename)
    b = b0.replace('.', '_')
    d = os.path.join(tmpdir, b)
    if not os.path.exists(d):
        os.mkdir(d)
    dest = os.path.join(d, b0)

    if not os.path.exists(dest):
        try:
            os.link(filename, dest)
        except OSError:
            shutil.copy(filename, dest)

    r = OrderedDict()
    r['filename'] = b0
    mtime = os.path.getmtime(filename)
    r['ctime'] = datetime.fromtimestamp(mtime)
    # no - otherwise it changes every time
    #    r['upload_host'] = socket.gethostname()
    # r['upload_date'] = datetime.now()
    r['upload_node'] = ipfsi.ipfs_id()
    #    r['upload_user'] = getpass.getuser()
    info = os.path.join(d, 'upload_info1.yaml')
    with open(info, 'w') as f:
        y = yaml_dump_omaps(r)
        f.write(y)
    return d
