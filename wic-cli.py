#!/usr/bin/env python

import argparse
import configparser
import os

import requests
import json

import http.client
import mimetypes
from codecs import encode

def org_set(args):
    Commands(args).org_set()

def group_get(args):
    Commands(args).group_get()

def group_add(args):
    Commands(args).group_add()

def group_delete(args):
    Commands(args).group_delete()

def group_list(args):
    Commands(args).group_list()

def user_list(args):
    Commands(args).user_list()

def user_deactivate(args):
    Commands(args).user_deactivate()

def user_activate(args):
    Commands(args).user_activate()

def user_get(args):
    Commands(args).user_get()

def user_add(args):
    Commands(args).user_add()

def user_delete(args):
    Commands(args).user_delete()

def apps_list(args):
    Commands(args).apps_list()

def apps_get(args):
    Commands(args).apps_get()

def apps_assign(args):
    Commands(args).apps_assign()

def apps_remove(args):
    Commands(args).apps_remove()

def command_help(args):
    print(parser.parse_args([args.command, '--help']))

def user_help(args):
    print(parser.parse_args([args.command, '--help']))

class Headers:

    def __init__(self,key,boundary,cookie):
        self.key = key
        self.boundary = boundary
        self.cookie = cookie

    def Get(self):
        headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'SSWS {}'.format(self.key),
          'Content-type': 'multipart/form-data; boundary={}'.format(self.boundary),
          'Cookie': '{}'.format(self.cookie)
        }
        return headers

    def Get_no_boundary(self):
        headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'SSWS {}'.format(self.key),
          'Cookie': '{}'.format(self.cookie)
        }
        return headers

class Payload:

    def __init__(self,idx,first,last,domain,pw):
    	self.idx = idx
    	self.first = first
    	self.last = last
    	self.domain = domain
    	self.pw = pw

    def Set(self):
        json_data = {"profile": {
                         "firstName": self.first+self.idx,
			 "lastName": self.last,
			 "email": self.first+self.idx+"."+self.last+"@"+self.domain,
			 "login": self.first+self.idx+"."+self.last+"@"+self.domain,
			 },
			 "credentials": {
			      "password": {
	 		          "value": self.pw
		     	       }
			    }
			 }
        return json_data

class gPayload:

    def __init__(self,idx,name):
    	self.idx = idx
    	self.name = name
    	self.description = name	

    def Set(self):
        json_data = {"profile": {
                         "name": self.name+self.idx,
			 "description": self.name+self.idx,
			 }
                     }
        return json_data

class app_assign_Payload:

    def __init__(self,id,name):
    	self.user_id = id
    	self.user_name = name

    def Set(self):
        json_data = {"id": self.user_id,
                     "scope": "USER",
                     "credentials": {
                        "userName": self.user_name
                        }
                     }

        return json_data

class Http:

    def __init__(self, o):
        self.o = o

    def Connect(self):
        co = http.client.HTTPSConnection(self.o)
        return co

    def Get(self,con,url):
        self.con = con
        self.url = url
        boundary = ''
        h = Headers(key,'','')
        headers = h.Get()
        self.con.request('GET', self.url, '', headers)
        r = self.con.getresponse()
        d = r.read()
        return d

    def Delete(self,con,url):
        self.con = con
        self.url = url
        boundary = ''
        h = Headers(key,'','')
        headers = h.Get()
        self.con.request('DELETE', self.url, '', headers)
        r = self.con.getresponse()
        d = r.read()
        return d

    def Post(self,con,url,pay):
        self.con = con
        self.url = url
        self.pay = pay

        boundary = ''
        h = Headers(key,'','')
        headers = h.Get_no_boundary()
        #headers = h.Get()
        self.con.request('POST', self.url, self.pay, headers)
        r = self.con.getresponse()
        d = r.read()
        return d
    

class Commands:
    def __init__(self, args):
        self.args = args

    def org_set(self):
        print(self.args.org)

    def user_list(self):
        full = self.args.full
	
        url = '/api/v1/groups?expand=stats'
        http = Http(org_name)
        conn = http.Connect()
        data = http.Get(conn,url)

        dict = json.loads(data.decode("utf-8"))
        for i in range(len(dict)):
               if(dict[i]["profile"]["name"] == 'Everyone'):
                   usersCount = dict[i]["_embedded"]["stats"]["usersCount"]

        cmd = 'GET'
        url = '/api/v1/users?limit='.format(usersCount)
        data = http.Get(conn,url)

        dict = json.loads(data.decode("utf-8"))
        for i in range(len(dict)):
           if(full):
               print("{} {} {} {} {}".format(
                    dict[i]["id"],
                    dict[i]["status"],
                    dict[i]["profile"]["login"],
                    dict[i]["credentials"]["provider"]["type"],
                    dict[i]["credentials"]["provider"]["name"]
                    ))
           else:
               print("{} {} {}".format(
                    dict[i]["id"],
                    dict[i]["status"],
                    dict[i]["profile"]["login"],
                    ))

        cmd = 'GET'
        url = '/api/v1/users?filter=status%20eq%20%22DEPROVISIONED%22&limit={}'.format(usersCount)
        data = http.Get(conn,url)

        dict = json.loads(data.decode("utf-8"))
        for i in range(len(dict)):
           if(full):
               print("{} {} {} {} {}".format(
                    dict[i]["id"],
                    dict[i]["status"],
                    dict[i]["profile"]["login"],
                    dict[i]["credentials"]["provider"]["type"],
                    dict[i]["credentials"]["provider"]["name"]
                    ))
           else:
               print("{} {} {}".format(
                    dict[i]["id"],
                    dict[i]["status"],
                    dict[i]["profile"]["login"],
                    ))

    def group_list(self):
        full = self.args.full
	
        url = '/api/v1/groups?expand=stats'
        http = Http(org_name)
        conn = http.Connect()
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        for i in range(len(dict)):
            if(full):
              print("{} {} {} usersCount:{}".format(
              #print("{} {} {} usersCount:{} appsCount:{} groupPushMappingsCount:{} hasAdminPrivilege:{}".format(
              dict[i]["id"],
              dict[i]["profile"]["name"],
              dict[i]["type"],
              dict[i]["_embedded"]["stats"]["usersCount"],
              #dict[i]["_embedded"]["stats"]["appsCount"],
              #dict[i]["_embedded"]["stats"]["groupPushMappingsCount"],
              #dict[i]["_embedded"]["stats"]["hasAdminPrivilege"]
              ))
            else:
              print("{} {}".format(dict[i]["id"],dict[i]["profile"]["name"]))

    def group_get(self):
        group_name = self.args.name

        url = '/api/v1/groups?expand=stats'
        http = Http(org_name)
        conn = http.Connect()
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        for i in range(len(dict)):
                if dict[i]["profile"]["name"] == group_name:
                   print("{} {}".format(dict[i]["id"],dict[i]["profile"]["name"]))

    def getusernamebyid(self):
        print(self.args.user)

    def getgroupnamebyid(self):
        print(self.args.user)

    def user_get(self):
        user_name =  self.args.name

        url = '/api/v1/users?filter=profile.login%20eq%20%22{}%22'.format(user_name)
        http = Http(org_name)
        conn = http.Connect()
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        for i in range(len(dict)):
            if dict[i]["profile"]["login"] == user_name:
               print("{} {} {} {} {}".format(
                    dict[i]["id"],
                    dict[i]["status"],
                    dict[i]["profile"]["login"],
                    dict[i]["credentials"]["provider"]["type"],
                    dict[i]["credentials"]["provider"]["name"]
                    ))

    def user_deactivate(self):
        user_name =  self.args.name

        url = '/api/v1/users/?filter=profile.login%20eq%20%22{}%22'.format(user_name)
        http = Http(org_name)
        conn = http.Connect()
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        if(dict):
          status = dict[0]["status"] 
        else:
          print("{} is not found".format(user_name))
          exit(1)

        if(status == 'DEPROVISIONED'):
                 print("{} is already DEPROVISIONED".format(user_name))
                 exit(1)

        for i in range(len(dict)):
                if dict[i]["profile"]["login"] == user_name:
                        user_id = dict[i]["id"]
                        status = dict[i]["status"]

        url = '/api/v1/users/{}/lifecycle/deactivate'.format(user_id)
        payload = ''
        data = http.Post(conn,url,payload)
        dict = json.loads(data.decode("utf-8"))

    def user_activate(self):
        user_name =  self.args.name

        url = '/api/v1/users/?filter=profile.login%20eq%20%22{}%22'.format(user_name)
        http = Http(org_name)
        conn = http.Connect()
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        if(dict):
          status = dict[0]["status"] 
        else:
          print("{} is not found".format(user_name))
          exit(1)

        if(status == 'ACTIVATED'):
                 print("{} is already ACTIVATED".format(user_name))
                 exit(1)

        for i in range(len(dict)):
                if dict[i]["profile"]["login"] == user_name:
                        user_id = dict[i]["id"]
                        user_status = dict[i]["status"]

        url = '/api/v1/users/{}/lifecycle/activate?sendEmail=false'.format(user_id)
        payload = ''
        data = http.Post(conn,url,payload)
        if(any(data)):
           dict = json.loads(data.decode("utf-8"))
           #print(data.decode("utf-8"))
           if(dict.get('errorCode')):
              #print("{} errorId: {}".format(dict["errorCauses"][0]["errorSummary"],dict["errorId"]))        
              print("{} errorId: {}".format(dict["errorSummary"],dict["errorId"]))           
           else:
              print("{} ({}) has been activated, userId: {} activationUrl: {}".format(user_name,user_status,user_id,dict["activationUrl"]))

    def user_delete(self):
        user_name =  self.args.name

        http = Http(org_name)
        conn = http.Connect()

        for u in user_name:

            url = '/api/v1/users/?filter=profile.login%20eq%20%22{}%22'.format(u)
            data = http.Get(conn,url)
            dict = json.loads(data.decode("utf-8"))

            if(not dict):
              print("{} is not found".format(u))
              continue
    
            for i in range(len(dict)):
                    if dict[i]["profile"]["login"] == u:
                            user_id = dict[i]["id"]
                            user_status = dict[i]["status"]

            if (user_status == "DEPROVISIONED"):
               url = '/api/v1/users/{}'.format(user_id)
               data = http.Delete(conn,url)
               #print(data.decode("utf-8"))
               if(any(data)):
                 dict = json.loads(data.decode("utf-8"))
                 if(dict.get('errorCode')):
                     print("{} errorId: {}".format(dict["errorSummary"],dict["errorId"]))
                 else:
                     print("{} ({}) has been deleted, userId: {}".format(u,user_status,user_id))
               else:
                 print("{} ({}) has been deleted, userId: {}".format(u,user_status,user_id))

            if(self.args.force and (user_status == "ACTIVE" or 
                                    user_status == "STAGED" or
				    user_status == "PROVISIONED" or
				    user_status == "PASSWORD_EXPIRED" or				    
				    user_status == "RECOVERY" )):
               url = '/api/v1/users/{}/lifecycle/deactivate'.format(user_id)
               payload = ''
               data = http.Post(conn,url,payload)
               url = '/api/v1/users/{}'.format(user_id)
               data = http.Delete(conn,url)
               #print(data.decode("utf-8"))

               # delete is scceeded, it will be retrun null
               if(any(data)):
                   dict = json.loads(data.decode("utf-8"))
                   if(dict.get('errorCode')):
                      print("{} errorId: {}".format(dict["errorCauses"][0]["errorSummary"],dict["errorId"]))        
                      #print("{} errorId: {}".format(dict["errorSummary"],dict["errorId"]))           
               else:
                   print("{} ({}) has been deleted, userId: {}".format(u,user_status,user_id))
         
    def group_delete(self):
        group_name =  self.args.name
          
        http = Http(org_name)
        conn = http.Connect()

        for g in group_name:

            url = '/api/v1/groups?search=profile.name%20eq%20%22{}%22'.format(g)
            data = http.Get(conn,url)
            dict = json.loads(data.decode("utf-8"))

            if(not dict):
              print("{} is not found".format(g))
              continue

            for i in range(len(dict)):
                    if dict[i]["profile"]["name"] == g:
                       group_id = dict[i]["id"]
   
            url = '/api/v1/groups/{}'.format(group_id)
            data = http.Delete(conn,url)

            # delete is scceeded, it will be retrun null
            if(any(data)):
               dict = json.loads(data.decode("utf-8"))
               if(dict.get('errorCode')):
                  print("{} errorId: {}".format(dict["errorCauses"][0]["errorSummary"],dict["errorId"]))
            else:
               print("{} has been deleted, userId: {}".format(g,group_id))

    def user_add(self):
        if(self.args.index):
            index = self.args.index
        else:
            index = ''
        firstname = self.args.firstname
        lastname = self.args.lastname
        domain = self.args.domain
        passwd = self.args.passwd

        url = '/api/v1/users?activate=true'
        http = Http(org_name)
        pl = Payload(index,firstname,lastname,domain,passwd)
        conn = http.Connect()
        payload = json.dumps(pl.Set())
        data = http.Post(conn,url,payload)
        dict = json.loads(data.decode("utf-8"))

        if(dict.get('errorCode')):
             print("{} errorId: {}".format(dict["errorCauses"][0]["errorSummary"],dict["errorId"]))
        else:  
             print("{} has been created, userId: {}".format(dict["profile"]["login"], dict["id"],))

    def group_add(self):
        if(self.args.index):
             index = self.args.index
        else:
             index = ''
        name = self.args.name

        url = '/api/v1/groups'
        http = Http(org_name)
        pl = gPayload(index,name)
        conn = http.Connect()
        payload = json.dumps(pl.Set())
        data = http.Post(conn,url,payload)
        dict = json.loads(data.decode("utf-8"))

        if(dict.get('errorCode')):
             print("{} errorId: {}".format(dict["errorCauses"][0]["errorSummary"],dict["errorId"]))
        else:  
             print("{} has been created, groupId: {}".format(dict["profile"]["name"], dict["id"],))

    def apps_list(self):

        http = Http(org_name)
        conn = http.Connect()

        url = '/api/v1/apps'
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        for i in range(len(dict)):
            print("{} {} \"{}\" ({})".format(
                 dict[i]["id"],
                 dict[i]["status"],
                 dict[i]["label"],
                 dict[i]["name"]
                 ))

    def apps_get(self):
        user_name =  self.args.user
        app_name =  self.args.app	

        http = Http(org_name)
        conn = http.Connect()

        if(user_name):
            url = '/api/v1/users/?filter=profile.login%20eq%20%22{}%22'.format(user_name)
            data = http.Get(conn,url)
            dict = json.loads(data.decode("utf-8"))

            if(not dict):
              print("{} is not found".format(user_name))
              exit(1)
        
            for i in range(len(dict)):
                    if dict[i]["profile"]["login"] == user_name:
                            user_id = dict[i]["id"]
                            user_status = dict[i]["status"]

            url = '/api/v1/apps?filter=user.id+eq+%22{}%22&expand=user/{}'.format(user_id,user_id)
            data = http.Get(conn,url)
            dict = json.loads(data.decode("utf-8"))
 
            for i in range(len(dict)):
                   print("{} {} \"{}\" ({})".format(
                         dict[i]["id"],
                         dict[i]["status"],
                         dict[i]["label"],
                         dict[i]["name"]
                 ))

        if(app_name):
           url = '/api/v1/apps'
           data = http.Get(conn,url)
           dict = json.loads(data.decode("utf-8"))
           for i in range(len(dict)):
               if(dict[i]["label"] == app_name):
                   app_id = dict[i]["id"]

           url = '/api/v1/apps/{}/users'.format(app_id)
           data = http.Get(conn,url)
           dict = json.loads(data.decode("utf-8"))
#           print(data.decode("utf-8"))
           for i in range(len(dict)):
             if(dict[i]["credentials"]):
                print("{}".format(
                      dict[i]["credentials"]["userName"]
                      ))
             else:
                # for admin console (fixme)
                print("user assiged {}".format(dict[i]["_links"]["user"]["href"]))


    def apps_assign(self):
        user_name =  self.args.user
        app_name =  self.args.app	
        app_already_assigned = 0

        http = Http(org_name)
        conn = http.Connect()

        url = '/api/v1/users/?filter=profile.login%20eq%20%22{}%22'.format(user_name)
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        if(not dict):
            print("{} is not found".format(user_name))
            exit(1)
       
        for i in range(len(dict)):
            if dict[i]["profile"]["login"] == user_name:
                 user_id = dict[i]["id"]
                 user_status = dict[i]["status"]

        url = '/api/v1/apps?filter=user.id+eq+%22{}%22&expand=user/{}'.format(user_id,user_id)
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        for i in range(len(dict)):
            if(dict[i]["label"] == app_name):
              print("{} is already assigned to {}".format(user_name,app_name)) 
              exit(1)

        url = '/api/v1/apps'
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))
        for i in range(len(dict)):
            if(dict[i]["label"] == app_name):
               app_id = dict[i]["id"]

        url = '/api/v1/apps/{}/users'.format(app_id) 
        pl = app_assign_Payload(user_id,user_name)
        conn = http.Connect()
        payload = json.dumps(pl.Set())
        data = http.Post(conn,url,payload)
        print("{} is assigned to {}".format(user_name,app_name)) 
        # fixme
        #dict = json.loads(data.decode("utf-8"))
        #print(data.decode("utf-8"))

    def apps_remove(self):
        user_name =  self.args.user
        app_name =  self.args.app	
        app_assigned = 0

        http = Http(org_name)
        conn = http.Connect()

        url = '/api/v1/users/?filter=profile.login%20eq%20%22{}%22'.format(user_name)
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))

        if(not dict):
            print("{} is not found".format(user_name))
            exit(1)
       
        for i in range(len(dict)):
            if dict[i]["profile"]["login"] == user_name:
                 user_id = dict[i]["id"]
                 user_status = dict[i]["status"]

        url = '/api/v1/apps?filter=user.id+eq+%22{}%22&expand=user/{}'.format(user_id,user_id)
        data = http.Get(conn,url)
        dict = json.loads(data.decode("utf-8"))
 
        for i in range(len(dict)):
            if(dict[i]["label"] == app_name):
              app_id = dict[i]["id"]
              app_assigned = 1
  
        if(app_assigned == 0):
             print("{} is not assigned to {}".format(user_name,app_name)) 
             exit(1)

        url = '/api/v1/apps/{}/users/{}'.format(app_id,user_id) 
        data = http.Delete(conn,url)
        if(not data):
              print("{} is unassigned to {}".format(user_name,app_name)) 
        else: 
              # fixme
              dict = json.loads(data.decode("utf-8"))
              print(data.decode("utf-8"))
              print("{} unable to unassigned to {}".format(user_name,app_name)) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--org', action='store', help='option org')
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=org_set)

    parser_user = subparsers.add_parser('user', help='parser user')
    subparser_user = parser_user.add_subparsers()

    parser_user_list = subparser_user.add_parser('list')
    parser_user_list.add_argument('--full', action='store_true', help='option full')
    parser_user_list.set_defaults(func=user_list)

    parser_user_get = subparser_user.add_parser('get')
    parser_user_get.add_argument('--name', action='store', help='option name')
    parser_user_get.set_defaults(func=user_get)

    parser_user_add = subparser_user.add_parser('add')
    parser_user_add.add_argument('--index', action='store', help='option index')
    parser_user_add.add_argument('--firstname', action='store', help='option firstname')
    parser_user_add.add_argument('--lastname', action='store', help='option lastname')
    parser_user_add.add_argument('--domain', action='store', help='option domain')
    parser_user_add.add_argument('--passwd', action='store', help='option')    
    parser_user_add.set_defaults(func=user_add)

    parser_user_activate = subparser_user.add_parser('activate')
    parser_user_activate.add_argument('--name', action='store', help='option name')
    parser_user_activate.set_defaults(func=user_activate)

    parser_user_deactivate = subparser_user.add_parser('deactivate')
    parser_user_deactivate.add_argument('--name', action='store', help='option name')
    parser_user_deactivate.set_defaults(func=user_deactivate)

    parser_user_delete = subparser_user.add_parser('delete')
    parser_user_delete.add_argument('--name', action='store', nargs='*', help='option name')
    parser_user_delete.add_argument('--force', action='store_true', help='option force')    
    parser_user_delete.set_defaults(func=user_delete)

    parser_group = subparsers.add_parser('group', help='parser group')
    subparser_group = parser_group.add_subparsers()

    parser_group_list = subparser_group.add_parser('list')
    parser_group_list.add_argument('--full', action='store_true', help='option full')
    parser_group_list.set_defaults(func=group_list)

    parser_group_get = subparser_group.add_parser('get')
    parser_group_get.add_argument('--name', action='store', help='option name')
    parser_group_get.set_defaults(func=group_get)

    parser_group_add = subparser_group.add_parser('add')
    parser_group_add.add_argument('--name', action='store', help='option name')
    parser_group_add.add_argument('--index', action='store', help='option index')    
    parser_group_add.set_defaults(func=group_add)

    parser_group_delete = subparser_group.add_parser('delete')
    parser_group_delete.add_argument('--name', action='store', nargs='*', help='option name')
    parser_group_delete.set_defaults(func=group_delete)

    parser_apps = subparsers.add_parser('apps', help='parser pass')
    subparser_apps = parser_apps.add_subparsers()

    parser_apps_list = subparser_apps.add_parser('list')
    parser_apps_list.set_defaults(func=apps_list)

    parser_apps_get = subparser_apps.add_parser('get')
    parser_apps_get.add_argument('--full', action='store_true', help='option full')
    parser_apps_get.add_argument('--user', action='store', help='option user')
    parser_apps_get.add_argument('--app', action='store', help='option app')        
    parser_apps_get.set_defaults(func=apps_get)

    parser_apps_assign = subparser_apps.add_parser('assign')
    parser_apps_assign.add_argument('--user', action='store', help='option user')
    parser_apps_assign.add_argument('--app', action='store', help='option app')        
    parser_apps_assign.set_defaults(func=apps_assign)

    parser_apps_remove = subparser_apps.add_parser('remove')
    parser_apps_remove.add_argument('--user', action='store', help='option user')
    parser_apps_remove.add_argument('--app', action='store', help='option app')        
    parser_apps_remove.set_defaults(func=apps_remove)

    parser_help = subparsers.add_parser('help', help='see `help -h`')
    parser_help.add_argument('command', help='command name which help is shown')
    parser_help.set_defaults(func=command_help)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
       parser.print_help()
       exit(1)

    config_dir = os.path.expanduser("~") 
    config_file = config_dir + "/.wicrc"

    rc = configparser.ConfigParser()
    rc.read(config_file, encoding='utf-8')

    if(args.org):
      config = rc[args.org]
    else:
      config = rc['default']

    org_name = config.get('org')
    key = config.get('key')
    firstname = config.get('firstname')
    lastname = config.get('lastname')
    domain = config.get('domain')
    passwd = config.get('passwd')

#    print("org: {}".format(org_name))

    try:
        func = args.func
    except AttributeError:
        parser.error('too few arguments')
    func(args)
