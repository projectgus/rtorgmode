#!/usr/bin/env python

import time, datetime, sys
import bottle, milky

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
    yield u"# %d RTM lists exported by rtm2orgmode %s\n" % (len(lists), datetime.datetime.now().isoformat())
    yield u"#\n"
    for task_list in sorted(lists, key=lambda l:l.position):
        if task_list.deleted or task_list.smart:
            continue
        list_todo = ""
        tasks = api.tasks.getList(list_id=task_list.id).lists[0].taskseries
        if len(tasks) == 0:
            continue
        yield u"* %s %s\n" % ("DONE" if task_list.archived else "",
                           task_list.name.strip())
        for task in tasks:
            if task.task[0].deleted:
                continue
            yield u"** %s %s %s\n" % ("DONE" if task.task[0].completed else "",
                                   task.name.strip(),
                                   orgify_tags(fix_tags(task.tags)))
            if task.task[0].completed:
                yield u"   CLOSED: [%s]\n" % (task.task[0].completed.strftime("%Y-%m-%d %A %H:%M"))
            if len(task.notes):
                notes = "\n".join([ note.text for note in task.notes ]).split("\n")
                for note in notes:
                    yield "   %s\n" % (note.strip())


def authenticate(frob):
    api = milky.API(API_KEY, API_SECRET, frob=frob)
    if frob is not None: # verify the frob
        try:
            token = api.get_token()
            return api # good frob
        except:
            api.frob = None # bad frob
    bottle.redirect(api.get_auth_url())
    return None

def orgify_tags(tags):
    if len(tags):
        return ":%s:" % ":".join(tags)
    return ""

def fix_tags(tags):
    """ There's a bug in the milky tags type where if there's only one tag, it comes up as a
    list of characters """
    if all(len(a) == 1 for a in tags):
        s = "".join(tags)
        return [ s ] if len(s) > 0 else [ ]
    return tags



if __name__ == "__main__":
    bottle.debug()
    bottle.run(host='localhost', port=8000)
