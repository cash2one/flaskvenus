import datetime
from mongoengine import (Document, DynamicDocument, EmbeddedDocument,LongField, SequenceField, DictField,
                        BooleanField, IntField, StringField, ListField, ReferenceField,GenericReferenceField, 
                        EmbeddedDocumentField, DateTimeField, GeoPointField , connect)

class City(Document):
    id = IntField(primary_key=True, unique=True,  required=True)
    province = StringField()
    name=StringField()
    city=StringField()
    

    
