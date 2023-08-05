#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercarddisbursements import ResourceConfig

class Consumer(BaseObject):
    """
    
    """

    __config = {
        
        "949604d4-9180-4562-a63c-c07713256c47" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "delete", [], []),
        
        "37dfaaf1-90ab-49d5-8155-25eadbae1524" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "create", [], []),
        
        "e30bcea1-5e52-4c13-bfb5-f91057b05589" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "read", [], []),
        
        "4a535316-e30a-484b-b584-c676d5ecdfa6" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "query", [], ["ref","contact_id_uri"]),
        
        "dac8c8a9-17fa-4120-97f0-6b05fa2a8f3f" : OperationConfig("/send/v1/partners/{partnerId}/consumers/search", "create", [], []),
        
        "c82dd3bc-42bb-4097-b3e7-a477a6db4ee4" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())





    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Consumer by id

        @param str id
        @return Consumer of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("949604d4-9180-4562-a63c-c07713256c47", Consumer(mapObj))

    def delete(self):
        """
        Delete object of type Consumer

        @return Consumer of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("949604d4-9180-4562-a63c-c07713256c47", self)



    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("37dfaaf1-90ab-49d5-8155-25eadbae1524", Consumer(mapObj))










    @classmethod
    def readByID(cls,id,criteria=None):
        """
        Returns objects of type Consumer by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Consumer
        @raise ApiException: raised an exception from the response status
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("e30bcea1-5e52-4c13-bfb5-f91057b05589", Consumer(mapObj))







    @classmethod
    def listByReferenceOrContactID(cls,criteria):
        """
        Query objects of type Consumer by id and optional criteria
        @param type criteria
        @return Consumer object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("4a535316-e30a-484b-b584-c676d5ecdfa6", Consumer(criteria))

    @classmethod
    def listByReferenceContactIDOrGovernmentID(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("dac8c8a9-17fa-4120-97f0-6b05fa2a8f3f", Consumer(mapObj))







    def update(self):
        """
        Updates an object of type Consumer

        @return Consumer object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("c82dd3bc-42bb-4097-b3e7-a477a6db4ee4", self)






