import pytest
from symtab.symtab import SimpleSymTab, Entry

symbols = [('s1', 'int', 0), 
            ('s2', 'int', 0), 
            ('s3', 'str', 0), 
            ('s4', 'str', {'return':'int'})
            ]

def test_add_new_symbol():
    syntab = SimpleSymTab()
    # add symbol
    table_entry =  syntab.sym_add('symbol', '', 1)
    assert table_entry is not None
    assert table_entry == Entry('symbol', '', 1)


def test_add_multiples_new_symbol():
    syntab = SimpleSymTab()
    for symbol in symbols:
        assert syntab.sym_add(*symbol) is not None
        table_entry =  syntab.sym_add('symbol', '', 1)
        assert table_entry is not None
        assert table_entry == Entry('symbol', '', 1)


def test_add_duplicated_symbol():
    syntab = SimpleSymTab()
    assert syntab.sym_add('symbol', '', 1) is not None
    assert syntab.sym_add('symbol', '2', 4) is None


def test_remove_symbol():
    syntab = SimpleSymTab()
    syntab.sym_add('symbol', '', 1) is not None
    syntab.sym_remove('symbol')
    assert syntab.sym_lookup('symbol') is None
    with pytest.raises(Exception) as e_info:
        syntab.sym_remove('symbol')