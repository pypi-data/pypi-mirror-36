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
from mastercardmastercom import ResourceConfig

class Claims(BaseObject):
    """
    
    """

    __config = {
        
        "03cac89a-7df0-4fe9-97ee-6fdc415e8302" : OperationConfig("/mastercom/v3/claims", "create", [], []),
        
        "9f39cb5d-2a28-4cfa-b9ec-2e9b605941ac" : OperationConfig("/mastercom/v3/claims/{claim-id}", "read", [], []),
        
        "7be12c46-2217-4b9d-94d6-6b0689f47dc9" : OperationConfig("/mastercom/v3/claims/{claim-id}", "update", [], []),
        
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
        Creates object of type Claims

        @param Dict mapObj, containing the required parameters to create a new object
        @return Claims of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("03cac89a-7df0-4fe9-97ee-6fdc415e8302", Claims(mapObj))










    @classmethod
    def retrieve(cls,id,criteria=None):
        """
        Returns objects of type Claims by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Claims
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

        return BaseObject.execute("9f39cb5d-2a28-4cfa-b9ec-2e9b605941ac", Claims(mapObj))



    def update(self):
        """
        Updates an object of type Claims

        @return Claims object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("7be12c46-2217-4b9d-94d6-6b0689f47dc9", self)






