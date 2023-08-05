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

class ConsumerGovernmentID(BaseObject):
    """
    
    """

    __config = {
        
        "d9e2b96e-0d9f-4dfe-997d-23744bd55838" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "create", [], []),
        
        "ac6d4173-3f64-410d-8c8f-3a48dc7b954f" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "delete", [], []),
        
        "32396151-0a11-4412-9c6a-a51cbc45ed83" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "read", [], []),
        
        "2c87f239-7b5c-4291-848a-d37257efe97f" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "query", [], []),
        
        "29390a5f-cbe5-43dd-8f3e-7f286bf4dda0" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerGovernmentID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerGovernmentID of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("d9e2b96e-0d9f-4dfe-997d-23744bd55838", ConsumerGovernmentID(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerGovernmentID by id

        @param str id
        @return ConsumerGovernmentID of the response of the deleted instance.
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

        return BaseObject.execute("ac6d4173-3f64-410d-8c8f-3a48dc7b954f", ConsumerGovernmentID(mapObj))

    def delete(self):
        """
        Delete object of type ConsumerGovernmentID

        @return ConsumerGovernmentID of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("ac6d4173-3f64-410d-8c8f-3a48dc7b954f", self)







    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ConsumerGovernmentID by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerGovernmentID
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

        return BaseObject.execute("32396151-0a11-4412-9c6a-a51cbc45ed83", ConsumerGovernmentID(mapObj))







    @classmethod
    def listAll(cls,criteria):
        """
        Query objects of type ConsumerGovernmentID by id and optional criteria
        @param type criteria
        @return ConsumerGovernmentID object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("2c87f239-7b5c-4291-848a-d37257efe97f", ConsumerGovernmentID(criteria))


    def update(self):
        """
        Updates an object of type ConsumerGovernmentID

        @return ConsumerGovernmentID object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("29390a5f-cbe5-43dd-8f3e-7f286bf4dda0", self)






