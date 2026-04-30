import functools
from collections import OrderedDict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import orm
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc
import pprint
from datetime import date

CURRENCY_GBP=152
PRODUCT_NA=2979
PRODUCT_STAR=24344
TAX_ID_ST4=10
TAX_ID_ST0=1
TAX_ID_STI20=14
TAX_ID_STE20=16
from order_tools_core27 import *
from order_tools_types27 import *
def get_xero_tax_code(cr, tax_id):
    cr.execute("select xero_code from account_tax where id=%s", (tax_id,))
    tax_ids = [x[0] for x in cr.fetchall()]
    assert len(tax_ids)==1
    xero_code = tax_ids[0]
    return xero_code
def get_order_lines(cr, so):
    lines=[]
    for l in so.order_line:
        code='200'
        bom_prod_ids=[]
        for m in l.move_ids:
            bom_prod_ids.append(m.product_id.id)
        tax_type = get_xero_tax_code(cr, l.tax_id[0].id)
        v={#"state":"authorised",
           #"currency_id":so.currency_id.id,
            "bom_prod_ids":bom_prod_ids,
           "discount_rate":l.discount,
           #"tax_type":"output2",
            "tax_type":tax_type,
           "account_code":code,
           "price":l.price_unit,
           "product_qty":l.product_uom_qty,
           "product_cr_qty":l.product_uom_cr_qty,
           "description":l.name,
           "product_id":l.product_id.id,
           }
        if l.product_id:
           v['product_id'] = l.product_id.id
        lines.append(v)
    return lines

def get_erp_tax_id(cr, xero_code, pricelist_type):
    if pricelist_type=='retail':
        price_include=True            
    else:
        price_include=False
    arg=(xero_code,price_include)
    cr.execute("select id from account_tax where xero_code=%s and price_include=%s",arg)
    tax_ids = [x[0] for x in cr.fetchall()]
    assert len(tax_ids)>=1
    #print 'TAX IDS: ', tax_ids, xero_code, pricelist_type, price_include
    t_id=tax_ids[0]
    return t_id
    
def get_erp_tax_id2(cr, xero_code, pricelist_type):
    if pricelist_type=='retail':
        tax_code = "STI20"
    else:
        tax_code = "STE20"
    if pricelist_type=='retail':
        cr.execute("select id from account_tax where description=%s and price_include=True", (tax_code,))        
    else:
        cr.execute("select id from account_tax where description=%s and price_include=False", (tax_code,))
    tax_ids = [x[0] for x in cr.fetchall()]
    

    assert len(tax_ids)==1
    tax_id = tax_ids[0]
    #if xero_code != 'none':
    return tax_id
    
    if pricelist_type=='retail':
        tax_code = "ST4"
    else:
        tax_code = "ST0"    
    cr.execute("select id from account_tax where xero_code=%s", (xero_code,))
    tax_ids = [x[0] for x in cr.fetchall()]
    #assert len(tax_ids)==1
    tax_id = tax_ids[0]
    return tax_id

def get_order_lines_new(cr, so):
    lines=[]
    for l in so.order_line:
        if l.product_id:
            p_id=l.product_id.id
        else:
            p_id=PRODUCT_NA
        if len(l.tax_id)==0:
            xero_code='output2'
        elif len(l.tax_id)==1:
            tax_id=l.tax_id[0].id
            xero_code = get_xero_tax_code(cr, tax_id)
        else:
            xero_code='output2'
            
        plk_d={'description': l.name,
               'discount_rate': l.discount,
               'price': l.price_unit,
               'product_id': p_id,
               'tax_type': xero_code}
        plk=ProductLineKey.model_validate(plk_d)
        state_id=(0,0)
        line=order_move_line_data(state_id,plk,
                                  l.product_uom_qty,
                                  l.product_uom_cr_qty)
        lines.append(line)
    return lines

def get_xero_lines_new(line_ids,workflow,state_model):
    lines=[]
    for l in line_ids:
        if l.product_id:
            p_id=l.product_id.id
        else:
            p_id=PRODUCT_NA
        plk_d={'description': l.description,
               'discount_rate': l.discount_rate,
               'price': l.price,
               'product_id': p_id,
               'tax_type': l.tax_type}
        plk=ProductLineKey.model_validate(plk_d)
        if l.state_id:
            state_id=row_col_to_state_code_inv(state_model,
                                               l.state_id.state,
                                               workflow=workflow)
        else:
            state_id=(0,0)
        line=order_move_line_data(state_id,plk,
                                  l.product_qty,
                                  l.product_cr_qty)
        lines.append(line)
    return lines
def plk_lines_to_xero_lines(cr, workflow, lines,state_model):
    ret=[]
    for l in lines:
        row,col=l.state_id
        state_id=state_id_from_row_col(cr,state_model,row,col,workflow)        
        l={'product_id':l.linekey_id.product_id,
           'description':l.linekey_id.description,
           'discount_rate': l.linekey_id.discount_rate,
           'price': l.linekey_id.price,
           'product_qty' : int(l.asset_qty.qty),
           'product_cr_qty' : int(l.asset_qty.cr_qty),
           'account_code':'200',
           'currency_id':CURRENCY_GBP,
           'state_id':state_id,
           #'state':'',
           #'order_id': order_id,
           'tax_type': l.linekey_id.tax_type
           }
        ret.append(l)
    return ret
def whs_lines_to_xero_lines(cr,workflow,lines,state_model):
    ret=[]
    for l in lines:
        row,col=l.state_id
        state_id=state_id_from_row_col(cr,state_model,row,col)
        l={'product_id':l.linekey_id.product_id,
           'description':l.linekey_id.description,
           'discount_rate': l.linekey_id.discount_rate,
           'price': l.linekey_id.price,
           'location_id':l.linekey_id.location_id,
           'location_dest_id':l.linekey_id.location_dest_id,
           'product_qty' : int(l.asset_qty.qty),
           'product_cr_qty' : int(l.asset_qty.cr_qty),
           'account_code':'200',
           'tax_type': l.linekey_id.tax_type,
           'state_id':state_id
           }
        ret.append(l)
    return ret

def get_whs_lines(line_ids, workflow,state_model):
    lines=[]
    for l in line_ids:
        if l.product_id:
            p_id=l.product_id.id
        else:
            p_id=PRODUCT_NA
        plk_d={'description': l.description,
               'discount_rate': l.discount_rate,
               'price': l.price,
               'product_id': p_id,
               'tax_type': l.tax_type,
               'location_id': l.location_id.id,
               'location_dest_id':l.location_dest_id.id}
        plk=ProductLineKeyWHS.model_validate(plk_d)
        if l.state_id:
            state_id=row_col_to_state_code_inv(state_model,
                                               l.state_id.state,
                                               workflow=None)
            #print '   ',l.description, l.state_id.state, state_id
        else:
            state_id=(0,0)
        line=order_move_line_data(state_id,plk,
                                  l.product_qty,
                                  l.product_cr_qty)
        lines.append(line)
    return lines

def get_xinv_from_xero_data(xinv):
    v={'sale_order_id':0,
       'date':xinv['DateString'].split('T')[0],
       'date_due':xinv['DueDateString'].split('T')[0],
       'number':0,
       'name':xinv['InvoiceNumber'],
       'reference':xinv['Reference'],
       'state':xinv['Status'].lower(),
       'type':xinv['Type'].lower(),
       'line_amount_type':xinv['LineAmountTypes'].lower(),
       'currency_code':CURRENCY_GBP,
       'external_id':xinv['InvoiceID'],
       'return_reason':'',
       'action':'',
       'user_id':1,
       'app_id':4} #xero app
    lines=[]
    for l in xinv['LineItems']:
        plk_d={'description': l['Description'],
               'discount_rate': 0,
               'price': l['UnitAmount'],
               'product_id': PRODUCT_NA,
               'tax_type': l['TaxType'].lower()}
        qty=l['Quantity']
        plk=ProductLineKey.model_validate(plk_d)
        state_id=(0,0)
        line=order_move_line_data(state_id,plk,
                                  qty,
                                  0)
        lines.append(line)
    v['line_ids']=lines
    r=SaleConfirmation.model_validate(v)
    return r

def get_sale_confirmation_cls(cr, so):
    lines_w = get_order_lines_new(cr,so)
    #conf = map(get_l_ids, so.sale_confirmation_ids) \
    #    + map(get_l_ids, so.rma_ids)
    #conf = functools.reduce( add_lines, conf )
    lines=[]
    for l in lines_w:
        lines.append( l.model_dump() )

    v={'sale_order_id':so.id,
       'date':so.date_confirm,
       'date_due':so.requested_date,
       'number':0,
       'name':so.name,
       'reference':so.client_order_ref,
       'state':'DRAFT',
       'type':'ACCREC',
       'line_amount_type':so.line_amount_type,
       'currency_code':so.pricelist_id.currency_id.id,
       'external_id':'',
       'return_reason':'',
       'action':'',
       'user_id':so.user_id.id,
       'app_id':0,
       'line_ids': lines}
    so_conf=SaleConfirmation.model_validate(v)
    return so_conf
def get_sale_confirmation_cls_xero(so):
    lines_w = get_xero_lines_new(so.line_ids,'trade','res.order.state')
    #conf = map(get_l_ids, so.sale_confirmation_ids) \
    #    + map(get_l_ids, so.rma_ids)
    #conf = functools.reduce( add_lines, conf )
    lines=[]
    for l in lines_w:
        lines.append( l.model_dump() )

    v={'sale_order_id':so.sale_order_id.id,
       'date':so.date,
       'date_due':so.date_due,
       'number':so.number,
       'name':so.name,
       'reference':so.reference,
       'state':so.state,
       'type':so.type,
       'line_amount_type':so.line_amount_type,
       'currency_code':so.currency_code.id,
       'external_id':so.external_id,
       'return_reason':so.return_reason,
       'action':so.action,
       'user_id':so.user_id.id,
       'app_id':so.app_id.id,
       'line_ids': lines}
    so_conf=SaleConfirmation.model_validate(v)
    return so_conf
#DRAFT=(0,0)
#CANCEL=(0,1)

whs_picking_row_col_to_state=[((0,0),'draft'),
                              ((0,1),'cancel'),
                              ((1,0),'confirmed'),
                              ((1,1),'waiting'),
                              ((2,0),'reserved'),
                              ((3,0),'manifest'),
                              ((4,0),'done'),
                              ((4,1),'scrap')]
order_retail_row_col_to_state=[((0,0),'draft'),
                               ((0,1),'cancel'),
                               ((1,0),'confirmed'),
                               ((1,1),'purchasing'),
                               ((2,0),'reserved'),
                               ((3,0),'delivered'),
                               ((4,0),'done')]
order_trade_row_col_to_state=[((0,0),'draft'),
                              ((0,1),'cancel'),
                              ((1,0),'confirmed'),
                              ((1,1),'purchasing'),
                              ((2,0),'reserved'),
                              ((3,0),'delivered'), #invoice/cr note
                              ((4,0),'done')]
purchase_order_row_col_to_state=[((0,0),'draft'),
                                  ((0,1),'cancel'),
                                  ((1,0),'confirmed'),
                                  ((2,0),'delivered'), #invoice/cr note
                                  ((3,0),'done')]
payment_row_col_to_state=[((0,0),'office'),
                          ((0,1),'cancel'),
                          ((1,0),'accounts')]

def row_col_to_state_(res_state_table,workflow=None):
    #print 'kocour', res_state_table,workflow
    state_map={'retail':{'res.order.state':order_retail_row_col_to_state},
               'trade': {'res.order.state':order_trade_row_col_to_state},
               None :   {'res.whs_picking.state':whs_picking_row_col_to_state,
                         'res.payment.state':payment_row_col_to_state,
                         'res.purchase_order.state':purchase_order_row_col_to_state
                        }
               }
    return state_map[workflow][res_state_table]

def row_col_to_state_code(res_state_table,row,col,workflow=None):
    state_map = dict(row_col_to_state_(res_state_table,workflow=workflow))
    state_code = state_map.get( (row,col),'draft')
    return state_code

def row_col_to_state_code_inv(res_state_table,state_code,workflow=None):
    def swp(xs):
        return [(b,a) for (a,b) in xs]
    state_map = dict(swp(row_col_to_state_(res_state_table,workflow=workflow)))
    row,col = state_map.get(state_code,(0,0) )
    return row,col
    
def state_id_from_row_col(cr,res_state_model,row,col,workflow=None):
    res_state_table=res_state_model.replace('.','_')
    state_code = row_col_to_state_code(res_state_model,row,col,workflow)    
    query="select id from %s"%res_state_table
    cr.execute(query + " where state=%s",(state_code,))
    #print 10*'*'
    #print cr.query
    state_ids=[x[0] for x in cr.fetchall()]
    if len(state_ids)>0:        
        state_id=state_ids[0] #TBD
    else:
        cr.execute("select id from " + res_state_table)
        state_id=[x[0] for x in cr.fetchall()][0]
    #print 'state_id_from_row_col ', res_state_table,row,col,workflow
    #print '   ', state_id,state_code
    return state_id

def get_xero_lines(line_ids):
    lines = []
    for l in line_ids:
        if (l.product_qty>0) and (l.product_cr_qty>0):            
           v={"discount_rate":l.discount_rate,
              "tax_type":l.tax_type,
              "account_code":l.account_code,
              "price":l.price,
              "product_qty":l.product_qty,
              "description":l.description,
              }
           if l.product_id:
              v['product_id'] = l.product_id.id
           else:
              v['product_id'] = PRODUCT_NA
           lines.append(v)
           v={"discount_rate":l.discount_rate,
              "tax_type":l.tax_type,
              "account_code":l.account_code,
              "price":l.price,
              "product_qty":l.product_cr_qty*(-1),
              "description":l.description,
              }
           if l.product_id:
              v['product_id'] = l.product_id.id
           else:
              v['product_id'] = PRODUCT_NA
           lines.append(v)
           
        elif (l.product_cr_qty>0):            
           v={
              "discount_rate":l.discount_rate,
              "tax_type":l.tax_type,
              "account_code":l.account_code,
              "price":l.price,
              "product_qty":l.product_cr_qty *(-1),
              "description":l.description,
              }
           if l.product_id:
              v['product_id'] = l.product_id.id
           else:
              v['product_id'] = PRODUCT_NA
           lines.append(v)
        else:
           v={
              "discount_rate":l.discount_rate,
              "tax_type":l.tax_type,
              "account_code":l.account_code,
              "price":l.price,
              "product_qty":l.product_qty,
              "description":l.description,
              }
           if l.product_id:
              v['product_id'] = l.product_id.id
           else:
              v['product_id'] = PRODUCT_NA
           lines.append(v)
           
    return lines
#def _convert_lines_to_create(line_ids):
#    lines=[]
#    for l in line_ids:
#        lines.append( (0,0,l) )
#    return lines
#def convert_lines_to_create(line_ids):
#    lines=[]
#    for l in line_ids:
#        if 'currency_id' not in l:
#            l['currency_id'] = CURRENCY_GBP
#            lines.append(l)
#    return _convert_lines_to_create(lines)
#
#def convert_to_create(invx):
#    lines=[]
#    for l in invx['line_ids']:
#        lines.append( (0,0,l) )
#    invx['line_ids'] = lines
#    return invx
#
def convert_to_create(invx):
    lines=[]
    for l in invx['line_ids']:
        lines.append( (0,0,l) )
    invx['line_ids'] = lines
    return invx
def convert_lines_to_create(line_ids):
    lines=[]
    for l in line_ids:
        if 'currency_id' not in l:
            l['currency_id'] = CURRENCY_GBP
        lines.append( (0,0,l) )
    #invx['line_ids'] = lines
    return lines

def lines_maps(lines):
    ret=OrderedDict()
    ret_neg = OrderedDict()
    for l in lines:
 
        key = (l['product_id'], l['description'], l['tax_type'], l['price'], l['discount_rate'])
            
        val = l['product_qty']
        price = l['price']
        #if val>=0.0 and (l['price']>=0.0):
        if val>=0.0:            
            v = ret.setdefault(key, [])
            v.append(val)
        else:
            v = ret_neg.setdefault(key, [])
            v.append((-1.0)*val)
            
    return (ret,ret_neg)
def fst(x):
    (a,b)=x
    return a
def snd(x):
    (a,b)=x
    return b

def map_mappend(a, b, df = None):
    if df is None:
        df=[]
    keys = []
    ret = OrderedDict()
    for k in a:
        if k not in keys:
            keys.append(k)            
    for k in b:
        if k not in keys:
            keys.append(k)
    for k in keys:
        v_a = a.get(k,df)
        v_b = b.get(k,df)
        ret[k] = v_a + v_b
    return ret

def get_xero_lines_ids(l_ids):
    def get_xero_lines_x(x):
        return get_xero_lines(x.line_ids)
    
    a = map(get_xero_lines_x, l_ids)
    b = map(lines_maps, a)

    n = map(fst, b)
    p = map(snd, b)
    n = functools.reduce( map_mappend, n , OrderedDict() )
    p = functools.reduce( map_mappend, p , OrderedDict() )
    return (n,p)
    
def list_to_sum(u):
    ret = OrderedDict()
    for k in u:
        v = u[k]
        ret[k] = sum(v)
    return ret
def sum_to_list(u):
    ret = OrderedDict()
    for k in u:
        v = u[k]
        ret[k] = [v]
    return ret
    
def neg(a):
    ret = OrderedDict()
    for (k,v) in a.items():
        ret[k] = (-1.0)*v
    return ret
def filter_if_zero(u):
    ret = OrderedDict()
    for k in u:
        v = u[k]
        if v != 0.0:
            ret[k] = v
    return ret

def split_for_inv_crn(u):
    inv = OrderedDict()
    crn = OrderedDict()
    for k in u:
        product_id, description, tax_type, price, discount_rate = k
        v = u[k]
        if (v>=0.0) and (price>=0.0):
            inv[k] = v
        elif (v<0.0) and (price>=0.0):            
            crn[k]= v * (-1)
        elif (v>=0.0) and (price<=0.0):
            k = product_id, description, tax_type, (-1)*price, discount_rate
            crn[k]= v 
        else:
            k = product_id, description, tax_type, (-1)*price, discount_rate
            inv[k]= v * (-1)            
            
    return (inv, crn)


def convert_to_val(u):
    ret = []
    for (k,v) in u.items():        
        product_id, description, tax_type, price, discount_rate = k
        val = {'description':description,
               'account_code':'200',
               'currency_id':CURRENCY_GBP,
               'tax_type':tax_type,
               'price':price,
               'discount_rate':discount_rate,
               'product_id':product_id,
               'product_qty':v}
        ret.append(val)
    return ret

def get_new_sale_confirmation(cr,so):
    cr.execute("select max(number) from sale_confirmation where sale_order_id=%s",(so.id, ) )
    number_ = [x[0] for x in cr.fetchall()][0]
    if number_ is None:
        number = 1
    else:
        number = number_ +1
    return number

def get_new_rma(cr,so):
    cr.execute("select max(number) from rma where sale_order_id=%s",(so.id, ) )
    number_ = [x[0] for x in cr.fetchall()][0]
    if number_ is None:
        number = 1
    else:
        number = number_ +1
    return number
def get_reference(so):
    if so.client_order_ref:
        ref=so.client_order_ref
    else:
        ref='Id%d'%(so.id)
    return ref

    
def _prepare_sale_confirmation(cr,so, number, name):
    #number = get_new_sale_confirmation(cr,so)
    ref = get_reference(so)
    #name = get_name(so,number,pos='SCO',neg='RMA')
    if so.state in ['cancel']:
        inv_type = 'accreccredit'
    else:
        inv_type = 'accrec'
    
    #d_c = datetime.strptime(so.date_confirm, "%Y-%m-%d")
    today=date.today()
    d_c=date.strftime(today,DEFAULT_SERVER_DATE_FORMAT)
    #ts = so.date_confirm #datetime_to_xero_str_timestamp(d_c)          
    #if so.pricelist_id.type == 'retail':
    #    lat='inclusive'
    #else:
    #    lat='exclusive'
    
    inv={'sale_order_id':so.id,
         'date': d_c,
         'date_due':d_c,
         'number': number,
         'reference':ref,
         'name':name,
         'state':'authorised',
         'type':inv_type,
         'line_amount_type':so.line_amount_type,
         'currency_code': so.currency_id.id, #'GBP',
         #'external_id':so.xero_id
         }
    #inv['line_ids']=lines
    return inv
def get_name(so, number, prefix):
    #if so.state in ['cancel']:
    #    name = "%s-%s%d" % (so.name, neg,number)
    #elif (pos=='INV') and (number == 1):
    #    name = so.name
    #else:
    if (prefix=='INV') and (number==1):
        name = so.name
    else:
        name = "%s-%s%d" % (so.name,prefix,number)
    return name
def get_new_invoice_number(cr,so):
    cr.execute("select max(number) from xero_invoice where sale_order_id=%s",(so.id, ) )
    number_ = [x[0] for x in cr.fetchall()][0]
    if number_ is None:
        number = 1
    else:
        number = number_ +1
    return number
def get_new_credit_note_number(cr,so):
    cr.execute("select max(number) from xero_credit_note where sale_order_id=%s",(so.id, ) )
    number_ = [x[0] for x in cr.fetchall()][0]
    if number_ is None:
        number = 1
    else:
        number = number_ +1
    return number

def _prepare_xero_invoice(cr,so,itype, number, name, proforma=False):
    
    #number = get_new_invoice_number(cr,so)
    ref = get_reference(so)
    #name = get_name(so,number)
    if itype == 'CRN':
        inv_type = 'accreccredit'
        state = 'draft'
    else:
        inv_type = 'accrec'
        state = 'authorised'
    if proforma:
        state='draft'
    #d_c = datetime.strptime(so.date_confirm, "%Y-%m-%d")
    #ts = so.date_confirm #datetime_to_xero_str_timestamp(d_c)
    
    today=date.today()
    d_c=date.strftime(today,DEFAULT_SERVER_DATE_FORMAT)
    
    lat = so.line_amount_type
    inv={'sale_order_id':so.id,
         'date': d_c,
         'date_due':d_c,
         'number': number,
         'reference':ref,
         'name':name,
         'state':state,
         'type':inv_type,
         'line_amount_type':lat,
         'currency_code': so.currency_id.id, #'GBP',
         'external_id':False
         }
    #inv['line_ids']=lines
    return inv
def convert_from_neg(a):
        y = OrderedDict()
        for (k,v) in a.items():
            product_id, description, tax_type, price, discount_rate = k
            if (v<0.0) and (price<0.0):
                nk=product_id, description, tax_type, (-1.0*price), discount_rate
                nv = -1*v
            elif (v>0.0) and (price<=0.0):
                nk=product_id, description, tax_type, -1*price, discount_rate
                nv = -1*v
                
            else:
                nk = product_id, description, tax_type, price, discount_rate
                nv = v
            y[nk]=nv
        return y
def print_kv(kv,label=''):
    #print(label)
    for (k,v) in kv.items():
        #print('  ', k)
        #print('  ', v)
        pass
def calc_total(kv):
    t=0.0
    for (k,v) in kv.items():
        product_id, description, tax_type, price, discount_rate = k
        #print [price,v]
        #if isinstance(v,list):
        #    t = t + price*(sum(v))
        #else:
        t = t + price*(v)    
    return t
def check_orders(pool, cr, uid, so_ids):

    SO=pool.get('sale.order')
    ret=[]
    ret_inv = []
    #print so_ids
    check_external_inv_ids = []
    check_external_crn_ids = []        
    for so in SO.browse(cr, uid, so_ids):
        total = so.amount_total
        #total_conf = [t.total for t in so.sale_confirmation_ids]
        #total_rma = [t.total for t in so.rma_ids]
        #total_inv =  [t.total for t in so.xero_invoice_ids]
        #total_crn =  [t.total for t in so.xero_credit_note_ids]
        inv_total_xero = so.inv_total_xero
        conf_total_office = so.conf_total_office
        
        check = abs( abs(total) - abs(conf_total_office) )<= 0.1
        
        if not check:
            for x in so.xero_invoice_ids:
                if x.external_id:
                    pass
                else:
                    check_external_inv_ids.append(x.id)
            for x in so.xero_credit_note_ids:
                if (not x.external_id) and (x.total > 0.00):
                    check_external_crn_ids.append(x.id)
            pass
        else:
            check = abs( abs(total) - abs(inv_total_xero) )<= 0.1
            if not check:
                ret_inv.append(so.id)
            else:
                ret.append(so.id)
    return ret, ret_inv, check_external_inv_ids, check_external_crn_ids

def get_line_ids(o):
    return get_xero_lines_new(o.line_ids,'trade','res.order.state')

def split_lines_for_invoicing(lines):
    inv=[]
    crn=[]
    for x in lines:
        l=x
        d=l.asset_qty.diff()
        if l.linekey_id.price >= 0:
           if abs(d)>0.001:            
              if l.asset_qty.qty>0: #price positive, qty positive
                   nl=copy.deepcopy(l)
                   nl.asset_qty=lineval(l.asset_qty.qty,0)
                   inv.append(nl)
              if l.asset_qty.cr_qty>0: #price positive, qty negative
                   nl=copy.deepcopy(l)
                   nl.asset_qty=lineval(0, l.asset_qty.cr_qty)
                   crn.append(nl)
        else:
           if d>0.001: #price negative, qty positive
              nl=copy.deepcopy(l)
              nl.asset_qty=lineval(0, d)
              nl.linekey_id.price = abs(l.linekey_id.price)
              crn.append(nl)
               
    return inv,crn
def calc_mlines_total(lines):
    tot=0
    for l in lines:
        tot += l.linekey_id.price * l.asset_qty.diff()
    return tot
def create_xero_invoices_and_cr_notes_new(pool, cr, uid, so, create=False):
    conf = map(get_line_ids, so.sale_confirmation_ids)
    #     + map(get_line_ids, so.rma_ids)
    conf = functools.reduce( add_lines, conf ,[])
    
    inv = map(get_line_ids, so.xero_invoice_ids) \
        + map(get_line_ids, so.xero_credit_note_ids)
    inv = functools.reduce( add_lines, inv ,[])

    #print
    #print " ________________   %s  ______________" % so.name    
    to_inv=meval_lines( sub_lines(conf,inv) )
    inv_new,crn_new=split_lines_for_invoicing(to_inv)
    inv_tot = calc_mlines_total(inv_new)
    crn_tot = calc_mlines_total(crn_new)
            
    #print '       inv tot, crn tot', inv_tot, crn_tot
    inv_label = str("To Invoice (%s)"%(str(inv_tot)))
    crn_label = str("To CRN (%s)"%(str(crn_tot)) )
                    
    #printmove_lines("Confirmed", conf,
    #                "Invoiced", inv,
    #                inv_label, inv_new,
    #                crn_label, crn_new)

    if inv_new:
            workflow='retail'
            lines=plk_lines_to_xero_lines(cr,workflow,inv_new,'res.order.state')
            
            number_inv = get_new_invoice_number(cr,so)
            name_inv = get_name(so, number_inv, 'INV')
            inv_data = _prepare_xero_invoice(cr,so,'INV', number_inv, name_inv)            
            inv_data['line_ids'] = lines
            x=convert_to_create(inv_data)
            if abs(inv_tot)>0.0000:
                new_id=pool.get('xero_invoice').create(cr,uid,inv_data)
                #print '     New Invoice Created', new_id, inv_data['name']

    if crn_new:
        workflow='retail'
        lines=plk_lines_to_xero_lines(cr,workflow,crn_new,'res.order.state')
                
        number_crn = get_new_credit_note_number(cr,so)
        name_crn = get_name(so, number_crn, 'CRN')
        crn_data = _prepare_xero_invoice(cr,so,'CRN', number_crn, name_crn)
        crn_data['line_ids'] = lines
        x=convert_to_create(crn_data)
        if abs(crn_tot)>0.0000:
            new_id=pool.get('xero_credit_note').create(cr,uid,crn_data)
            #print '     New Credit Note', new_id, crn_data['name']
                
    
    
    
    
def create_xero_invoices_and_cr_notes(pool, cr, uid, so, create=True):
    
    #Confirmations and RMAs    
    (u, u_cr) = get_xero_lines_ids(so.sale_confirmation_ids)    
    (v, v_cr) = get_xero_lines_ids(so.rma_ids)
    u = list_to_sum(u)
    u_cr = list_to_sum(u_cr)

    u_one_inv = map_mappend(u, u_cr, df=0 )
    u_one_inv_val = convert_to_val(u_one_inv)
    
    v = list_to_sum(v)        
    v_cr = list_to_sum(v_cr)
    
    u = map_mappend(u, neg(u_cr), df=0 )
    v = map_mappend(v, neg(v_cr), df=0 )
    #print(['calc total', calc_total(u) , calc_total(v)])
    conf_total = calc_total(u)  - calc_total(v)
    #Invoices and CRNs
    (xu, xu_cr) = get_xero_lines_ids(so.xero_invoice_ids)
    (xv, xv_cr) = get_xero_lines_ids(so.xero_credit_note_ids)
    xu = list_to_sum(xu)
    xv = list_to_sum(xv)
    xu_cr = list_to_sum(xu_cr)
    xv_cr = list_to_sum(xv_cr)
    xu = map_mappend(xu, xu_cr, df=0 )
    xv = map_mappend(xv, xv_cr, df=0 )
    inv_crn_total = calc_total(xu) - calc_total(xv)    
    uxu = map_mappend(u, neg(xu), df=0 )    
    uxu = map_mappend(uxu, u_cr, df=0 )
    
    vxv = map_mappend(v, neg(xv), df=0 )
    vxv = map_mappend(vxv, v_cr, df=0 )

    uxu=convert_from_neg(uxu)
    vxv=convert_from_neg(vxv)

    uxu_new = filter_if_zero(uxu)
    vxv_new = filter_if_zero(vxv)

    inv_and_crn = map_mappend(uxu_new, neg(vxv_new), df=0 )
    inv_and_crn = filter_if_zero(inv_and_crn)

    uxu_new, vxv_new = split_for_inv_crn(inv_and_crn)

    #print_kv(uxu_new,label='uxu_new')
    #print_kv(vxv_new,label='vxv_new')
    #print_kv(inv_and_crn,label='inv_nad_crn')
    uxu_lines = convert_to_val(uxu_new)
    vxv_lines = convert_to_val(vxv_new)

    uxu_cr = convert_lines_to_create(uxu_lines)

    new_vxv_lines = []
    for l in vxv_lines:
        #print 'kocour', l
        l['product_cr_qty'] = l['product_qty']
        l['product_qty']=0 #l['product_qty']
        new_vxv_lines.append(l)
    vxv_lines = new_vxv_lines
    
    vxv_cr = convert_lines_to_create(vxv_lines)
    #print('create_xero_invoices_and_cr_notes', 44*'*', so.name, so.amount_total, conf_total)
    ret = ([],[])
    number_inv = get_new_invoice_number(cr,so)
    name_inv = get_name(so, number_inv, 'INV')
    
    number_crn = get_new_credit_note_number(cr,so)
    name_crn = get_name(so, number_crn, 'CRN')

    if inv_and_crn:
       if (len(so.sale_confirmation_ids)==1) and (len(so.rma_ids)==0): #inv_crn_total != conf_total:           
          inv_data = _prepare_xero_invoice(cr,so,'INV', number_inv, name_inv)
          inv_data['line_ids'] = convert_lines_to_create(u_one_inv_val)
          if u_one_inv_val and create:
              new_id=pool.get('xero_invoice').create(cr,uid,inv_data)
              #print('INV DATA (one)', new_id, inv_data['name'])
          ret = (u_one_inv_val, [])

       else:
          inv_data = _prepare_xero_invoice(cr,so,'INV', number_inv, name_inv)
          inv_data['line_ids'] = uxu_cr
          crn_data = _prepare_xero_invoice(cr,so,'CRN', number_crn, name_crn)        
          crn_data['line_ids'] = vxv_cr
          #conf_vs_so_total = (so.amount_total - conf_total) <= 0.01
          inv_tot = calc_total(uxu_new)
          crn_tot = calc_total(vxv_new)
          #print conf_total, so.name          
          #print inv_and_crn
          if uxu_cr and create and (inv_tot >= 0.001):
              pass
              new_id=pool.get('xero_invoice').create(cr,uid,inv_data)
              #print('INV DATA', new_id, inv_data['name'], inv_tot)
              #pprint.pprint(inv_data)
          if vxv_cr and create and (crn_tot >= 0.001):
              pass
              new_id=pool.get('xero_credit_note').create(cr,uid,crn_data)
              print('CRN DATA', new_id, inv_data['name'], crn_tot)              
              #pprint.pprint(crn_data)
              #pprint.pprint( crn_data )
          ret = (uxu_lines, vxv_lines)
    return ret
    
def create_order_confirmation_and_rma(pool, cr, uid, lines, wiz=None, so=None, create=True):
    if wiz:
        so=wiz.order_id
        delivery_notes = wiz.delivery_notes
        reason_for_return = wiz.reason_for_return
        date_due = wiz.date_due
        val_conf = {'date_due':date_due,'notes':delivery_notes}
        val_rma = {'date_due':date_due,'return_reason':reason_for_return,'notes':delivery_notes}
    else:
        val_conf = {}
        val_rma = {}
    lines_w = lines
    (w_u,w_v) = lines_maps(lines_w)
    w_u = list_to_sum(w_u)
    w_v = list_to_sum(w_v)
    #uv = get_xero_lines_ids(w.order_id.sale_confirmation_ids)            
    #(u,v) = get_xero_lines_ids(w.order_id.xero_invoice_ids)
    (u, u_cr) = get_xero_lines_ids(so.sale_confirmation_ids)
    (v, v_cr) = get_xero_lines_ids(so.rma_ids)
        
    u = list_to_sum(u)
    v = list_to_sum(v)
    u_cr = list_to_sum(u_cr)
    v_cr = list_to_sum(v_cr)

    w_u_new = map_mappend(w_u, neg(u), df=0 )
    w_u_new = map_mappend(w_u_new, u_cr, df=0 )
    
    w_v_new = map_mappend(w_v, neg(v), df=0 )
    w_v_new = map_mappend(w_v_new, v_cr, df=0 )
    

    w_u_new = filter_if_zero(w_u_new)
    w_v_new = filter_if_zero(w_v_new)

    sale_conf_lines = convert_to_val(w_u_new)
    sale_rma_lines= convert_to_val(w_v_new)

    sale_conf = convert_lines_to_create(sale_conf_lines)
    sale_rma_lines_cr=[]
    for l in sale_rma_lines:
        l['product_cr_qty'] = l['product_qty']
        l['product_qty']=0 #l['product_qty']
        sale_rma_lines_cr.append(l)
    sale_rma = convert_lines_to_create(sale_rma_lines)

    number_sco = get_new_sale_confirmation(cr,so)
    number_rma = get_new_rma(cr,so)

    if number_sco == number_rma:
        pass
    elif number_sco < number_rma:
        number_sco = number_rma
        number_rma = number_rma
    else:
        number_sco = number_sco
        number_rma = number_sco        
    
    name_rma = get_name(so, number_rma, 'RMA')
    name_sco = get_name(so, number_sco, 'SCO')
    
    sale_conf_val = _prepare_sale_confirmation(cr,so, number_sco, name_sco)
    sale_conf_val['line_ids'] = sale_conf
    sale_conf_val.update(val_conf)

    sale_rma_val = _prepare_sale_confirmation(cr,so, number_rma, name_rma)
    sale_rma_val['line_ids'] = sale_rma
    sale_rma_val.update(val_rma)

    if sale_conf and create:
        pass
        new_id=pool.get('sale_confirmation').create(cr,uid,sale_conf_val)
    if sale_rma and create:
        #print('NEW RMA:')
        new_id=pool.get('rma').create(cr,uid,sale_rma_val)
    return (sale_conf_lines, sale_rma_lines)
def create_order_confirmation(pool, cr, uid, lines, wiz, so,sale_date=None,
                              date_due=None,app_code='erp7',cancel=False):
    if wiz:
        so=wiz.order_id
        delivery_notes = wiz.delivery_notes
        reason_for_return = wiz.reason_for_return
        date_due = wiz.date_due
        val_conf = {'date_due':date_due,'notes':delivery_notes}
        val_conf = {'date_due':date_due,'notes':delivery_notes,
                    'return_reason':reason_for_return}
    else:
        val_conf = {}
        val_rma = {}
    cr.execute("select code,id from res_application")
    app_map = dict([x for x in cr.fetchall()])
    val_conf['app_id']=app_map[app_code]
    val_conf['user_id']=uid

    
    number_sco = get_new_sale_confirmation(cr,so)
    number_rma = get_new_rma(cr,so)

    if number_sco == number_rma:
        pass
    elif number_sco < number_rma:
        number_sco = number_rma
        number_rma = number_rma
    else:
        number_sco = number_sco
        number_rma = number_sco
    if number_sco==1:
        val_conf['action']='initial'
    elif cancel:
        val_conf['action']='cancel'
    else:
        if val_conf['return_reason']:
            val_conf['action']='rma'
        else:
            val_conf['action']='amend'
    name_sco = get_name(so, number_sco, 'SCO')
        
    sale_conf_val = _prepare_sale_confirmation(cr,so, number_sco, name_sco)
    sale_conf_val['line_ids'] = lines
    if sale_date:
        sale_conf_val['date']=sale_date
    if date_due:
        sale_conf_val['date_due']=date_due
    sale_conf_val.update(val_conf)
    if lines:
        x=convert_to_create(sale_conf_val)
        print 'kocour', x
        new_id=pool.get('sale_confirmation').create(cr,uid,x)
    else:
        new_id=False
    return new_id
def order_history_section(pool, cr, uid, so):
    sco_map = OrderedDict()
    rma_map = OrderedDict()
    for sco in so.sale_confirmation_ids:
        sco_map[int(sco.number)] = sco
    for rma in so.rma_ids:
        rma_map[int(rma.number)] = rma    
    number_sco = get_new_sale_confirmation(cr,so)
    number_rma = get_new_rma(cr,so)
    sco_rma_map = OrderedDict()
    for i in range(1, max(number_sco, number_rma) ):
        sco=sco_map.get(i)
        rma=rma_map.get(i)
        #title=str(i)
        if sco and rma:
            title = sco.name + ' ' + rma.name
            c_date = sco.date
            date_due = rma.date_due
        elif sco:
            title=sco.name
            c_date= sco.date
            date_due = sco.date_due
        else:
            title = rma.name
            c_date = rma.date
            date_due = rma.date_due
            
        val = { 'sco':sco,
                'rma':rma,
                'title':title,
                'date':c_date,
                'date_due':date_due
              }        
        sco_rma_map[i] = val
    data=[]
    for i,v in sco_rma_map.items():
        row=[i,v['title'],v['date'],v['date_due']]
        data.append(row)
    ctx = {'so':so, 'time':time, 'sco_rma_map':sco_rma_map,'data':data}
    return ctx
                
# def create_order_lines(pool, cr, uid, so):
#     lines = get_order_lines(so)
    
#     (w_u,w_v) = lines_maps(lines_w)
#     w_u = list_to_sum(w_u)
#     w_v = list_to_sum(w_v)
    
#     (u,v) = get_xero_lines_ids(so.sale_confirmation_ids)
#     (xx,v) = get_xero_lines_ids(so.rma_ids)

#     u = list_to_sum(u)
#     v = list_to_sum(v)


#     w_u_new = map_mappend(w_u, neg(u), df=0 )
#     w_v_new = map_mappend(w_v, neg(v), df=0 )

#    w_u_new = filter_if_zero(w_u_new)
#    w_v_new = filter_if_zero(w_v_new)

#    sale_conf = convert_to_val(w_u_new)
#    sale_rma = convert_to_val(w_v_new)

#    print sale_conf
