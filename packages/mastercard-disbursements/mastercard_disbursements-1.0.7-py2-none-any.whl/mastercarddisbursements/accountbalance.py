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

class AccountBalance(BaseObject):
    """
    
    """

    __config = {
        
        "79e0b8cf-2a54-4e46-b3e4-7f4a3727c413" : OperationConfig("/send/v1/partners/{partnerId}/non-card-tokens/{non-card-tokens}/account-balance", "query", [], []),
        
        "3c7044e0-2cc0-4d2f-95e5-ddcf8d12daff" : OperationConfig("/send/v1/partners/{partnerId}/account-balances", "query", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())







    @classmethod
    def accountBalanceForSpecificAccount(cls,criteria):
        """
        Query objects of type AccountBalance by id and optional criteria
        @param type criteria
        @return AccountBalance object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("79e0b8cf-2a54-4e46-b3e4-7f4a3727c413", AccountBalance(criteria))






    @classmethod
    def accountBalancesForSpecificPartner(cls,criteria):
        """
        Query objects of type AccountBalance by id and optional criteria
        @param type criteria
        @return AccountBalance object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("3c7044e0-2cc0-4d2f-95e5-ddcf8d12daff", AccountBalance(criteria))


