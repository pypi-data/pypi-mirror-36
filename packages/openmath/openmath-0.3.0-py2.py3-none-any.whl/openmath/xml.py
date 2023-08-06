from . import openmath as om
from lxml.etree import QName

openmath_ns = "http://www.openmath.org/OpenMath"

omtags = {
    "OMOBJ": om.OMObject,
    "OMR": om.OMReference,
    "OMI": om.OMInteger,
    "OMF": om.OMFloat,
    "OMSTR": om.OMString,
    "OMB": om.OMBytes,
    "OMS": om.OMSymbol,
    "OMV": om.OMVariable,
    "OMFOREIGN": om.OMForeign,
    "OMA": om.OMApplication,
    "OMATTR": om.OMAttribution,
    "OMATP": om.OMAttributionPairs,
    "OMBIND": om.OMBinding,
    "OMBVAR": om.OMBindVariables,
    "OME": om.OMError
    }

inv_omtags = dict((v,k) for k,v in omtags.items())
    
def tag_to_object(tag, check_ns=False):
    q = QName(tag)
    if check_ns and q.namespace != openmath_ns:
        raise ValueError('Invalid namespace')
    return omtags[q.localname]

def object_to_tag(obj, ns=True):
    tpl = '{%(ns)s}%(tag)s' if ns else '%(tag)s'
    return tpl % { "ns": openmath_ns, "tag": inv_omtags[obj.__class__] }
