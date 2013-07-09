import json
from collections import deque

from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

from keywords.models import Edge, Query


class KeywordForm(forms.Form):
    keyword = forms.CharField()


def home(request):
    keyword = u'\uc3d8\uce74'
    
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        query = Query.objects.get(text=request.POST['keyword'])
    else:
        form = KeywordForm()
        query = Query.objects.get(text=keyword)
    
    graph = {'name': query.text}
    queue = deque([query])
    queue2 = deque([graph])
    visited = set()
    n = 0
    
    while queue:
        n = n + 1
        if n == 110: break
        q = queue.popleft()        
        t = queue2.popleft()
        if q in visited: continue
        children = []
        for edge in Edge.objects.filter(head=q):
            # Add children to the queue            
            if edge.tail not in visited:
                queue.append(edge.tail)
                child = {'name': edge.tail.text}
                queue2.append(child)
                children.append(child)
        if children:
            t['children'] = children
        visited.add(q)
        
    data = json.dumps(graph)

    return render_to_response('graph.html', {
        'data': data, 'form': form,
    }, context_instance=RequestContext(request))
