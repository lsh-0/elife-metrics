from article_metrics.utils import merge, lmap
from schema import Schema, And, Or, Use as Coerce, Optional, SchemaError
from datetime import datetime, date
from django.conf import settings
import json
import logging
from collections import OrderedDict
from article_metrics.utils import ensure

LOG = logging.getLogger(__name__)

def date_wrangler(v):
    if isinstance(v, str):
        return datetime.strptime(v, "%Y-%m-%d").date()
    return v

def frames_wrangler(frame_list):

    def fill_empties(frame):
        frame['starts'] = frame['starts'] or settings.INCEPTION.date()
        frame['ends'] = frame['ends'] or date.today()
        return frame

    frame_list = lmap(fill_empties, frame_list)
    frame_list = sorted(frame_list, key=lambda f: f['starts']) # ASC

    # TODO: ensure no overlaps between frames

    return frame_list

type_optional_date = Or(Coerce(date_wrangler), None)
type_str = And(str, len) # non-empty string

_frame0 = {
    'starts': type_optional_date,
    'ends': type_optional_date,
    'id': And(Coerce(str), type_str),
    Optional('comment'): type_str
}
_only_one = lambda d: d['starts'] or d['ends']
frame0 = And(_frame0, _only_one) # we can't merge Schemas, which sucks

_frame1 = merge(_frame0, {'prefix': type_str})
frame1 = And(_frame1, _only_one)

# a prefix+path-list lets us generate a query for a finite number of paths
_frame2 = merge(_frame1, {'path-list': [type_str]})
frame2 = And(_frame2, _only_one)

# an explicit pattern to pass to GA as-is
_frame3 = merge(_frame0, {'pattern': type_str})
frame3 = And(_frame3, _only_one)

# similar to prefix+path-list, the keys are used in the query and the
# values are used in the results processing
_frame4 = merge(_frame0, {'path-map': {type_str: str}}) # we allow empty strings here (landing pages)
frame4 = And(_frame4, _only_one)

# similar to path-map, the redirects are read in from a text file
# while `path-map` uses an explicit map of path->ids, 'redirect-prefix' is used here to parse out an `id`.
_frame5 = merge(_frame0, {'path-map-file': type_str, 'redirect-prefix': type_str,
                          Optional('prefix'): type_str, Optional('pattern'): type_str})
frame5 = And(_frame5, _only_one)

type_frame = Or(frame1, frame2, frame3, frame4, frame5)

type_object = Schema({
    'frames': And([type_frame], Coerce(frames_wrangler))
})

type_history = Schema({type_str: type_object})


def load_from_file(history_path=None):
    history_path = history_path or settings.GA_PTYPE_HISTORY_PATH
    try:
        history_data = json.load(open(history_path, 'r'), object_pairs_hook=OrderedDict)
        return type_history.validate(history_data)
    except SchemaError as err:
        LOG.error("history is invalid: %s", str(err))
        raise

def ptype_history(ptype, history=None):
    history = history or load_from_file()
    ensure(ptype in history, "no historical data found: %s" % ptype, ValueError)
    return history[ptype]
