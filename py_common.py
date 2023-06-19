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

def get_psycopg2_env(conf):
  dbname=conf['dbname']
  user=conf['user']
  host=conf['host']
  password=conf['host']
  #dsn =
  conn = psycopg2.connect(**conf)
  #conn = psycopg2.connect("dbname='river_erp7' user='jan' host='localhost' password='Jf3IBqP9'")
  cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  return {'conn':conn, 'cr':cr}

def get_data_type(cr, table):
  dt_map = {}
  cr.execute(sql_data_type, (table,) )
  ret = cr.fetchall()
  for x in ret:
    dt_map[ x['column_name'] ] = x['data_type']
  return dt_map
def get_fkey(cr, table):
  fk_map = {}
  cr.execute(sql_fkey, (table,) )
  ret = cr.fetchall()
  for x in ret:
    fk_map[ x['child_column'] ] = x['parent_table']
  return fk_map
  #return list(ret)

def get_schema(dsn):
   env = get_psycopg2_env(dsn)
   cr = env['cr']
   conn=env['conn']
   is_null_map = {}
   cr.execute(sql_is_null)
   
   ret = cr.fetchall()
   for x in ret:
       table = x['table_name']
       column = x['column_name']
       nullable = x['nullable']

       #is_null_map[ (table, column) ] = nullable
       v = is_null_map.setdefault( table , [] )
       v.append( (column,nullable) )
   #
   schema_map = {}
   for table, cols in is_null_map.items():
       dt_map = get_data_type(cr, table)
       fk_map = get_fkey(cr,table)
       v=schema_map.setdefault(table, [])
       for (c,isn) in cols:
           val = {'column_name':c
                  ,'nullable':isn
                  ,'data_type':dt_map[c]
                  ,'parent_table':fk_map.get(c)
                  }
           v.append(val)
   #cr.commit()           
   conn.close()
   return schema_map
