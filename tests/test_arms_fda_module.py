from arms_fda_module import arms_fda_module
from arms_fda_module import __version__
import pytest

def test_version():
    assert __version__ == '0.1.0'

#test to check if getdf_fda_arms() returns a dictionary
def test_getjson_fda_arms():
    a = get_fda_arms(key = '91ycY1QG2K2gtDXnvHqwB1EvpN8WdKVGEBTLPZSf',year = ['2005','2006','2011'],variable = ['frwcnum','tacres'],category = ['age'],report = ['5','4'],farmtype = '',statecode = ['12','13'])
    actual = type(a)
    expected = dict
    assert actual == expected
    
    print("Passed test.")