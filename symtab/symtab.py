from abc import ABC, abstractmethod
from symtab.data import Entry, ListStructure, HashStructure


class SYMTAB(ABC):
    '''
    Abstract class definition of SYMTAB
    '''
    @abstractmethod
    def sym_add(self, symbol:str, type:int, size:int, offset:int, params={}):
        pass
    
    @abstractmethod
    def sym_lookup(self, symbol:str):
        pass

    @abstractmethod
    def sym_remove(self, symbol:str):
        pass


class SimpleSymTab(SYMTAB):
    """
    Symbol table implementation without scope support.

    Methods
    -------
    sym_add(symbol:str, type:int, size:int, offset:int, params={})
        Registre a new symbol in the symbol
    sym_lookup(symbol:str)
        Find a symbol in the symtab
    sym_remove(symbol:str)
        Remove a symbol of the symtab
    """
    
    def __init__(self, optimized=False):
        """
        Parameters
        ----------
        optimized : bool, optional
            If the symtab use a Hashmap to store the symbols(default is False)
        """
        if optimized:
            self.symbol_table = HashStructure()
        else:
            self.symbol_table = ListStructure()


    def sym_add(self, symbol:str, type:int, size:int, offset:int, params={}):
        """ Stores a new symbol in the symtab

        Parameters
        ----------
        symbol : str
            lexeme of the symbol
        type : int
            type of the symbol
        size : int
            size of the symbol
        offset : int
            offset of the symbol
        params : dict, optional
            extension of the symbol attributes(default {})
        Returns
        -------
        Entry
            Entry stored in the symbol table or None in case that symbol is registered
        """
        # find if the symbol are registered in the table
        if symbol in self.symbol_table:
            return None
        # registre new entry in the symbol table
        symbol_entry = Entry(symbol, type, size, offset, params) 
        self.symbol_table.append(symbol_entry)
        return symbol_entry 


    def sym_lookup(self, symbol:str):
        """ Find a symbol in the symtab

        Parameters
        ----------
        symbol : str
            lexeme of the symbol to find
       
        Returns
        -------
        Entry
            Entry stored in the symbol table or None in case that symbol is not found
        """
        return self.symbol_table.get(symbol)


    def sym_remove(self, symbol:str):
        """ Remove a symbol

        Parameters
        ----------
        symbol : str
            lexeme of the symbol to remove
       
         Raises
        ------
        Exception
            If the symbol it is not found
        """
        self.symbol_table.remove(symbol)


class MultiScopeSymTab(SYMTAB):
    """
    Symbol table implementation with scope support.

    Methods
    -------
    sym_add(symbol:str, type:int, size:int, offset:int, params={})
        Registre a new symbol in the current scope
    sym_lookup(symbol:str, in_current_scope=False)
        Find a symbol in the current scope
    sym_remove(symbol:str)
        Remove a symbol of the current scope
    sym_global_add(symbol: str, type: str, size: int, params={})
        Add new symbol in the global scope
    sym_global_lookup(symbol: str)
        Find a symbol in the global scope
    sym_global_remove(symbol: str)
        Remove a symbol stored in the global scope
    sym_push_scope(optimized=False)
        Push the current scope in the stack and create a new scope
    sym_pop_scope()
        Remove the current scope and get the previus scope in the stack
    """
    __scopes_stack__:list
    __global_scope__:SimpleSymTab
    __current_scope__:SimpleSymTab
    
    def __init__(self, glob_optimization=True):
        """
        Parameters
        ----------
        glob_optimization : bool, optional
            If the global scope use a Hashmap to store the symbols(default is True)
        """
        self.__global_scope__ = SimpleSymTab(optimized=glob_optimization)
        self.__current_scope__ = self.__global_scope__
        self.__scopes_stack__ = [self.__global_scope__ ]


    def sym_add(self, symbol:str, type:int, size:int, offset:int, params={}):
        """ Stores a new symbol in the current scope, if it doesn't have any scope the symbol is stored in
            the global scope

        Parameters
        ----------
        symbol : str
            lexeme of the symbol
        type : int
            type of the symbol
        size : int
            size of the symbol
        offset : int
            offset of the symbol
        params : dict, optional
            extension of the symbol attributes(default {})
         Returns
        -------
        Entry
            Entry stored in the symbol table or None in case that symbol is registered
        """
        return self.__current_scope__.sym_add(symbol, type, size, offset, params)


    def sym_lookup(self, symbol:str, in_current_scope=False):
        """ Find a symbol in the symtab, if the symbol was not found in the current scope, it will
        search in the previus scopes

        Parameters
        ----------
        symbol : str
            lexeme of the symbol to find
        in_current_scope : bool, optional
            find symbol only in the current scope
        Returns
        -------
        Entry
            Entry stored in the symbol table or None in case that symbol is not found
        """
        # find in current scope if it is necesary
        if in_current_scope:
            return self.__current_scope__.sym_lookup(symbol)

        # find the symbol in all scopes
        for scope in reversed(self.__scopes_stack__):
            entry = scope.sym_lookup(symbol)
            if not entry is None:
                return entry
        return None


    def sym_remove(self, symbol:str):
        """ Remove a symbol in the current scope, if it doesn't have any scope the symbol is removed in
            the global scope

        Parameters
        ----------
        symbol : str
            lexeme of the symbol to remove
       
         Raises
        ------
        Exception
            If the symbol it is not found
        """
        self.__current_scope__.sym_remove(symbol)

    
    def sym_global_add(self, symbol: str, type: str, size: int, params={}):
        """ Stores a new symbol in the the global scope

        Parameters
        ----------
        symbol : str
            lexeme of the symbol
        type : int
            type of the symbol
        size : int
            size of the symbol
        offset : int
            offset of the symbol
        params=dict, optional
            extension of the symbol attributes(default {})
         Returns
        -------
        Entry
            Entry stored in the symbol table or None in case that symbol is registered
        """
        return self.__global_scope__.sym_add(symbol, type, size, params)


    def sym_global_lookup(self, symbol: str):
        """ Find a symbol in the global scope

        Parameters
        ----------
        symbol : str
            lexeme of the symbol to find
       
        Returns
        -------
        Entry
            Entry stored in the symbol table or None in case that symbol is not found
        """
        return self.__global_scope__.sym_lookup(symbol)


    def sym_global_remove(self, symbol: str):
        """ Remove a symbol in the global scope

        Parameters
        ----------
        symbol : str
            lexeme of the symbol to remove
       
         Raises
        ------
        Exception
            If the symbol it is not found
        """
        return self.__global_scope__.sym_remove(symbol)


    def sym_push_scope(self, optimized=False):
        """ Push the current scope in the stack and create a new scope

        Parameters
        ----------
        optimized : bool, optional
           To select if the new scope use a HashMap to store the symbols (default False)
        """
        self.__current_scope__ = SimpleSymTab(optimized=optimized)
        self.__scopes_stack__.append(self.__current_scope__)


    def sym_pop_scope(self):
        """ 
        Pop the current scope in the stack and get the previous scope in the stack
        """
        if len(self.__scopes_stack__) == 1:
            raise Exception('Can\'t remove the global scope')
        self.__scopes_stack__.pop()
        self.__current_scope__ = self.__scopes_stack__[-1]
