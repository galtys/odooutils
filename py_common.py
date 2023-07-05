import sys
import os
import hashlib
import psycopg2
import psycopg2.extras
import pprint
import toml
import sys

sys.setrecursionlimit(10000)



#server_path=None
#config_file=None

def import_openerp7_server(server_path, config_file):
   #global server_path
   #global config_file
   if os.path.isdir(server_path):   
          sys.path.append(server_path)
          import openerp
          import openerp.tools.config
          import openerp.service.web_services
          openerp.tools.config.parse_config(['--config=%s' % config_file])
          from openerp import netsvc
          from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
          from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT    
          #import html_reports.controllers.main as r_main
          import galtyslib.openerplib as openerplib
          from openerp.osv import fields, osv
          global openerplib
          global DEFAULT_SERVER_DATE_FORMAT
          global DEFAULT_SERVER_DATETIME_FORMAT
          global netsvc
          return 1
   return 0 
        
#if __name__ == '__main__':
#    server_path='/home/jan/github.com/migrated_pjb70'
#    config_file='/home/jan/projects/server_pjbrefct.conf'
#    import_openerp7_server(server_path, config_file)
          
#def set_server_path(p):
#    global server_path
#    server_path = p
#def set_config_path(p):
#    global config_file
#    config_file = p


def get_connection7(db):
    pool, cr, uid = openerplib.get_connection(db)

    return {'pool':pool, 'cr':cr, 'uid':uid}
#def split_sku(sku):
#    sku.split('_')
def close_connection7(env7):
   env7['cr'].commit()
   env7['cr'].close()
   
def read_file_as_dict(pth):
    return eval(file(pth).read())
def pretty_xml(s):
    return etree.tostring(etree.fromstring(s),pretty_print=True) 
def resolve_xid(env, model, xid):
    try:
        (res_name, res_id) =env['pool'].get('ir.model.data').get_object_reference(env['cr'], env['uid'], model, xid)
        return res_id
    except:
        return (-1)
#ReturnTriple        
def return_tuple(code, err, msg):
    return (code, err, msg)

def read_one(m,f):
    #print ["read_one", m, f]
    return m[f]

def erp7_create(env, model, data):
    #pprint.pprint(data)
    return model.create( env['cr'], env['uid'], data)
def odoo14_browse(env, model, ids):
    return model.search( [('id','in',ids)])
def get_sha256_hex(a):
    return hashlib.sha256(a.encode('utf8')).hexdigest()

