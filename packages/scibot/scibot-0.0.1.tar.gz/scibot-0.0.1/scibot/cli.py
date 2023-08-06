#!/usr/bin/env python3.6
"""SciBot command line utilities

Usage:
    scibot db-init    [options] [<database>]
    scibot api-sync   [options] [<database>]
    scibot ws-sync    [options] [<database>]
    scibot debug      [options] [<database>]

Options:
    -h --help       show this
    -d --debug      enable echo and embed
"""

import os
from IPython import embed


def main():
    from docopt import docopt
    args = docopt(__doc__)
    database = args['<database>']
    if database is not None:
        os.environ.update({'SCIBOT_DATABASE': database})

    from scibot import config
    from scibot.db import getSession, init_scibot, AnnoSyncFactory

    if args['db-init']:
        # insurace, it is passed into init direclty as well
        #os.system(f'scibot-dbsetup {config.dbPort()} {database}')
        # the above should be done manually to prevent fat fingers
        init_scibot(database)

    elif args['api-sync']:
        session = getSession(echo=args['--debug'])
        AnnoSync = AnnoSyncFactory(session)
        cur_sync = AnnoSync(config.api_token, config.username,
                            config.group, config.memfile)
        cur_sync.sync_annos()
        pub_sync = AnnoSync(config.api_token, config.username,
                            config.group_staging, config.pmemfile)
        pub_sync.sync_annos()

    elif args['ws-sync']:
        'TODO'

    elif args['debug']:
        from time import time
        session = getSession(echo=args['--debug'])
        if True:
            dcount = {r.uri:r.document_id
                    for r in session.execute('SELECT uri, document_id FROM document_uri')}
            from h import models
            from hyputils.hypothesis import Memoizer
            from scibot.anno import disambiguate_uris
            from interlex.core import makeParamsValues
            mem = Memoizer(config.memfile, config.api_token, config.username, config.group)
            annos, last_updated = mem.get_annos_from_file()
            uris = set(a.uri for a in annos)
            dd = disambiguate_uris(uris)
            multi = [v for v in dd.values() if len(v) > 1]
            _rows = [a._row for a in annos]
            AnnoSync = AnnoSyncFactory(session)
            cur_sync = AnnoSync(config.api_token, config.username, config.group)

            rows = _rows

            # rows = [r for r in _rows if 'articles/4-42/' in r['uri']]
            # rows = [r for r in _rows if '10.1002/jnr.23615' in r['uri']]
            # rows = [r for r in _rows if 'ncomms8028' in r['uri']]  # TODO res chain these
            # rows = [r for r in _rows if '?term=Gene' in r['uri']]
            # rows = [r for r in _rows if 'index.php?' in r['uri']]
            # rows = [r for r in _rows if 'govhttp' in r['uri']]  # maximum wat
            # rows = [r for r in _rows if 'fasebj.org' in r['uri']]

            check = False

            cur_sync.memoization_file = config.memfile
            cur_sync.sync_annos(check=check)


            return
            cur_sync.sync_annos(api_rows=rows, check=check)
            # when remote the upload bandwidth is now the limiting factor
            session.rollback()
            cur_sync.sync_annos(check=check)
            session.rollback()
            embed()


if __name__ == '__main__':
    main()
