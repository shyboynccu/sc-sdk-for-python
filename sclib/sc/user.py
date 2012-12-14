# Copyright (c) 2012 Trend Micro, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

from sclib.sc.scobject import SCObject
from xml.etree import ElementTree

class User(SCObject):
    def __init__(self, connection):
        SCObject.__init__(self, connection)
        #contact information
        self.firstName = None
        self.lastName = None
        self.email = None
        #account information
        self.account = None
        self.role = None
        #user information
        self.id = None
        self.loginname = None
        self.logintext = None
        self.usertype = None
        self.email = None
        self.href = None
        self.isPending = None
        self.isCurrent = None
        self.authType = None
        self.ssoIdPName = None
        self.isLicensedUser = None
        self.MFAStatus = None
        
    def startElement(self, name, attrs, connection):
        ret = SCObject.startElement(self, name, attrs, connection)
        if ret is not None:
            return ret
        
        if name == 'user':
            for key, value in attrs.items():
                setattr(self, key, value)

            #self.id = attrs['id']
            #self.loginname = attrs['loginname']
            #self.logintext = attrs['logintext']
            #self.email = attrs['email']
            #self.href = attrs['href']
            #self.isPending = attrs['isPending']
            #self.isCurrent = attrs['isCurrent']
            #self.authType = attrs['authType']
            #self.ssoIdPName = attrs['ssoIdPName']
            #self.isLicensedUser = attrs['isLicensedUser']
            #self.MFAStatus = attrs['MFAStauts']
            return self
        elif name == 'account':
            self.account = Account(connection)
            self.account.startElement(name, attrs, connection)
            return self.account
        elif name == 'role':
            self.role = Role(connection)
            self.role.startElement(name, attrs, connection)
            return self.role
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'firstName':
            self.firstName = value
        elif name == 'lastName':
            self.lastName = value
        elif name == 'email':
            self.email = value
        else:
            setattr(self, name, value)
            
    def buildElements(self):
        user = ElementTree.Element('user')
        user.attrib['version'] = '3.5'
        
        #user info
        if self.id: user.attrib['id'] = self.id
        if self.loginname: user.attrib['loginname'] = self.loginname
        if self.logintext: user.attrib['logintext'] = self.logintext
        if self.email: user.attrib['email'] = self.email
        if self.href: user.attrib['href'] = self.href
        if self.isPending: user.attrib['isPending'] = self.isPending
        if self.isCurrent: user.attrib['isCurrent'] = self.isCurrent
        if self.authType: user.attrib['authType'] = self.authType
        if self.ssoIdPName: user.attrib['ssoIdPName'] = self.ssoIdPName
        if self.isLicensedUser: user.attrib['isLicensedUser'] = self.isLicensedUser
        if self.MFAStatus: user.attrib['MFAStauts'] = self.MFAStatus
        
        #contact info
        contact = ElementTree.SubElement(user, 'contact')
        if self.firstName: 
            firstName = ElementTree.SubElement(contact, 'firstName')
            firstName.text = self.firstName
        if self.lastName: 
            firstName = ElementTree.SubElement(contact, 'lastName')
            firstName.text = self.lastName
        if self.email: 
            firstName = ElementTree.SubElement(contact, 'email')
            firstName.text = self.email
        
        #role
        if self.role: user.append(self.role.buildElements())
        if self.account: user.append(self.account.buildElements())
        return user
    
    # ----- functions -----
    def create(self):
        req_element = self.buildElements()
        data = ElementTree.tostring(req_element)

        action = 'user/'
        response = self.connection.make_request(action, data, method='POST')
        return response
    
    def delete(self):
        if self.id is None:
            return None

        data = ElementTree.tostring(self.buildElements())
        action = 'user/' + self.id
        response = self.connection.make_request(action, data, method='POST')
        return response
    
    def get(self):
        if self.id is None:
            return None

        data = ElementTree.tostring(self.buildElements())
        action = 'user/' + self.id
        response = self.connection.make_request(action, data)
        return response
        
    def update(self):
        #TODO - check more fields
        if self.id is None:
            return None

        data = ElementTree.tostring(self.buildElements())
        action = 'user/' + self.id
        response = self.connection.make_request(action, data, method='POST')
        return response



class Account(SCObject):
    def __init__(self, connection):
        SCObject.__init__(self, connection)
        self.name = None
        self.id = None
        
    def startElement(self, name, attrs, connection):
        ret = SCObject.startElement(self, name, attrs, connection)
        if ret is not None:
            return ret
        
        if name == 'account':
            self.id = attrs['id']
            self.name = attrs['name']
        else:
            return None

    def endElement(self, name, value, connection):
        setattr(self, name, value)
            
    def buildElements(self):
        account = ElementTree.Element('account')
        if self.id: account.attrib['id'] = self.id
        if self.name: account.attrib['name'] = self.name
        return account
        
class Role(SCObject):
    def __init__(self,connection):
        SCObject.__init__(self, connection)
        self.MFAStatus = None
        self.name = None
        
    def startElement(self, name, attrs, connection):
        ret = SCObject.startElement(self, name, attrs, connection)
        if ret is not None:
            return ret
        
        if name == 'role':
            self.MFAStatus = attrs['MFAStatus']
            self.name = attrs['name']
        else:
            return None

    def endElement(self, name, value, connection):
        setattr(self, name, value)
            
    def buildElements(self):
        role = ElementTree.Element('role')
        if self.MFAStatus: role.attrib['MFAStatus'] = self.MFAStatus
        if self.name: role.attrib['name'] = self.name
        return role
        
        