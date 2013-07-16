import json
import requests
import xml.etree.ElementTree as et

from collections import deque
from django.conf import settings
from keywords.models import Edge, Query


NAVER_SEARCH_API = 'http://openapi.naver.com/search'

seed = deque([u'\uc3d8\uce74'])

def build_graph(seed):
    graph = {}
    n = 0
    
    while seed:
        n = n + 1
        if n == 5000: break
        nodes = []
        # TODO: make this a priority queue and pop the most interesting keyword 
        query = seed.popleft()
        try:
            Query.objects.get(text=query)
            print '%s is already in the database' % query
            continue
        except Query.DoesNotExist:
            pass
        print 'Popped %s from queue' % query
        payload = {'key': settings.NAVER_SEARCH_API_KEY,
                   'query': query, 'target': 'recmd'}
        while True:
            try:
                r = requests.get(NAVER_SEARCH_API, params=payload, timeout=5)
                break
            except requests.exceptions.Timeout:
                print 'Request timed out after 5 seconds. Trying again...'
        tree = et.fromstring(r.content)
        
        for child in tree.getchildren():
            nodes.append(child.text)
        print 'Adding',
        if query in graph:
            for x in set(nodes) - graph[query] - set(graph.keys()): print x+',',
            graph[query] |= set(nodes)
        else:
            for x in set(nodes) - set(graph.keys()): print x+',',
            graph[query] = set(nodes)
        print 'to the queue'
        seed.extend(set(nodes) - set(seed) - set(graph.keys()))
    return graph


def save_to_model(graph):
    for k, v in graph.iteritems():
        head, created = Query.objects.get_or_create(text=k)
        for w in v:
            tail, created = Query.objects.get_or_create(text=w)
            e = Edge.objects.get_or_create(head=head, tail=tail)


def save_to_json():
    with open('keywords.txt', 'w') as f:
        for query in Query.objects.all():
            values = [edge.head.text for edge in Edge.objects.filter(head=query)]
            json.dump({query.text: values}, f)
