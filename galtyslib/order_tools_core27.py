import sys
PYTHON_VERSION = sys.version.split()[0]
if PYTHON_VERSION=='2.7.18':
    from order_tools_types27 import *
    #
    #In order to get py27 version, run:
    #strip-hints order_tools_core.py > order_tools_core27.py
    #
else:
    from order_tools_types import *
    
from tabulate import tabulate
import docutils.parsers.rst
from docutils import statemachine
import copy
from collections import OrderedDict, defaultdict
import functools
#from order_tools_types import *
#from order_tools_core import *

def add_lines(a          , b          )           :
    return a+b
def mul_lines(lines          , b         )           :
    ret=[]
    for l in lines:
        k=l.key()
        v=l.val()*b
        ret.append( OrderMoveLineData.fromkv(k, v) )
    return ret
def mneg_lines(lines          )           :
    ret = []
    for l in lines:
        k = l.key()
        v = l.val()
        ret.append( OrderMoveLineData.fromkv(k, LineVal.mneg(v)  ) )            
    return ret
def mn_max(lines          )           :
    s_m_max=0
    s_n_max=0
    for l in lines:
        (m,n)=l.state_id
        #print ('m,n', m, n)
        if m > s_m_max:
            s_m_max=m
        if n > s_n_max:
            s_n_max=n
    return (s_m_max, s_n_max)
def sub_lines(a          ,b          )           :
    return (a + mneg_lines(b))
def meval_lines(a          )           :
    d=OrderedDict()
    for l in a:
        k = l.key()
        v = d.setdefault(k, [])
        v.append( l.val() )
    dl=[]
    for (k,v) in d.items():
        val=functools.reduce(LineVal.mappend, v, LINE_VAL_ZERO)
        vv=val.meval() #LineVal.meval(val)
        if not (vv == LINE_VAL_ZERO):
            dl.append( OrderMoveLineData.fromkv(k,vv) )
    return dl
def eq_lines(a          , b          )      :
    e=sub_lines(a, b) #a-b
    e=meval_lines(e)
    return (len(e)==0)
def msort_lines(a          )           :
    return sorted( a, key=lambda l:(l.linekey_id,l.state_id))
def minc_lines(a          , m=1, n=0)           :
    ret=[]
    for x in a:
        y=copy.deepcopy(x)
        # Increment row (m) component of tuple (m,n)
        y.state_id = (y.state_id[0] + m, y.state_id[1]+n)            
        ret.append(y)
    return ret
def mdec_lines(a          , m=1, n=0)           :
    ret=[]
    for x in a:
        y=copy.deepcopy(x)
        # Decrement row (m) component of tuple (m,n)
        y.state_id = (y.state_id[0] - m, y.state_id[1] - n)            
        ret.append(y)
    return ret

def transpose(a):
    """
    Transpose lists of lists. Rows become columns.
    """
    return list(map(list, zip(*a)))
def transpose2(a):
    return [[row[i] for row in a] for i in range(len(a[0]))]
            
def add_array(a,b):
    ret=[]
    for (rowa,rowb) in zip(a,b):
        row=[]
        for (ca,cb) in zip(rowa,rowb):
            row.append(ca+cb)
        ret.append(row)
    return ret

def sub_array(a,b):
    ret=[]
    for (rowa,rowb) in zip(a,b):
        row=[]
        for (ca,cb) in zip(rowa,rowb):
            row.append(ca-cb)
        ret.append(row)
    return ret

def get_shape(a):
    m,n=0,0
    for row in a:
        if len(row)>n:
            n=len(row)
            break
        break
    m=len(a)
    return (m,n)

def move_to_array_lines(m          )            :
    (m_max,n_max)=mn_max(m)
    d=OrderedDict()
    for l in m:
        val=l.val()
        stv=d.setdefault(l.linekey_id, OrderedDict() )
        v = stv.setdefault( l.state_id, [] )
        v.append( val)
    ret=[]
    for (linekey_id, vv) in d.items():
        array=[]
        for m in range(m_max+1):
            row=[]
            for n in range(n_max+1):
                state_id=(m,n)
                #val=sum(vv.get(state_id,[]), start=lineval(0,0))
                val=sum(vv.get(state_id,[]) + [lineval(0,0)] )
                row.append(val)
            array.append(row)
        a=OrderMoveLineArray(linekey_id=linekey_id,
                               array_qty=array)
        ret.append(a)
    return ret
def array_to_move_lines(a           )           :
    ret=[]
    for l in a:
        for (m,row) in enumerate(l.array_qty):
            for (n,cell_qty) in enumerate(row):
               state_id=(m,n)
               ml=OrderMoveLineData(state_id=state_id,
                                    linekey_id=l.linekey_id,
                                    asset_qty=cell_qty,
                                    )
               ret.append(ml)
    return ret

def plk_lines_to_int_lines(plk_lines             )              :
    ret=[]
    for l in plk_lines:
        k = (l.state_id, l.linekey_id.product_id  )
        ret.append( OrderMoveLineData.fromkv(k, l.val() ) )
    return ret

#Bundle operations
def default_bundle_PLK_lines(bint          ,plk_lines             )             :
    b_dict = {}
    order_line_map ={}
    for l in plk_lines:
        order_line_map[l.linekey_id.product_id] = l
    ret=[]
    for (b_id,components) in bint.todict().items():
       b_sum = sum([cq for (cid,cq) in components])
       if b_id in order_line_map:
           l = order_line_map[b_id]
           b_price = l.linekey_id.price
           desc = l.linekey_id.description
           tax_type = l.linekey_id.tax_type
           disc_rate = l.linekey_id.discount_rate
       else:
           b_price = Fraction(1)
           desc = 'Bundle%d'%b_id
           tax_type = 'output2'
           disc_rate = 0           
       bval={'product_id':b_id,
             'description':desc,
             'tax_type':tax_type,
             'price':  b_price,
             'discount_rate':disc_rate}
       plk_list = []
       for (c_id, c_qty) in components:
           plk_id={'product_id':c_id,
                   'description':'SKU%d'%c_id,
                   'tax_type':'output2',
                   'price':  (b_price*(c_qty/b_sum) ),
                   'discount_rate':0}
           val = {'component_id':plk_id,
                  'component_qty':c_qty}
           plk_list.append(val)
       ret.append( (bval, plk_list) )
    b_dict['bundle_data'] = ret
    return BundlePLK.model_validate( b_dict )
    #return Bundle[ProductLineKey].model_validate( b_dict )

def bundle_lines_to_component_lines(bundle_lines          , bundles       )           :
    if bundles is None:
        bundles = {}        
    bundles = bundles.todict()    
    component_lines=[]
    for l in bundle_lines: #m.line_ids:
        # Check if this product_id is a bundle
        if l.linekey_id in bundles:
            # Expand bundle into component products
            bundle_components = bundles[l.linekey_id]
            line_val = l.val()
            for component_id, component_qty in bundle_components:
                # Calculate component quantities based on bundle quantity
                component_val = LineVal(
                    qty=line_val.qty * component_qty,
                    cr_qty=line_val.cr_qty * component_qty
                )
                component_plk = component_id                
                component_key = (l.state_id, component_plk)
                component_lines.append(OrderMoveLineData.fromkv(component_key, component_val))
        else:
            # Regular product, not a bundle
            k=(l.state_id,l.linekey_id)
            component_lines.append(OrderMoveLineData.fromkv(k, l.val()))
    return component_lines

def component_lines_to_bundle_lines(component_lines          ,bundles       )           :
    if bundles is None:
        bundles = {}        
    bundles = bundles.todict()
    def bundle_allocation(compqty_to_bundle,
                          component_qty):
        ret=[]
        for (bundle_id, c_qty) in compqty_to_bundle:
            if component_qty > c_qty:
                b_qty = component_qty // c_qty
                ret.append( (bundle_id,b_qty) )
                component_qty = component_qty - (b_qty*c_qty)
            else:
                ret.append( (bundle_id, 0) )

        return ret
    if bundles is None:
        bundles = {}
    reverse_bundle_map = {}
    for b_id,components in bundles.items():
        for c_id, c_qty in components:               
            v=reverse_bundle_map.setdefault( c_id, [] )
            v.append( (b_id, c_qty) )
    #Group moves by state_id and then by product_id (component)
    move_map = OrderedDict()
    for ml in component_lines: #m.line_ids:
        v = move_map.setdefault(ml.state_id, OrderedDict() )
        vv = v.setdefault(ml.linekey_id, [] )           
        vv.append( int(ml.val()) )
    bundle_lines=[]
    for (state_id,vv) in move_map.items():
        d=OrderedDict() 
        for (component_id, qtys) in vv.items():
            if component_id in reverse_bundle_map:
                b_out = bundle_allocation( reverse_bundle_map[component_id], sum(qtys) )
            else:
                b_out = [ (component_id, sum(qtys)) ]
            #Group components and bundle qtys by bundle_id (next step will be
            #to find the minimum)
            for (bundle_id,qty) in b_out:
                x = d.setdefault(bundle_id, [])
                x.append( (component_id, qty) )

        for (bundle_id, bqtys) in d.items():
            key = (state_id, bundle_id)
            #find minimum 
            val = min( [bqty for (cid,bqty) in bqtys] )
            bundle_lines.append( OrderMoveLineData.fromkv(key, LineVal.fromint(val) )) 
    return bundle_lines


#massign operations
def array_assignment(a, tot):
    ret=[]
    arr=copy.deepcopy(a)
    arr.reverse() #allocate from right to left
    for a in arr:
        res=tot-a
        if res >= lineval(0,0):
            ret.append(a)
            tot = res
        else:
            ret.append(tot)
            tot = lineval(0,0)
    ret.reverse() #back
    return (ret, tot)
def sub_list(a,b):
    ret=[]
    for (x,y) in zip(a,b):
        ret.append(x-y)
    return ret
def validate_array_lines(lines           )                         :
    ret=[]
    ret_df=[]
    for l in lines:
        array_qty = copy.deepcopy(l.array_qty)
        r0=array_qty[0]
        #remain=sum(r0, start=lineval(0,0) )
        remain = sum(r0 +[lineval(0,0)] )
        
        valid_rows=[]
        df_rows=[]
        for r in array_qty[1:]:
            (valid, _) = array_assignment(r, remain)            
            #remain = sum(valid, start=lineval(0,0) )
            remain = sum(valid +[lineval(0,0)] )
            df=sub_list(valid, r)
            #df.reverse()
            df_rows.append(df   )
            
            valid_rows.append( valid )
        valid=[r0]+ valid_rows
        df_out = [[lineval(0,0) for x in range(len(r0))]]+df_rows
        ret.append(OrderMoveLineArray(linekey_id=l.linekey_id,
                                      array_qty=valid)
                   )
        ret_df.append(OrderMoveLineArray(linekey_id=l.linekey_id,
                                         array_qty=df_out)
                   )
        
    return ret,ret_df
def validate_lines(lines          )                       :
    a=move_to_array_lines(lines)
    v,df=validate_array_lines(a)
    return array_to_move_lines(v), array_to_move_lines(df)

def add_array_lines(a           ,b           )            :
    d=OrderedDict()
    for l in a:
        d[l.linekey_id]=l.array_qty
    for l in b:
        if l.linekey_id in d:
            #print (d[l.linekey_id])
            #print (l.array_qty)
            d[l.linekey_id] = add_array( d[l.linekey_id], l.array_qty )
        else:
            d[l.linekey_id] = l.array_qty
    ret=[]
    for lk,a in d.items():
        ret.append(OrderMoveLineArray(linekey_id=lk,
                                      array_qty=a)
                   )
    return ret
def assert_zero(a           )      :
    ret=True
    for l in a:
        for row in l.array_qty:
            for c in row:
                ret = ret and (c == lineval(0,0))
    return ret
def array_lines_reduced(a           ):
    ret=[]
    for l in a:
        out=[]
        for row in l.array_qty:
            row_out=[]
            for c in row:
                row_out.append( c.meval() )
            out.append(row_out)
        ret.append(OrderMoveLineArray(linekey_id=l.linekey_id,
                                      array_qty=out)
                   )
    return ret

def move_array_lines(lines           )            :
    ret=[]
    for l in lines:
        r0=l.array_qty[0]
        #remain=sum(r0, start=lineval(0,0) )
        remain=sum(r0 + [lineval(0,0)] )
        rows = copy.deepcopy(l.array_qty)
        rows.reverse() #from bottom up
        new_rows=[]
        for row in rows:
            (moved, remain) = array_assignment(row, remain)
            new_rows.append(moved)
        new_rows.reverse() #reverse back
        ret.append(OrderMoveLineArray(linekey_id=l.linekey_id,
                                      array_qty=new_rows)
                   )
    return ret

def move_lines(lines          )                        :
    a=move_to_array_lines(lines)
    valid,df=validate_array_lines(a)
    moved = move_array_lines(valid)
    return meval_lines(array_to_move_lines(moved)), array_to_move_lines(df)
    
#show and parse
STATE_IDS = [ (x,0) for x in range(4) ] + [(3,1)]    
def statemap( state_id           )       :
    return "STATE%d%d"%(state_id)
def showpivot_lines(lines          )     :
    linekey_ids = []
    line_map = OrderedDict()
    for l in lines: #a.line_ids:
        if l.linekey_id not in linekey_ids:
            linekey_ids.append( l.linekey_id )
        k = l.linekey_id, l.state_id
        assert (l.state_id in STATE_IDS)
        v = line_map.setdefault(k, [])
        #if l.val()==lineval(0,0):
        #    v.append( '')
        #else:
        v.append( l.val() )
    header = ['']+[statemap(x) for x in STATE_IDS]
    data=[]
    for line_key in linekey_ids:
        row=[str(line_key)]
        for state_id in STATE_IDS:
            k=(line_key, state_id)
            vals = line_map.get(k, [])
            val = sum(vals,start=lineval(0,0))
            if val==lineval(0,0):
                row.append('')
            else:
                row.append( str(val) )
        data.append(row)
    ret=tabulate(data,headers=header,tablefmt="grid",stralign="right")
    return ret
def showarray_lines(lines           , tra=False)     :
    tr_array=tra
    if len(lines)>0:
        (m_max,n_max)=get_shape(lines[0].array_qty)
    else:
        (m_max,n_max)=(0,0)
    if tr_array:
        header = ['linekey_id','state_id', ]+[str(i) for i in range(m_max)]
    else:
        header = ['linekey_id','state_id', ]+[str(i) for i in range(n_max)]
    data=[]
    for l in lines:     
        line=[]
        if tr_array:
            array=transpose(l.array_qty)
        else:
            array=l.array_qty
        for (m,arow) in enumerate(array):           
            row=[str(l.linekey_id), str(m)]
            for (n,c_qty) in enumerate(arow):
               state_id=(m,n)
               if c_qty==lineval(0,0):
                  row.append('   ~')
               else:
                   row.append( str(c_qty.meval()) )
            line.append(row)
        tr=transpose(line)
        line=[]
        for i,x in enumerate(tr):
            if i==0:
                k=x[0]
                nx=len(x)
                h=[" " for c in range(nx)]
                h[nx//2]=k
                y=h
            else:
                y=x
            line.append( "\n".join(y) )
        data.append(line)
    ret=tabulate(data,headers=header,tablefmt="grid",stralign="right")
    return ret
def printlines(*arg, **kwarg):
    for lns in arg:
        if isinstance(lns, str):
            print ("\n"+lns)
        else:
            a=move_to_array_lines(lns)
            print (showarray_lines(a,**kwarg) )
def printmove_lines(*arg, **kwarg):
    for lns in arg:
        if isinstance(lns, str):
            print ("\n"+lns)
        else:
            r=show_lines(lns)
            print (r)
def show_lines(lines          )     :
    if len(lines)>0:
        h=lines[0].grid_header()
        data=[]
        for l in lines:
            data.append(l.grid_data())
        ret=tabulate(data,headers=h,tablefmt="grid")
    else:
        ret=''
    return ret

def parse_grid_table(text):
    def parse_cell(c):
        morerows,morecols,lineoffset,content=c
        return content.data[0]
    parser=docutils.parsers.rst.tableparser.GridTableParser()
    block=statemachine.StringList( text.strip().split('\n') )
    widths,hds,rows=parser.parse(block)
    header=[parse_cell(h) for h in hds[0]]
    data=[]
    for r in rows:
        data.append( [parse_cell(c) for c in r] )    
    return data

def parse_plk_grid_lines(text):
    data=parse_grid_table(text)
    line_ids=[]    
    for row in data:
        state_id,product_id,description,tax_type,price,discount_rate,asset_qty=row
        linekey={'description':description,
                 'discount_rate':discount_rate,
                 'price':price,
                 'product_id':int(product_id),
                 'tax_type':tax_type}
        line={'state_id':eval(state_id),
              'linekey_id':linekey,
              'asset_qty':LineVal.fromscalar(asset_qty)}
        line_ids.append( OrderMoveLineData[ProductLineKey].model_validate(line) )
    return line_ids
def parse_int_grid_lines(text):
    data=parse_grid_table(text)
    line_ids=[]
    for row in data:
        state_id,linekey_id,asset_qty=row
        line={'state_id':eval(state_id),
              'linekey_id':int(linekey_id),
              'asset_qty':LineVal.fromscalar(asset_qty)
              }
        line_ids.append(OrderMoveLineData[int].model_validate(line) )
    return line_ids         
        
def parse_str_grid_lines(text):
    data=parse_grid_table(text)
    line_ids=[]
    for row in data:
        state_id,linekey_id,asset_qty=row
        line={'state_id':eval(state_id),
              'linekey_id':linekey_id,
              'asset_qty':LineVal.fromscalar(asset_qty)
              }
        line_ids.append(OrderMoveLineData[str].model_validate(line) )
    return line_ids         

def order_move_line_data(state_id,linekey, qty, qty_cr):
    """
    Convenience function to build various order lines
    including PLK, str, int
    """
    return OrderMoveLineData.fromkv( ( state_id, linekey), lineval(qty,qty_cr) )
def prepare_line(sku, mult, m=1, n=0):
    return mul_lines(minc_lines(sku, m=m,n=n), mult)

