# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import
from fractions import Fraction
import sys


class LineVal(object):
    def __init__(self, qty=None, cr_qty=None):
        if qty is None:
            qty = Fraction(0)
        if cr_qty is None:
            cr_qty = Fraction(0)
        
        # Convert to Fraction if needed
        if isinstance(qty, (int, float)):
            qty = Fraction(qty)
        elif isinstance(qty, str):
            qty = Fraction(qty)
            
        if isinstance(cr_qty, (int, float)):
            cr_qty = Fraction(cr_qty)
        elif isinstance(cr_qty, str):
            cr_qty = Fraction(cr_qty)
            
        self.qty = qty
        self.cr_qty = cr_qty
    
    def __add__(self, b):
        sc = self.fromscalar(b)
        return LineVal(qty=self.qty+sc.qty,
                       cr_qty=self.cr_qty+sc.cr_qty)
    
    def __radd__(self, b):
        return self.__add__(b)
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "%s;%s" % (self.qty, self.cr_qty)
    
    def __int__(self):
        return int(self.qty - self.cr_qty)
    
    @staticmethod
    def fromint(a):
        if a > 0:
            ret = LineVal(qty=Fraction(a),
                         cr_qty=Fraction(0))
        elif a < 0:
            ret = LineVal(qty=Fraction(0),
                         cr_qty=Fraction(abs(a)))
        else:
            ret = LineVal(qty=Fraction(0),
                         cr_qty=Fraction(0))
        return ret
    
    @staticmethod
    def fromscalar(sc):
        
        if isinstance(sc, (int, float)):  # Python 2.7 compatible union syntax
            a = Fraction(sc)
        elif isinstance(sc, str):
            if ';' in sc:
                q, crq = sc.split(';')
                ret = LineVal(qty=Fraction(q),
                             cr_qty=Fraction(crq))
                return ret
            else:
                a = Fraction(sc)            
        elif isinstance(sc, Fraction):
            a = sc
        elif isinstance(sc, LineVal):
            return sc
        else:
            #print (sc,isinstance(sc,list) )
            raise Exception("Type not known")
        
        if a > 0:
            ret = LineVal(qty=Fraction(a),
                         cr_qty=Fraction(0))
        elif a < 0:
            ret = LineVal(qty=Fraction(0),
                         cr_qty=Fraction(abs(a)))
        else:
            ret = LineVal(qty=Fraction(0),
                         cr_qty=Fraction(0))
        return ret        
    
    @staticmethod
    def mappend(a, b):
        return a + b
    
    @staticmethod
    def mneg(a):
        return LineVal(qty=a.cr_qty,
                       cr_qty=a.qty)
    
    def __neg__(self):
        return self.mneg(self)
    
    def __sub__(self, other):
        sc = self.fromscalar(other)
        return (self + (self.mneg(sc)))
    
    def __rsub__(self, other):
        sc = self.fromscalar(other)
        return (sc + (self.mneg(self)))    
    
    @staticmethod
    def mzero():
        return LineVal(qty=Fraction(0), cr_qty=Fraction(0))
    
    def meval(self):
        a = self
        q_min = min(a.qty, a.cr_qty)
        ret = LineVal(qty=a.qty-q_min,
                     cr_qty=a.cr_qty-q_min)
        return ret
    
    def diff(self):
        return (self.qty - self.cr_qty)
    
    def __eq__(self, b):
        sc = self.fromscalar(b)
        ret = (self.qty+sc.cr_qty) == (self.cr_qty+sc.qty)
        return ret
    
    def __lt__(self, other):
        sc = self.fromscalar(other)
        ret = (self.qty+sc.cr_qty) < (self.cr_qty+sc.qty)
        return ret
    
    def __le__(self, other):
        sc = self.fromscalar(other)
        return ((self < sc) or (self == sc))
    
    def __gt__(self, other):
        sc = self.fromscalar(other)
        ret = (self.qty+sc.cr_qty) > (self.cr_qty+sc.qty)
        return ret
    
    def __ge__(self, other):
        sc = self.fromscalar(other)
        return ((self > sc) or (self == sc))
    
    def __mul__(self, other):
        sc = self.fromscalar(other)
        a = self
        b = sc
        ret = LineVal(qty=a.qty*b.qty+a.cr_qty*b.cr_qty,
                      cr_qty=a.qty*b.cr_qty+a.cr_qty*b.qty)
        return ret
    
    def __rmul__(self, other):
        return self.__mul__(other)        
    
    def reciprocal(self):
        a = self
        cr_qty = (a.qty+a.cr_qty) + (1/(a.qty+a.cr_qty))
        qty = cr_qty + 1/(a.qty-a.cr_qty)
        return LineVal(qty=qty,
                       cr_qty=cr_qty)
    
    def __truediv__(self, other):
        a = self
        b = self.fromscalar(other)
        return (a * (b.reciprocal()))
    
    def __div__(self, other):  # Python 2.7 division operator
        return self.__truediv__(other)
    
    def __rtruediv__(self, other):
        a = self
        b = self.fromscalar(other)
        return (a.reciprocal() * b)
    
    def __rdiv__(self, other):  # Python 2.7 division operator
        return self.__rtruediv__(other)
    
    def __iadd__(self, b):
        return (self + b)    
    
    def __isub__(self, other):
        return (self - other)
    
    def __imul__(self, other):
        return (self * other)
    
    def __itruediv__(self, other):
        return (self / other)
    
    def __idiv__(self, other):  # Python 2.7 division operator
        return self.__itruediv__(other)
    
    def model_dump(self):
        """Pydantic compatibility method for serialization"""
        return {
            'qty': str(self.qty),
            'cr_qty': str(self.cr_qty)
        }
    
    @classmethod
    def model_validate(cls, data):
        """Pydantic compatibility method for deserialization"""
        return cls(qty=data['qty'], cr_qty=data['cr_qty'])

def lineval(qty, cr_qty):
    return LineVal(qty=qty, cr_qty=cr_qty)

LINE_VAL_ZERO = LineVal.mzero()

class ProductLineKey(object):
    def __init__(self, product_id, description, tax_type, price, discount_rate):
        self.product_id = product_id
        self.description = description
        self.tax_type = tax_type
        
        # Convert to Fraction if needed
        if isinstance(price, (int, float)):
            price = Fraction(price)
        elif isinstance(price, str):
            price = Fraction(price)
        self.price = price
        
        if isinstance(discount_rate, (int, float)):
            discount_rate = Fraction(discount_rate)
        elif isinstance(discount_rate, str):
            discount_rate = Fraction(discount_rate)
        self.discount_rate = discount_rate
    def header(self):
        return ['product_id','description','tax_type','price',
                'discount_rate']
    def get_description(self):
        return self.description
        width=60
        n=len(self.description)
        ret=[]
        for i in range( 1+(n//width) ):
            a=i*width
            b=i*width+width
            if (a<=n):
               if (b<=n):
                   ret.append(self.description[a:b])
               else:
                   ret.append(self.description[a:n])
        return "\n".join(ret)    
    def key(self):
        return (self.product_id, self.get_description(), self.tax_type, self.price, self.discount_rate)
    def key2(self):
        return (self.product_id, self.get_description(), self.tax_type, float(self.price), float(self.discount_rate))
    def __repr__(self):
        return str(self.key())
    def __eq__(self, b):
        return self.key() == b.key()
    
    def __lt__(self, other):
        return self.key() < other.key()
    
    def __hash__(self):
        return hash(self.key())
    
    @classmethod
    def model_validate(cls, data):
        """Pydantic compatibility method for deserialization"""
        return cls(
            product_id=data['product_id'],
            description=data['description'],
            tax_type=data['tax_type'],
            price=data['price'],
            discount_rate=data['discount_rate']
        )
    def model_dump(self):
        v={'product_id':self.product_id,
           'description':self.description,
           'price':str(self.price),
           'tax_type':self.tax_type,
           'discount_rate':str(self.discount_rate)}
        return v
class ProductLineKeyWHS(object):
    def __init__(self, product_id, description, tax_type,
                       price, discount_rate,
                       location_id,location_dest_id):
        self.product_id = product_id
        self.description = description
        self.tax_type = tax_type
        
        # Convert to Fraction if needed
        if isinstance(price, (int, float)):
            price = Fraction(price)
        elif isinstance(price, str):
            price = Fraction(price)
        self.price = price
        
        if isinstance(discount_rate, (int, float)):
            discount_rate = Fraction(discount_rate)
        elif isinstance(discount_rate, str):
            discount_rate = Fraction(discount_rate)
        self.discount_rate = discount_rate
        self.location_id=location_id
        self.location_dest_id=location_dest_id
    def header(self):
        return ['product_id','description','tax_type','price',
                'discount_rate','location_id','location_dest_id']
    def get_description(self):
        return self.description
        width=60
        n=len(self.description)
        ret=[]
        for i in range( 1+(n//width) ):
            a=i*width
            b=i*width+width
            if (a<=n):
               if (b<=n):
                   ret.append(self.description[a:b])
               else:
                   ret.append(self.description[a:n])
        return "\n".join(ret)
    def key(self):
        return (self.product_id, self.get_description(), self.tax_type, self.price, self.discount_rate,self.location_id,self.location_dest_id)
    def key2(self):
        return (self.product_id, self.get_description(), self.tax_type, float(self.price), float(self.discount_rate),self.location_id,self.location_dest_id)
    
    def __repr__(self):
        return str(self.key())
    def __eq__(self, b):
        return self.key() == b.key()
    
    def __lt__(self, other):
        return self.key() < other.key()
    
    def __hash__(self):
        return hash(self.key())
    
    @classmethod
    def model_validate(cls, data):
        """Pydantic compatibility method for deserialization"""
        return cls(
            product_id=data['product_id'],
            description=data['description'],
            tax_type=data['tax_type'],
            price=data['price'],
            discount_rate=data['discount_rate'],
            location_id=data['location_id'],
            location_dest_id=data['location_dest_id']
        )
    def model_dump(self):
        v={'product_id':self.product_id,
           'description':self.description,
           'price':str(self.price),
           'tax_type':self.tax_type,
           'discount_rate':str(self.discount_rate),
           'location_id':self.location_id,
           'location_dest_id':self.location_dest_id}
        return v
    
class BundleComponent(object):
    def __init__(self, component_id, component_qty):
        self.component_id = component_id
        self.component_qty = component_qty
        #if isinstance(component_qty, (int, float)):
        #    component_qty = Fraction(component_qty)
        #elif isinstance(component_qty, str):
        #    component_qty = Fraction(component_qty)
        #self.component_qty = component_qty

class Bundle(object):
    def __init__(self, bundle_data):
        self.bundle_data = bundle_data
    
    def todict(self):
        ret = {}
        for (b_id, components) in self.bundle_data:
            ret[b_id] = [(c.component_id, c.component_qty) for c in components]
        return ret
    
    @classmethod
    def model_validate(cls, data):
        """Pydantic compatibility method for deserialization"""
        bd = data.get('bundle_data', [])
        bundle_data=[]
        for (b_id, c_dicts) in bd:
            components=[]
            for c in c_dicts:
                c_id=c['component_id']
                c_qty=c['component_qty']
                components.append(BundleComponent(c_id,c_qty))
            bundle_data.append( (b_id, components) )
        return cls(bundle_data=bundle_data)
BundleComponentInt = Bundle
BundleInt = Bundle

class BundlePLK(Bundle):
    @classmethod
    def model_validate(cls, data):
        """Pydantic compatibility method for deserialization"""
        bd = data.get('bundle_data', [])
        bundle_data=[]
        for (b_id, c_dicts) in bd:
            components=[]
            b_plk=ProductLineKey.model_validate(b_id)
            for c in c_dicts:
                c_id=c['component_id']
                c_plk=ProductLineKey.model_validate(c_id)
                c_qty=c['component_qty']
                components.append(BundleComponent(c_plk,c_qty))
            bundle_data.append( (b_plk, components) )
        return cls(bundle_data=bundle_data)
    
#BundlePLK = Bundle

class OrderMoveLineData(object):
    def __init__(self, state_id, linekey_id, asset_qty):
        self.state_id = state_id
        self.linekey_id = linekey_id
        self.asset_qty = asset_qty
        
        # Convert to Fraction if needed
        #if isinstance(product_qty, (int, float)):
        #    product_qty = Fraction(product_qty)
        #elif isinstance(product_qty, str):
        #    product_qty = Fraction(product_qty)
        #self.product_qty = product_qty
        
        #if isinstance(product_cr_qty, (int, float)):
        #    product_cr_qty = Fraction(product_cr_qty)
        #elif isinstance(product_cr_qty, str):
        #    product_cr_qty = Fraction(product_cr_qty)
        #self.product_cr_qty = product_cr_qty
    def grid_header(self):
        if isinstance(self.linekey_id,ProductLineKey):
            return ['state_id']+self.linekey_id.header()+['asset_qty']
        elif isinstance(self.linekey_id,ProductLineKeyWHS):
            return ['state_id']+self.linekey_id.header()+['asset_qty']
        else:
            return ['state_id', 'linekey_id', 'asset_qty']
    def grid_data(self):
        if isinstance(self.linekey_id,ProductLineKey):
            return [self.state_id]+list(self.linekey_id.key())+[str(self.asset_qty)]
        elif isinstance(self.linekey_id,ProductLineKeyWHS):
            return [self.state_id]+list(self.linekey_id.key())+[str(self.asset_qty)]
        else:
            return [self.state_id, self.linekey_id, str(self.asset_qty)]    
    def key(self):
        return self.state_id, self.linekey_id
    def val(self):
        return self.asset_qty
    def __repr__(self):
        return str( (self.key(), self.val()))
    #def val_int(self):
    #    return int(self.val())
    
    @staticmethod
    def fromkv(k,v):
        state_id,linekey_id=k
        return OrderMoveLineData(state_id=state_id,
                                 linekey_id=linekey_id,
                                 asset_qty=v)

    def model_dump(self):
        if isinstance(self.linekey_id,int):
            linekey_id=self.linekey_id
        else:
            linekey_id=self.linekey_id.model_dump()
        v={'state_id':self.state_id,
           'linekey_id':linekey_id,
           'asset_qty':self.asset_qty.model_dump()}
        return v
#    def fromkv(k, v):
#        state_id, linekey_id = k
#        return OrderMoveLineData(state_id=state_id,
#                                linekey_id=linekey_id,
#                                product_qty=v.product_qty,
#                                product_cr_qty=v.product_cr_qty)
class OrderMoveLineDataPlk(OrderMoveLineData):

    def subtotal(self,line_amount_type):
        item=self
        item.product_qty=self.asset_qty.qty
        item.product_cr_qty=self.asset_qty.cr_qty
        item.price=self.linekey_id.price
        item.discount_rate=self.linekey_id.discount_rate
        item.tax_type=self.linekey_id.tax_type
        #print ['kocour', line_amount_type]
        ret=round(({"inclusive":(((item.price)*((item.product_qty)+(((-1)*item.product_cr_qty)))*((1)+(((-1)*((item.discount_rate)/(100))))))), "exclusive":(((item.price)*((item.product_qty)+(((-1)*item.product_cr_qty)))*((1)+(((-1)*((item.discount_rate)/(100)))))*(({"output2":(1.2), "none":(1), }[item.tax_type])))), "none":(((item.price)*((item.product_qty)+(((-1)*item.product_cr_qty)))*((1)+(((-1)*((item.discount_rate)/(100))))))), }[line_amount_type]),2)
        return ret        
    @classmethod        
    def model_validate(cls, data):
        return cls(data['state_id'],
                   ProductLineKey.model_validate( data['linekey_id'] ),
                   LineVal.model_validate( data['asset_qty'] ),
                  )
def create_plk_line(d):
    return OrderMoveLineDataPlk.model_validate(d)
class SaleConfirmation(object):
    def __init__(self, sale_id,date,date_due,
                       number,name,reference,state,typex,
                       line_amount_type,currency_code,external_id,
                       return_reason,action,
                       user_id, app_id,
                 line_ids):
        self.sale_order_id=sale_id
        self.date=date
        self.date_due=date_due
        self.number=number
        self.name=name
        self.reference=reference
        self.state=state
        self.type=typex
        self.line_amount_type=line_amount_type
        self.currency_code=currency_code
        self.external_id=external_id
        self.return_reason=return_reason
        self.action=action
        self.line_ids=line_ids
        self.user_id=user_id
        self.app_id=app_id
    def total(self):
        ret=0
        for l in self.line_ids:
            #print ('   ', l.linekey_id.tax_type)
            ret += l.subtotal(self.line_amount_type)
        return ret
    @classmethod
    def model_validate(cls,data):
        return cls(data['sale_order_id'],
                   data['date'],
                   data['date_due'],
                   data['number'],
                   data['name'],
                   data['reference'],
                   data['state'],
                   data['type'],
                   data['line_amount_type'],
                   data['currency_code'],
                   data['external_id'],
                   data['return_reason'],
                   data['action'],
                   data['user_id'],
                   data['app_id'],
                   map(create_plk_line,data['line_ids']) )
    def model_dump(self):
        line_ids=[]
        for l in self.line_ids:
            line_ids.append( l.model_dump() )
        v={'sale_order_id':self.sale_order_id,
           'date':self.date,
           'date_due':self.date_due,
           'number':self.number,
           'name':self.name,
           'reference':self.reference,
           'state':self.state,
           'type':self.type,
           'line_amount_type':self.line_amount_type,
           'currency_code':self.currency_code,
           'external_id':self.external_id,
           'return_reason':self.return_reason,
           'action':self.action,
           'user_id':self.user_id,
           'app_id':self.app_id,
           'line_ids':line_ids}
        return v

class OrderMoveLineArray(object):
    def __init__(self, linekey_id, array_qty):
        #self.state_id = state_id
        self.linekey_id = linekey_id
        self.array_qty = array_qty
    def __repr__(self):
        return str((self.linekey_id, self.array_qty))
        # self.product_qty = product_qty
    
    #def key(self):
    #    return self.state_id, self.linekey_id
    #
    #def val(self):
    #    return self.product_qty

class OrderMoveArray(object):
    def __init__(self, line_ids):
        self.line_ids = line_ids
