from mygpo.core.models import Podcast, PodcastGroup

def search_wrapper(result):
    doc = result['doc']
    if doc['doc_type'] == 'Podcast':
        p = Podcast.wrap(doc)
    elif doc['doc_type'] == 'PodcastGroup':
        p = PodcastGroup.wrap(doc)
    p._id = result['id']
    return p


def search_podcasts(q, limit=20, skip=0):
    db = Podcast.get_db()

    #FIXME current couchdbkit can't parse responses for multi-query searches
    q = q.replace(',', '')

    res = db.search('directory/search', wrapper=search_wrapper,
        include_docs=True, limit=limit, skip=skip, q=q)

    #FIXME: return empty results in case of search backend error
    try:
        return list(res), res.total_rows
    except:
        return [], 0
