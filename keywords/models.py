from django.db import models


class Topic(models.Model):
    # Topic keyword
    keyword = models.CharField(max_length=100)
    # Size of audience for this topic
    audience_size = models.PositiveIntegerField()
    
    def __unicode__(self):
        return '%s: %s' % (self.keyword, audience_size)


class Query(models.Model):
    # The actual text for the query
    text = models.CharField(max_length=100)
    # Topic this query belongs to
    topic = models.ForeignKey(Topic)
    
    def __unicode__(self):
        return self.text


class Edge(models.Model):
    # The head of the edge
    head = models.ForeignKey(Query, related_name='outging_edge_set')
    # The tail of the edge
    tail = models.ForeignKey(Query, related_name='incoming_edge_set')

    def __unicode__(self):
        return self.head.text + '->' + self.tail.text
