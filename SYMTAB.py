from abc import ABC, abstractmethod

class Entry:
    '''
    Entry of a SYMTAB
    '''
    symbol: str
    type: str
    size:int
    data:dict

    def __init__(self, symbol:str, type:str, size:int, data={}): 
        self.symbol = symbol
        self.type = type
        self.size = size
        self.data = data


class SYMTAB(ABC):
    '''
    Abstract class definition of SYMTAB
    '''
    @abstractmethod
    def sym_add(self, symbol:str, type:str, size:int, data={}):
        pass
    
    @abstractmethod
    def sym_lookup(self, symbol:str):
        pass

    @abstractmethod
    def sym_remove(self, symbol:str):
        pass


class SimpleSymTab(SYMTAB):
    '''
    Symbol table implementation without scope support.
    '''
    
    def __init__(self):
        self.symbol_table = []


    def sym_add(self, symbol:str, type:str, size:int, data={}):
        # find if the symbol are registered in the table
        entry_in_table = self.sym_lookup(symbol)
        if not entry_in_table is None:
            return None
        # registre new entry in the symbol table
        symbol_entry = Entry(symbol, type, size, data) 
        self.symbol_table.append(symbol_entry)
        return symbol_entry 


    def sym_lookup(self, symbol:str):
        for entry in self.symbol_table:
            if symbol == entry.symbol:
                return entry
            return None


    def sym_remove(self, symbol:str):
        # find if the symbol are registered in the table
        entry_in_table = self.sym_lookup(symbol)
        if entry_in_table is None:
            raise Exception(f'Symbol {symbol} not registered')