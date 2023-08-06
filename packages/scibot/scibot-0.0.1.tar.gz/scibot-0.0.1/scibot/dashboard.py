#!/usr/bin/env python3.6
import atexit
from os import environ
from pathlib import Path
from jinja2 import ChoiceLoader, FileSystemLoader
from scibot.config import api_token, username, group, group_staging, memfile, pmemfile
from scibot.release import Curation, PublicAnno
from scibot.rrid import PMID, DOI
from scibot.export import bad_tags
from pyontutils.utils import anyMembers, noneMembers
from pyontutils.htmlfun import render_table, htmldoc, atag, divtag
from pyontutils.htmlfun import table_style, navbar_style, cur_style
 
from hyputils.subscribe import preFilter, AnnotationStream
from hyputils.handlers import helperSyncHandler, filterHandler
from hyputils.hypothesis import Memoizer
from flask import Flask, render_template, request, url_for
from IPython import embed

print('END IMPORTS')

def route(route_name):
    def wrapper(function):
        def inner(*args, **kwargs):
            print(route_name)
            return function(*args, **kwargs)
        return inner
    return wrapper

def make_app(annos, pannos=[]):

    app = Flask('scibot dashboard')

    template_loader = ChoiceLoader([app.jinja_loader,
                                    FileSystemLoader([(Path(__file__).parent.parent / 'templates').as_posix()])])
    app.jinja_loader = template_loader

    [Curation(a, annos) for a in annos]
    [PublicAnno(a, pannos) for a in pannos]
    base_url = '/dashboard/'
    names = ['missing', 'incorrect', 'papers', 'unresolved',
             'no-pmid', 'no-doi', 'no-annos', 'table', 'Journals']

    def tag_string(c):
        return ' '.join(sorted(t.replace('RRIDCUR:', '')
                               for t in c.tags if 'RRIDCUR' in t))

    def filter_rows(filter=lambda c: True):
        yield from ((str(i + 1),
                     tag_string(c),
                     atag(PMID(c.pmid), c.pmid, new_tab=True)
                     if c.pmid
                     else (atag(DOI(c.doi), c.doi, new_tab=True)
                           if c.doi
                           else ''),
                     atag(c.shareLink, 'Annotation', new_tab=True)
                     if c  # FIXME how does this work?
                     else atag(c.uri, 'Paper', new_tab=True),
                     atag(c.htmlLink, 'Anno HTML', new_tab=True),
                     c.user,
                     '\n'.join(c.curator_notes))
                    for i, c in enumerate(sorted((c for c in Curation
                                                  if c.isAstNode
                                                  and not c.Duplicate
                                                  and not c.corrected  # FIXME need a better way...
                                                  and not c.public_id
                                                  and filter(c)),
                                                 key=tag_string)))
    k = 0
    kList = []
    URLDict = {}
    for h in Curation:
        if BaseURL(h._anno) in URLDict.keys():
            URLDict[BaseURL(h._anno)] += 1
        else:
            URLDict[BaseURL(h._anno)] = 1
            kList.append(k)
    class NavBar:
        def atag(self, route, name):
            if route == self.current_route:
                return atag(url_for(route), name, cls='navbar-select')
            else:
                return atag(url_for(route), name)

        def __call__(self, route=None):
            self.current_route = route
            out =  divtag(self.atag('route_base', 'Home'),
                          self.atag('route_papers', 'Papers'),
                          self.atag('route_anno_help_needed', 'Help Needed'),
                          self.atag('route_anno_incorrect', 'Incorrect'),
                          self.atag('route_anno_unresolved', 'Unresolved'),
                          self.atag('route_anno_missing', 'Missing'),
                          self.atag('route_no_pmid', 'No PMID'),
                          self.atag('route_no_doi', 'No DOI'),
                          self.atag('route_no_id', 'No ID'),
                          #self.atag('route_no_annos', 'No annos'),
                          self.atag('route_table', 'All'),
                          # TODO search box
                          atag('https://github.com/SciCrunch/scibot/issues',
                               'GitHub issues', new_tab=True),
                          cls='navbar')
            self.current_route = None
            return out

    navbar = NavBar()

    def table_rows(rows, title, route):
        return htmldoc(navbar(route),
                       divtag(render_table(rows, '#', 'Problem', 'Identifier', 'Link', 'HTML Link', 'Curator', 'Notes'),
                              cls='main'),
                       title=title,
                       styles=(table_style, cur_style, navbar_style))

    def nonestr(thing):
        return '' if thing is None else thing

    def done_rrids(rrids):
        for rrid, s in rrids.items():
            for a in s:
                if a.Validated:
                    yield rrid
                    break

    def todo_rrids(rrids):
        done = set(done_rrids(rrids))
        for rrid in rrids:
            if rrid not in done:
                yield rrid

    def render_papers(rows):
        return divtag(render_table(rows,
                                   '#', 'Paper', 'PMID', 'DOI',
                                   'TODO', 'Done', 'RRIDs', 'Annotations'),
                      cls='main')

    def papers(filter=lambda a:True):
        return [(str(i + 1),) + t
                for i, t in
                enumerate(sorted(((atag(url, '...' + url[-20:], new_tab=True),
                                   nonestr(rrids.pmid),
                                   '' if
                                   rrids.doi is None else
                                   atag(DOI(rrids.doi), rrids.doi, new_tab=True),
                                   str(len(list(todo_rrids(rrids)))),
                                   str(len(list(done_rrids(rrids)))),
                                   str(len(rrids)),
                                   str(len([a for r in rrids.values()
                                            for a in r])))
                                  for url, rrids in Curation._papers.items()
                                  if filter(next(a for s in rrids.values()
                                                  for a in s))),
                                 key=lambda r: int(r[3]),
                                 reverse=True))]

    def no_pmid():
        return papers(lambda a:a.pmid is None)

    def no_doi():
        return papers(lambda a:a.doi is None)

    def no_id():
        return papers(lambda a:a.doi is None and a.pmid is None)

    def no_annos():  # TODO
        return []

    @app.route('/css/table.css')
    def route_css_table_style():
        return table_style, 200, {'Content-Type':'text/css'}

    @app.route('/dashboard', methods=('GET', 'POST'))
    @app.route('/dashboard/', methods=('GET', 'POST'))
    def route_base():
        return render_template('main.html', method='get',
                               navbar=navbar(request.url_rule.endpoint),
                               navbar_style = navbar_style,
                               var='We have a lot of work to do!',
                               nmissing='??',
                               nures='??',
                               incor='??',
                               npapers=str(len(Curation._papers)),
                               nnopmid=str(len(no_pmid())),
                               nnodoi=str(len(no_doi())),
                               #nnoboth=str(len(no_both())),
                               #nnoannos=str(len(no_annos()))
                               nnoannos='??',
                               allp='??',)

    @app.route('/dashboard/anno-count')
    def route_anno_count():
        return str(len(Curation._annos_list))

    #@app.route(PurePath(base_url, 'anno-tags').as_posix())
    @app.route('/dashboard/anno-user/<user>')
    def route_anno_tags(user):
        print(user)
        out = '\n'.join([f'{anno.user} {anno.text} {anno.tags}<br>'
                         for anno in Curation._annos_list if anno.user == user])
        return out

    @app.route('/dashboard/journals')
    def route_Journals():
        file = open("Journals.txt","r")
        paperStr = file.read()
        file.close()
        if paperStr == '':
            h = 0
            URLList = []
            counter = 0
            paperStr = str(counter) + ' Results:<br><br>'
            print("PROSSESING")
            for h in Curation:
                journal = Journal(h._anno)
                if "urn:x-pdf" in journal or "file:" in journal:
                    URLList.append(journal)
                if journal == "":
                    print (h.shareLink)
                if not journal in URLList:
                    paperStr += "<br> <a href=\"" + h.shareLink + "\"> Journal Link </a><br>"
                    paperStr += journal
                    counter += 1
                    URLList.append(journal)
            paperStr = str(counter) + paperStr[1:]
            file = open("Journals.txt", "w")
            file.write(paperStr)
            file.close()
        return (paperStr)	

    @app.route('/dashboard/DOI')
    def route_DOI():
        DOIStr = ""
        DOIList = []
        counter = 0
        for h in Curation:
            if [t for t in h.tags if t.startswith("DOI")]:
                if h.doi not in DOIList:
                    DOIStr += '<br> Anno #:%s <br>' % h
                    DOIStr += '<a href=' + h.shareLink + '> Anno Link </a><br>'
                    DOIStr += h.doi
                    counter += 1
                    if h.doi:
                        DOIList.append(h.doi)
        return (str(counter) + "<br><br>" + DOIStr)

    @app.route('/dashboard/done')
    def route_done():
        return 'TODO'

    @app.route('/dashboard/public')
    def route_public():
        #return 'TODO'
        rows = ((str(i + 1),) + r for i, r in
                enumerate((nonestr(pa.curation_paper.pmid),
                           nonestr(pa.curation_paper.doi),
                           pa.rrid,)
                          for pa in PublicAnno
                          # skip incorrectly formatted and errors for now
                          if pa.curation_ids and
                          None not in pa.curation_annos and
                          pa.rrid is not None  # FIXME make clear these are page notes
                ))
        return htmldoc(navbar(request.url_rule.endpoint),
                       divtag(render_table(rows, '#', 'PMID', 'DOI', 'RRID'),
                                           cls='main'),
                       title='SciBot public release',
                       styles=(table_style, cur_style, navbar_style))

    @app.route('/dashboard/table')
    def route_table():
        rows = filter_rows(lambda c: c.very_bad or c._Missing and not c.rrid or c.Incorrect or c.Unresolved)
        return table_rows(rows, 'All SciBot curation problems', request.url_rule.endpoint)

        """
        <style type="text/css">
            td {width: 300px; hight 40px}     
            td {border: 1px solid #000000;}
            a.class1:link {
                background-color: #aaaaff;
                color: white;
                padding: 14px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
            }
              a.class2:visited, a.class2:link{
                  background-color: #79c478;

                  color: black;
                  padding: 14px 25px;
                  text-align: center;
                  text-decoration: none;
                  display: inline-block;
              }
              a.class1:visited {
                  background-color: #009cdb;
                  color: white;
              }

              a.class1:hover, a.class1:active, a.class2:hover, a.class2:active {background-color: red;}
        </style>"""

    @app.route('/dashboard/no-annos')
    def route_no_annos():
        return htmldoc(navbar(request.url_rule.endpoint),
                       divtag('There shouldn\'t be anything here...',
                              cls='main'),
                       title='SciBot No Anno Papers',
                       styles=(navbar_style,))

    @app.route('/dashboard/papers')
    def route_papers():
        rows = papers()
        return htmldoc(navbar(request.url_rule.endpoint),
                       render_papers(rows),
                       title='SciBot papers',
                       styles=(table_style, cur_style, navbar_style))

    @app.route('/dashboard/no-pmid')
    def route_no_pmid():
        rows = no_pmid()
        return htmldoc(navbar(request.url_rule.endpoint),
                       render_papers(rows),
                       title='SciBot No PMID Papers',
                       styles=(table_style, cur_style, navbar_style))

    @app.route('/dashboard/no-doi')
    def route_no_doi():
        rows = no_doi()
        return htmldoc(navbar(request.url_rule.endpoint),
                       render_papers(rows),
                       title='SciBot No DOI Papers',
                       styles=(table_style, cur_style, navbar_style))

    @app.route('/dashboard/no-id')
    def route_no_id():
        rows = no_id()
        return htmldoc(navbar(request.url_rule.endpoint),
                       render_papers(rows),
                       title='SciBot No ID Papers',
                       styles=(table_style, cur_style, navbar_style))

    @app.route('/dashboard/help-needed')
    def route_anno_help_needed():
        rows = filter_rows(lambda c: c.very_bad)

        return table_rows(rows, 'Help needed RRIDs', request.url_rule.endpoint)

    @app.route('/dashboard/incorrect')
    def route_anno_incorrect():
        rows = filter_rows(lambda c: not c.very_bad and c.Incorrect)
        return table_rows(rows, 'Incorrect RRIDs', request.url_rule.endpoint)

    @app.route('/dashboard/unresolved')
    def route_anno_unresolved():
        rows = filter_rows(lambda c: c.Unresolved and not c.very_bad and not c.Incorrect)

        return table_rows(rows, 'Unresolved RRIDs', request.url_rule.endpoint)

    @app.route('/dashboard/missing', methods=('GET', 'POST'))
    def route_anno_missing():
        rows = filter_rows(lambda c: c._Missing and not c.rrid)
        return table_rows(rows, 'Missing RRIDs', request.url_rule.endpoint)

    @app.route('/dashboard/no-replies')
    def route_no_replies():
        # this should be the table with no replies
        return 'TODO'

    @app.route('/dashboard/results')
    def search_results(search):
        h = 0
        hlist = []
        hstr = ''
        counter = 0
    #    if search.data['search'] == '':
    #        h = 0
    #        hstr = ''
    #        for h in Curation:
    #            hstr += repr(h)
    #            h += 1
    #        return(hstr)
    #    else:
        if search.data['select'] == 'ID':
            for h in Curation:
                if search.data['search'] in h.id:
                    hstr += '<br> Anno #:%s <br>' % h
                    hstr += '<a href=' + h.shareLink + '> Anno Link </a><br>'
                    hstr += repr(h)
                    counter += 1
            if hstr == '':
                return('no results')
            return (str(counter) + ' Results:<br><br>' + hstr)
            #return render_template('results.html', results=html.unescape(hstr))
        elif search.data['select'] == 'Tags':
            for h in Curation:
                if [t for t in h.tags if search.data['search'] in t]:
                    hstr += '<br> Anno #:%s <br>' % h
                    hstr += '<a href=' + h.shareLink + '> Anno Link </a><br>'
                    hstr += repr(h)
                    counter += 1
            if hstr == '':
                return('no results')
            print (str(len(hlist)))
            print(len(Curation._annos_list))
            return (str(counter) + ' Results:<br><br>' + hstr)
            #return render_template('results.html', results=hstr)
        elif search.data['select'] == 'User':
            for h in Curation:
                if h._anno.user == search.data['search']:
                    hstr += '<br> Anno #:%s <br>' % h
                    hstr += '<a href=' + h.shareLink + '> Anno Link </a><br>'
                    hstr += repr(h)
                    counter += 1
            if hstr == '':
                return('no results')
            return (str(counter) + ' Results:<br><br>' + hstr)
        else:
            return search_text(search.data['select'], Curation._annos_list, list(Curation), search.data['search'])

    #new_function = route('/my/route')(route_base)

    #return new_function
    #embed()
    return app
    #new_function_outside = make_app('not really annos')

def search_text(text, annos,  search):
        h = 0
        hlist = []
        hstr = ''
        counter = 0
        for h in Curation:
            hsplit = h.text.split('<p>',h.text.count('<p>'))
            t = 0
            Data = ''
            for t in range(0, len(hsplit)):
                if text in hsplit[t]:
                    Data = hsplit[t].replace(text + ': ', '')
            
            if search.upper() in Data.upper():
                hstr += '<br> Anno #:%s <br>' % h
                hstr += '<a href=' + h.shareLink + '> Anno Link </a><br>'
                hstr += repr(h)
                hstr += "<br>" + BaseURL(annos[h])
                counter += 1
        if hstr == '':
            return('no results')
        return (str(counter) + ' Results:<br><br>' + hstr)

def BaseURL(anno):
    URL = anno.uri.replace(".long", "").replace("/abstract", "").replace("/full","").replace(".short", "").replace(".full", "").replace("http://","").replace("https://","").replace("/FullText","").replace("/Abstract","").replace("/enhanced","")
    SplitURL = URL.split("/", URL.count("/"))
    if SplitURL[-1] == '':
        URL = SplitURL[0] + SplitURL[-2]
    else:
        URL = SplitURL[0] + SplitURL[-1]
    return URL

def Journal(anno):
    URL = anno.uri.replace(".long", "").replace("/abstract", "").replace("/full","").replace(".short", "").replace(".full", "").replace("http://","").replace("https://","").replace("/FullText","").replace("/Abstract","").replace("/enhanced","")
    SplitURL = URL.split("/", URL.count("/"))
    if len(SplitURL) == 1 or len(SplitURL) == 0:
        print(URL)
    URL = SplitURL[0]
    return URL

def annoSync(memfile, group, helpers=tuple(), world_ok=False):
    if group == '__world__' and not world_ok:
        raise ValueError('Group is set to __world__ please run the usual `export HYP_ ...` command.')
    get_annos = Memoizer(memfile, api_token, username, group)
    yield get_annos
    prefilter = preFilter(groups=[group]).export()
    hsh = type(f'helperSyncHandler{group}',
               (helperSyncHandler,),
               dict(memoizer=get_annos,
                    helpers=helpers))
    annos = get_annos()
    yield annos
    stream_thread, exit_loop = AnnotationStream(annos, prefilter, hsh)()
    yield stream_thread
    yield exit_loop

def setup():
    get_annos, annos, stream_thread, exit_loop = annoSync(memfile, group, (Curation,))
    get_pannos, pannos, pstream_thread, pexit_loop = annoSync(pmemfile, group_staging,
                                                (PublicAnno,), world_ok=True)
    def close_stuff():
        exit_loop()
        stream_thread.join()

    atexit.register(close_stuff)

    stream_thread.start()
    app = make_app(annos, pannos)
    app.debug=False
    return app

def main():
    get_annos, annos, stream_thread, exit_loop = annoSync(memfile, group, (Curation,))
    get_pannos, pannos, pstream_thread, exit_loop = annoSync(pmemfile, group_staging,
                                                (PublicAnno,), world_ok=True)

    app = make_app(annos, pannos)
    #stream_loop.start()
    #pstream_loop.start()  # FIXME eventloop already running error...
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    print(app.view_functions)
    app.debug = False
    from scibot.config import test_host, port_dashboard
    app.run(host=test_host, port=port_dashboard)

if __name__ == '__main__':
    main()
