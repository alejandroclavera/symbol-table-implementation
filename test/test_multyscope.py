import pytest
from symtab.symtab import MultiScopeSymTab
from symtab.data import Entry

symbols = [('s1', 1, 0, 0), 
            ('s2', 1, 0, 1), 
            ('s3', 2, 0,2), 
            ('s4', 2, 0, 3, {'return':'int'})
        ]

def test_add_new_symbol():
    syntab = MultiScopeSymTab()
    # add symbol
    table_entry =  syntab.sym_add('symbol', 1, 1, 0)
    assert table_entry is not None
    assert table_entry == Entry('symbol', 1, 1, 0)


def test_add_multiples_new_symbol():
    syntab = MultiScopeSymTab()
    for symbol in symbols:
        assert syntab.sym_add(*symbol) is not None
    table_entry  =  syntab.sym_add('symbol', 1, 1, 0)
    assert table_entry is not None


def test_add_duplicated_symbol():
    syntab = MultiScopeSymTab()
    assert syntab.sym_add('symbol', 1, 1, 0) is not None
    assert syntab.sym_add('symbol', 3, 1, 0) is None


def test_remove_symbol():
    syntab = MultiScopeSymTab()
    syntab.sym_add('symbol', 1, 1, 0) is not None
    syntab.sym_remove('symbol')
    assert syntab.sym_lookup('symbol') is None
    with pytest.raises(Exception) as e_info:
        syntab.sym_remove('symbol')


# Test SCOPES
def test_add_symbol_new_register_symbol():
    syntab = MultiScopeSymTab()
    syntab.sym_add('symbol', 1, 1, 0) is not None
    syntab.sym_push_scope()
    syntab.sym_add('symbol', 2, 1, 0) is not None    


def test_find_symbol_current_scope():
    syntab = MultiScopeSymTab()
    syntab.sym_push_scope()
    symbol = syntab.sym_add('symbol', 2, 1, 0)
    
    table_entry = syntab.sym_lookup('symbol')
    assert table_entry == symbol and table_entry is not None 


def test_find_symbol_other_scope():
    syntab = MultiScopeSymTab()
    symbol = syntab.sym_add('symbol', 2, 1, 0)
    syntab.sym_push_scope()
    
    # find symbol registered in global scope
    table_entry = syntab.sym_lookup('symbol')
    assert table_entry == symbol and table_entry is not None 

    symbol = syntab.sym_add('symbol2', 2, 1, 0)
    syntab.sym_push_scope()

    table_entry = syntab.sym_lookup('symbol2')
    assert table_entry == symbol and table_entry is not None


def test_pop_current_scope():
    syntab = MultiScopeSymTab()
    symbol = syntab.sym_add('symbol', 2, 1, 0)
    syntab.sym_push_scope()

    to_delete = syntab.sym_add('symbolDeleted', 2, 1, 0)
    assert syntab.sym_lookup('symbolDeleted') == to_delete

    syntab.sym_pop_scope()
    assert syntab.sym_lookup('symbolDeleted') is None


def test_pop_global_scope():
    syntab = MultiScopeSymTab()
    with pytest.raises(Exception) as e_info:
        syntab.sym_pop_scope()

    





