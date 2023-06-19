import toml
import sys
import psycopg2
import psycopg2.extras
import pprint

sql_is_null="""
select c.table_schema,c.table_name,
       c.column_name,
       case c.is_nullable
            when 'NO' then 'notnull'
            when 'YES' then 'null'
       end as nullable
from information_schema.columns c
join information_schema.tables t
     on c.table_schema = t.table_schema 
     and c.table_name = t.table_name
where c.table_schema not in ('pg_catalog', 'information_schema')
      and t.table_type = 'BASE TABLE' 
order by table_schema,
         table_name,
         column_name;
"""

sql_data_type="""
SELECT
    pg_attribute.attname AS column_name,
    
    pg_catalog.format_type(pg_attribute.atttypid, pg_attribute.atttypmod) AS data_type
FROM
    pg_catalog.pg_attribute
INNER JOIN
    pg_catalog.pg_class ON pg_class.oid = pg_attribute.attrelid
INNER JOIN
    pg_catalog.pg_namespace ON pg_namespace.oid = pg_class.relnamespace
WHERE
    pg_attribute.attnum > 0
    AND NOT pg_attribute.attisdropped
    AND pg_namespace.nspname = 'public'
    AND pg_class.relname = %s
ORDER BY
    attnum ASC;
"""

sql_fkey="""
select 
    att2.attname as "child_column", 
    cl.relname as "parent_table", 
    att.attname as "parent_column",
    conname
from
   (select 
        unnest(con1.conkey) as "parent", 
        unnest(con1.confkey) as "child", 
        con1.confrelid, 
        con1.conrelid,
        con1.conname
    from 
        pg_class cl
        join pg_namespace ns on cl.relnamespace = ns.oid
        join pg_constraint con1 on con1.conrelid = cl.oid
    where
        cl.relname = %s
        and ns.nspname = 'public'
        and con1.contype = 'f'
   ) con
   join pg_attribute att on
       att.attrelid = con.confrelid and att.attnum = con.child
   join pg_class cl on
       cl.oid = con.confrelid
   join pg_attribute att2 on
       att2.attrelid = con.conrelid and att2.attnum = con.parent;
"""

def get_psycopg2_env(conf):
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

if __name__ == '__main__':
  if len(sys.argv)==3:
    conf = sys.argv[1]
    prod= sys.argv[2]
    pg='pg10'
    dsn=toml.load(conf)[pg][prod]    
    schema_map = get_schema(dsn)
    pprint.pprint( schema_map)
  else:
    print "py_schema.py conf.toml dev7"
  #pprint.pprint( get_fkey(cr,'res_partner') )

