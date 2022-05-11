from abc import ABC, abstractmethod

class Entry:
    '''
    Entry of a SYMTAB
    '''
    symbol: str
    type: str
    size:int
    data:dict

    def __init__(self, symbol:str, type:int, size:int, offset:int, data={}): 
        self.symbol = symbol
        self.type = type
        self.size = size
        self.offset = offset
        self.data = data

    def __eq__(self, other):
        return \
            self.symbol == other.symbol \
            and self.type == other.type \
            and self.size == other.size \
            and self.offset == other.offset \
            and self.data == other.data
        

class SYMTAB(ABC):
    '''
    Abstract class definition of SYMTAB
    '''
    @abstractmethod
    def sym_add(self, symbol:str, type:int, size:int, offset:int, data={}):
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

    def sym_add(self, symbol:str, type:int, size:int, offset:int, data={}):
        # find if the symbol are registered in the table
        entry_in_table = self.sym_lookup(symbol)
        if not entry_in_table is None:
            return None
        # registre new entry in the symbol table
        symbol_entry = Entry(symbol, type, size, offset, data) 
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
        self.symbol_table.remove(entry_in_table)


class MultiScopeSymTab(SYMTAB):
    '''
    Symbol table implementation with scope support.
    '''
    __scopes_stack__:list
    __global_scope__:SimpleSymTab
    __current_scope__:SimpleSymTab
    
    def __init__(self):
        self.__scopes_stack__ = []
        self.__global_scope__ = SimpleSymTab()
        self.__current_scope__ = self.__global_scope__


    def sym_add(self, symbol:str, type:int, size:int, offset:int, data={}):
        return self.__current_scope__.sym_add(symbol, type, size, offset, data)


    def sym_lookup(self, symbol:str):
        # find the symbol in all scopes
        for scope in self.__scopes_stack__.reverse():
            entry = scope.sym_lookup(symbol)
            if not entry is None:
                return entry
        return None


    def sym_remove(self, symbol:str):
        # find if the symbol are registered in the table
        entry_in_table = self.__current_scope__.sym_lookup(symbol)
        if entry_in_table is None:
            raise Exception(f'Symbol {symbol} not registered')

    
    def sym_global_add(self, symbol: str, type: str, size: int, data={}):
        return self.__global_scope__.sym_add(symbol, type, size, data)


    def sym_global_lookup(self, symbol: str):
        return self.__global_scope__.sym_lookup(symbol)


    def sym_global_remove(self, symbol: str):
        return self.__global_scope__.sym_remove(symbol)


    def sym_push_scope(self):
        self.__current_scope__ = SimpleSymTab()
        self.__scopes_stack__.append(self.__current_scope__)


    def sym_pop_scope(self):
        self.__scopes_stack__.pop()
        self.__current_scope__ = self.__scopes_stack__[-1]

    