from abc import ABC, abstractmethod
from symtab.data import Entry, ListStructure, HashStructure

       
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
    
    def __init__(self, optimized=False):
        if optimized:
            self.symbol_table = HashStructure()
        else:
            self.symbol_table = ListStructure()

    def sym_add(self, symbol:str, type:int, size:int, offset:int, data={}):
        # find if the symbol are registered in the table
        if symbol in self.symbol_table:
            return None
        # registre new entry in the symbol table
        symbol_entry = Entry(symbol, type, size, offset, data) 
        self.symbol_table.append(symbol_entry)
        return symbol_entry 


    def sym_lookup(self, symbol:str):
        return self.symbol_table.get(symbol)


    def sym_remove(self, symbol:str):
        self.symbol_table.remove(symbol)


class MultiScopeSymTab(SYMTAB):
    '''
    Symbol table implementation with scope support.
    '''
    __scopes_stack__:list
    __global_scope__:SimpleSymTab
    __current_scope__:SimpleSymTab
    
    def __init__(self, glob_optimization=True):
        self.__global_scope__ = SimpleSymTab(optimized=glob_optimization)
        self.__current_scope__ = self.__global_scope__
        self.__scopes_stack__ = [self.__global_scope__ ]


    def sym_add(self, symbol:str, type:int, size:int, offset:int, data={}):
        return self.__current_scope__.sym_add(symbol, type, size, offset, data)


    def sym_lookup(self, symbol:str):
        # find the symbol in all scopes
        for scope in reversed(self.__scopes_stack__):
            entry = scope.sym_lookup(symbol)
            if not entry is None:
                return entry
        return None


    def sym_remove(self, symbol:str):
        self.__current_scope__.sym_remove(symbol)

    
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
        if len(self.__scopes_stack__) == 1:
            raise Exception('Can\'t remove the global scope')
        self.__scopes_stack__.pop()
        self.__current_scope__ = self.__scopes_stack__[-1]

