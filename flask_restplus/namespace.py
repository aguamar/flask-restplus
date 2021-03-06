# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Namespace(object):
    '''
    Group resources together

    :param Api api: The API on which the namespace is attached
    :param str name: The namespace name
    :param str description: An optionale short description
    :param str path: An optional prefix path. If not provided, prefix is ``/+name``
    '''
    def __init__(self, api, name, description=None, endpoint=None, path=None, **kwargs):
        self.api = api
        self.name = name
        self.path = path or ('/' + name)
        self.description = description
        self.resources = {}
        self.models = []

    def add_resource(self, resource, *urls, **kwargs):
        endpoint = self.api.add_resource(resource, *urls, namespace=self, **kwargs)
        self.resources[endpoint] = (resource, urls, kwargs)
        return endpoint

    def route(self, *urls, **kwargs):
        def wrapper(cls):
            doc = kwargs.pop('doc', None)
            if doc is not None:
                self.api._handle_api_doc(cls, doc)
            self.add_resource(cls, *[self.path + url for url in urls], **kwargs)
            return cls
        return wrapper
