#!/usr/bin/env python
#
# A Remember The Milk exporter web app for emacs org-mode users.
#
# Copyright 2012 Angus Gratton, licensed under the MIT License as
# described in the accompanying file README.md.
#
import datetime
import urllib
import bottle
import milky
from milky.datastructures import SortedDict

STANDALONE=False


# you'll need a separate file api_key.py that assigns
# API_KEY = "myapikey"
# API_SECRET = "myapisharedsecret"
from api_key import API_KEY, API_SECRET


@bottle.route("/")
def export():
    api = authenticate(bottle.request.query.frob)
    if api is None:
        return
    lists = api.lists.getList()
    bottle.response.content_type = 'text/plain; charset="utf-8"'
    yield u"# %d RTM lists exported by rtorgmode %s\n" % (
        len(lists),
        datetime.datetime.now().isoformat()
        )
    yield u"#\n"
    sort_lists = lambda l: (l.position, l.name)
    for task_list in sorted(lists, key=sort_lists):
        if task_list.deleted or task_list.smart:
            continue
        tasks = api.tasks.getList(list_id=task_list.id).lists[0].taskseries
        if len(tasks) == 0:
            continue
        yield u"* %s%s\n" % ("DONE " if task_list.archived else "",
                           task_list.name.strip())
        # sort tasks to show non-closed first, then by newest closed
        sort_key = lambda task: (datetime.datetime.max -
                                 (task.task[0].completed or
                                  datetime.datetime.max), task.name.strip())
        for task in sorted(tasks, key=sort_key):
            inner = task.task[0]
            if inner.deleted:
                continue
            yield u"** %s %s %s\n" % ("DONE" if inner.completed else "",
                                   task.name.strip(),
                                   orgify_tags(fix_tags(task.tags)))
            if inner.completed:
                yield u"   CLOSED: [%s]\n" % (format_orgmode_ts(inner.completed))
            elif inner.due and not task_list.archived:
                ts = format_orgmode_date(inner.due)
                yield u"   SCHEDULED: <%s>\n" % (ts)
            if len(task.notes):
                notes = [note.text for note in task.notes]
                # split out any embedded newlines
                notes = "\n".join(notes).split("\n")
                for note in notes:
                    yield "   %s\n" % (note.strip())


def authenticate(frob):
    api = milky.API(API_KEY, API_SECRET, frob=frob)
    if frob is not None:      # verify the frob
        try:
            api.get_token()
            return api        # good frob
        except:
            api.frob = None   # bad frob

    if not STANDALONE:
        # bit hacky: this is a slightly modified version of milky's
        # api.get_auth_url() that generates the URL without a frob
        # param, so that RTM uses the callback URL we supplied for it
        auth_params = SortedDict([
                ('api_key', API_KEY),
                ('perms', 'read') ])
        auth_params['api_sig'] = api._API__sign(auth_params)
        AUTH_URL = 'http://www.rememberthemilk.com/services/auth/'
        auth_url = '%s?%s' % (AUTH_URL, urllib.urlencode(auth_params))
    else:
        auth_url = api.get_auth_url()
    bottle.redirect(auth_url)
    return None


def orgify_tags(tags):
    if len(tags):
        return ":%s:" % ":".join(tags)
    return ""

def format_orgmode_ts(ts):
    return ts.strftime("%Y-%m-%d %a %H:%M")

def format_orgmode_date(ts):
    return ts.strftime("%Y-%m-%d %a")

def fix_tags(tags):
    """ There's a bug in the milky tags type where if there's
    only one tag, it comes up as a list of characters. """
    if all(len(a) == 1 for a in tags):
        s = "".join(tags)
        return [s] if len(s) > 0 else []
    return tags


if __name__ == "__main__":
    STANDALONE=True
    bottle.debug()
    bottle.run(host='localhost', port=8000)
