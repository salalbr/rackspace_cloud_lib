#!/usr/bin/python

''' cloud_lib.py - Driver to test library methods '''

__author__ = 'Maer Melo'
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1'
__email__ = 'salalbr@gmail.com'

import os, pyrax, sys

def get_servers(location = 'all'):
  region_list = {}
  if location == 'all':
    for temp_reg in pyrax.regions:
      for server in pyrax.connect_to_cloudservers(region=temp_reg).servers.list():
        region_list[server.name] = [ server.name, server.id, server.status, temp_reg ]
  else:
    for server in pyrax.connect_to_cloudservers(region=location).servers.list():
      region_list[server.name] = [ server.name, server.id, server.status, location ]
  return region_list
  
def get_server_flavors():
  flavors = {}
  for flavor in pyrax.cloudservers.flavors.list():
    flavors[flavor.id] = [ flavor.id, flavor.name, flavor.ram, flavor.disk, flavor.vcpus ]
  return flavors
  
def get_server_images():
  images = {}
  for image in pyrax.cloudservers.images.list():
    images[image.id] = [ image.id, image.name ]
  return images
  
def create_server(server_name, image_id, flavor_id):
  server = {}
  instance = pyrax.cloudservers.servers.create(server_name, image_id, flavor_id)
  server['name'] = instance.name
  server['id'] = instance.id  
  server['status'] = instance.status
  server['adminpass'] = instance.adminPass
  server['networks'] = instance.networks  
  return server

def delete_server(server_name):
  try:
    sacrifice = pyrax.cloudservers.servers.find(name=server_name)
  except Exception as e:
    print 'Error: could not find server ', server_name
    return False
  if sacrifice.status == 'ACTIVE':
    sacrifice.delete()
    return True
  else:
    print 'Error: server in an unknown state!'
    return False

def print_dict_options(dict, result=False):
  index = {}
  index_num = 0
  for key in dict:
    print '[' + str(index_num) + ']\t',
    index[index_num] = dict[key][0]
    index_num += 1
    for i in range(len(dict[key])):
      print dict[key][i], '\t',
    print
  if result == True:  
    return index

def main():
  pyrax.set_setting('identity_type', 'rackspace')
  creds_file = os.path.expanduser('./cloud_credentials.conf')
  pyrax.set_credential_file(creds_file)

  # Driver
  while(True):
    os.system('clear')
    option = raw_input('--Options:\n1) List servers\n2) Create server\n3) Delete server\n4) Quit\n\nType your option: ')[0].lower()
    if option == '4' or option == 4 or option == 'q':
      sys.exit(0)
    elif option == '1' or option == 1:
      servers = get_servers()
      print '\n... Listing servers:'
      print_dict_options(servers)
      raw_input('\n *** Press Enter to continue ***')
      
    elif option == '2' or option == 2:
      print '--Create server:'
      server_name_option = raw_input('Server name: ').lower()
      images = get_server_images()
      images_index = print_dict_options(images, True)
      image_option = raw_input('Image #: ').lower()
      flavors = get_server_flavors()
      flavors_index = print_dict_options(flavors, True)
      flavors_option = raw_input('Flavor #: ').lower()
      print '\n--Server details:'
      server = create_server(server_name_option, images_index[int(image_option)], flavors_index[int(flavors_option)])
      print server
      raw_input('\n *** Press Enter to continue ***')
    elif option == '3' or option == 3:
      print '\n--Servers currently deployed:'
      servers = get_servers()
      print_dict_options(servers)
      delete_server_option = raw_input('\nEnter server name you wish to delete: ').lower()
      result = delete_server(delete_server_option)
      if result == True:
        '*** Server ', delete_server_option, ' has been successfully deleted!'
      raw_input('\n *** Press Enter to continue ***')
  
if __name__ == '__main__':
  main()
