import json
from collections import deque

from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from keywords.models import Edge, Query


class KeywordForm(forms.Form):
    keyword = forms.CharField()


def home(request):
    keyword = u'\uc3d8\uce74'
    
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        query = get_object_or_404(Query, text=request.POST['keyword'])
    else:
        form = KeywordForm()
        query = Query.objects.get(text=keyword)
    
    graph = {'name': query.text}
    queue = deque([query])
    queue2 = deque([graph])
    tf = {}
    visited = set()
    n = 0
    
    while queue:
        n = n + 1
        if n == 100: break
        q = queue.popleft()        
        t = queue2.popleft()
        if q in visited: continue
        
        terms = q.text.split(' ')
        for term in terms:
            if tf.has_key(term):
                tf[term] = tf[term] + 1
            else:
                tf[term] = 1
        children = []
        for edge in Edge.objects.filter(head=q):
            # Add children to the queue            
            if edge.head not in visited:
                queue.append(edge.tail)
                child = {'name': edge.tail.text}
                queue2.append(child)
                children.append(child)
        if children:
            t['children'] = children
        visited.add(q)
    
    import operator
    sorted_tf = sorted(tf.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    data = json.dumps(graph)

    return render_to_response('graph.html', {
        'data': data, 'form': form, 'tf': sorted_tf,
    }, context_instance=RequestContext(request))
