#import shopify
import pprint
import sys
import psycopg2
from psycopg2 import Error
#import csv_tools
from galtyslib import py_common
from galtyslib import openerplib
from galtyslib import csv_tools

import requests
import json
import pprint
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import time
import subprocess
import socket
import toml
#import StringIO
import tempfile
import copy
#create SO60605, SO60681, SO60961
from tabulate import tabulate
#need fix: SO60846,
import os

if __name__ == '__main__':
    usage = "usage: python %prog [options] dbname csv_fn\n"
    #parser = optparse.OptionParser(version='0.1', usage=usage)
    conf_fn = '/home/jan/projects/pjb.toml' #sys.argv[1]
    conf = toml.load(conf_fn)
    
    dbx = sys.argv[1] #pjb_live
    if len(sys.argv)==3:
        SHOW_STOCK=1
    else:
        SHOW_STOCK=0
    dsn=dbx
    site_arg = 'retail' #sys.argv[2] #retail    
    erp7=conf['erp7'][dbx]
    dbname = erp7['database']
    server_path = erp7['server_path']
    config_file=erp7['config_file']
    ret=py_common.import_openerp7_server(server_path, config_file)
    pool, cr, uid = py_common.get_connection(dbname)
    #pool, cr, uid = get_connection(dbname)
    #from py_common.sale_order_history_and_corrections import order_tools
    import sale_order_history_and_corrections
    from sale_order_history_and_corrections import order_tools
    from sale_order_history_and_corrections.order_tools_core27 import *
    import functools
    Y0=2025
    Y1=2025
    so_ids = pool.get('sale.order').search(cr,uid,[('date_confirm','>=','%d-09-11'%Y0),
                                                   ('date_confirm','<=','%d-12-31'%Y1),
                                                   ('state','in',['done',
                                                                  'progress',
                                                                  'manual',
                                                                  'invoice_except',
                                                                  'shipping_except'])])
    cnt1=0
    cnt2=0
    so_ids=so_ids[2:4]
    
    cr.execute("select code,id from res_application")
    app_map=dict([x for x in cr.fetchall()])
    erp7_id=app_map['erp7']
    
    cr.execute("select name,id from stock_location")
    location_map=dict([x for x in cr.fetchall()])
    stock_id=location_map['Stock']
    customers_id=location_map['Customers']

    #order states
    cr.execute("select state,id from res_order_state")
    state_map=dict([x for x in cr.fetchall()])
    draft_id=state_map['draft']
    cr.execute("update lines_sale_journal set state_id=%s where state_id is null",(draft_id,))
    cr.execute("update lines_xero_invoice set state_id=%s where state_id is null",(draft_id,))
    cr.execute("update lines_xero_credit_note set state_id=%s where state_id is null",(draft_id,))
    #order_tools.get_whs_lines(line_ids)
    if SHOW_STOCK:
       DELETE=0
       CREATE_SALE=0
       CREATE_PO=0
       INITIAL_COPY=0
       ADD_EVENTS=0
       UPDATE_WHS=0
       UPDATE_SALE=0
    else:
       DELETE=1
       CREATE_SALE=0
       CREATE_PO=1
       INITIAL_COPY=0
       ADD_EVENTS=0
       UPDATE_WHS=0
       UPDATE_SALE=0
        
    #SHOW_STOCK=0
    #update res_partner set name='Customer' where customer=True;
    if DELETE:
        cr.execute("delete from lines_sale_journal")
        cr.execute("delete from sale_journal")
        cr.execute("delete from lines_purchase_journal")
        cr.execute("delete from lines_purchase")
        cr.execute("delete from purchase_journal")
        cr.execute("delete from purchase")
        cr.execute("update res_partner set name='Customer' where customer=True")
        cr.execute("update res_partner set name='Supplier' where supplier=True")
        cr.execute("delete from lines_sale")
        cr.execute("delete from sale")
        cr.execute("delete from lines_whs_picking")
        cr.execute("delete from lines_whs_picking_journal")
        cr.execute("delete from whs_picking_journal")
        cr.execute("delete from whs_picking")
    if SHOW_STOCK:
       header=['SKU','Name','In','Out','On Hand','Forecast']
       header=['SKU','Name','On Hand','Forecast']
       data=[]
       p_ids = pool.get('product.product').search(cr,uid,[])
       for p in pool.get('product.product').browse(cr,uid, p_ids):
           if (p.qty_available2!=0.0) or (p.virtual_available2!=0.0):
               row=[p.default_code, p.name, p.incoming_qty2, p.outgoing_qty2,
                    p.qty_available2, p.virtual_available2]
               row=[p.default_code, p.name,
                    p.qty_available2, p.virtual_available2]               
               data.append(row)    
       ret=tabulate(data,headers=header,tablefmt="grid")
       print ret
    if CREATE_PO:
       val = {'reference':'existing stock',
              'name':'-',
              'date':'2025-10-28',
              'supplier_id':33,
              'line_amount_type':'exclusive'}
       new_id=pool.get('purchase').create(cr,uid,val)
       for so in pool.get('sale.order').browse(cr, uid, so_ids[0:1]):           
           for c in so.sale_confirmation_ids:
               #print 'new_id,c.id: ', new_id, c.id
               plk_l=order_tools.get_xero_lines_new(c.line_ids,'trade','res.order.state')
               act = {'reference':c.name,
                      'state':'draft',
                      #'type':'accrec',
                      #'action':'',
                      'line_amount_type':'exclusive',
                      'currency_code':c.currency_code.id,
                      'purchase_id':new_id
                      }
               act['line_ids']=order_tools.plk_lines_to_xero_lines(cr,None,plk_l,'res.purchase_order.state')
               act=order_tools.convert_to_create(act)
               act_id = pool.get('purchase_journal').create(cr,uid,act)
       pool.get('purchase').update_state(cr,uid,[new_id])
       pool.get('purchase').confirm(cr,uid,[new_id])
       w_id=pool.get('purchase').create_delivery(cr,uid,[new_id])
       for i in range(4):
           pool.get('whs_picking').simulate_move(cr,uid,[w_id])
       w=pool.get('whs_picking').browse(cr,uid,w_id)
       
       #by_state=pool.get('whs_picking').get_lines_by_state(w.whs_picking_journal_ids)
       #done_lines=by_state['done']
       #po_id=w.purchase_null_id.id #target
       pool.get('whs_picking').notify_po(cr,uid,[w_id])
       
           
    if CREATE_SALE:
       for so in pool.get('sale.order').browse(cr, uid, so_ids):           
           val = {'reference':so.name,
                  'name':'-',#so.name,
                  'date':so.date_order,
                  'customer_id':so.partner_id.id,
                  'line_amount_type':so.line_amount_type,
                  'app_id':erp7_id}
           new_id=pool.get('sale').create(cr,uid,val)
           for c in so.sale_confirmation_ids:
               #print 'new_id,c.id: ', new_id, c.id
               plk_l=order_tools.get_xero_lines_new(c.line_ids,'trade','res.order.state')
               #print show_lines(plk_l)
               #number=c.number
               #a=sa.name+'-A%d'%number
               act = {#'name':'-',
                      #'date':c.date,
                      #'state':'draft',
                      #'number':c.number,
                      #'app_id':erp7_id,
                      #'user_id':uid,
                      'reference':c.reference,
                      'state':'draft',
                      'type':'accrec',
                      'action':'',
                      'line_amount_type':c.line_amount_type,
                      'currency_code':c.currency_code.id,
                      'sale_id':new_id
                      }
               act['line_ids']=order_tools.plk_lines_to_xero_lines(cr,'trade',plk_l)
               act=order_tools.convert_to_create(act)
               act_id = pool.get('sale_journal').create(cr,uid,act)
               #cr.execute("update sale_journal set sale_null_id=%s,state_id=%s where id=%s",(new_id,draft_id,c.id))
    if UPDATE_SALE:
        sa_ids=pool.get('sale').search(cr,uid,[])
        pool.get('sale').update_sale(cr,uid,sa_ids)
        
    if INITIAL_COPY:
       sa_ids=pool.get('sale').search(cr,uid,[])
       pool.get('sale').create_delivery(cr,uid,sa_ids)
       
    for _ in range(ADD_EVENTS):  #add new events (simulate)      
        whs_ids=pool.get('whs_picking').search(cr,uid,[])
        pool.get('whs_picking').add_events(cr,uid,whs_ids)
    if UPDATE_WHS: #update
        whs_ids=pool.get('whs_picking').search(cr,uid,[])
        pool.get('whs_picking').update_state(cr,uid,whs_ids)
        

    cr.commit()
    cr.close()
    #print cnt1, cnt2
