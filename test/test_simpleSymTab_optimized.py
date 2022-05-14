import pytest
from symtab.symtab import SimpleSymTab, Entry

symbols = [('s1', 1, 0, 0), 
            ('s2', 1, 0, 1), 
            ('s3', 2, 0,2), 
            ('s4', 2, 0, 3, {'return':'int'})
        ]

def test_add_new_symbol():
    syntab = SimpleSymTab(optimized=True)
    # add symbol
    table_entry =  syntab.sym_add('symbol', 1, 1, 0)
    assert table_entry is not None
    assert table_entry == Entry('symbol', 1, 1, 0)


def test_add_multiples_new_symbol():
    syntab = SimpleSymTab(optimized=True)
    for symbol in symbols:
        assert syntab.sym_add(*symbol) is not None
    table_entry  =  syntab.sym_add('symbol', 1, 1, 0)
    assert table_entry is not None


def test_add_duplicated_symbol():
    syntab = SimpleSymTab(optimized=True)
    assert syntab.sym_add('symbol', 1, 1, 0) is not None
    assert syntab.sym_add('symbol', 3, 1, 0) is None


def test_remove_symbol():
    syntab = SimpleSymTab(optimized=True)
    syntab.sym_add('symbol', 1, 1, 0) is not None
    syntab.sym_remove('symbol')
    assert syntab.sym_lookup('symbol') is None
    with pytest.raises(Exception) as e_info:
        syntab.sym_remove('symbol')