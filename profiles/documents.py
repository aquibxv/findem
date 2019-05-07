from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from . import models

connections.create_connection()

# connecting post model to engine by subclassing DocType
class ProfileIndex(DocType):
        # specifying the feilds that we want to index
        # from the User Profile model

        college_name = Text()
        name = Text()
        skill_1 = Text()
        skill_2 = Text()
        skill_3 = Text()
        skill_4 = Text()
        skill_5 = Text()
        skill_6 = Text()

        class Meta:
            index = 'profile-index'

def bulk_indexing():
    ProfileIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing()
    for b in models.UserProfile.objects.all().iterator()))