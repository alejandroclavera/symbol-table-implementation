class Entry:
    '''
    Entry of a SYMTAB
    '''
    symbol: str
    type: str
    size:int
    params:dict

    def __init__(self, symbol:str, type:int, size:int, offset:int, params={}): 
        self.symbol = symbol
        self.type = type
        self.size = size
        self.offset = offset
        self.params = params

    def __eq__(self, other):
        return \
            self.symbol == other.symbol \
            and self.type == other.type \
            and self.size == other.size \
            and self.offset == other.offset \
            and self.params == other.params

    def __str__(self):
        return '{' + 'symbol:{0}, type:{1}, offset:{2}'.format(self.symbol, self.type, self.offset) + '}'

    def __repr__(self):
        return '{' + 'symbol:{0}, type:{1}, offset:{2}'.format(self.symbol, self.type, self.offset) + '}'


class ListStructure:
    __entries__:list

    def __init__(self):
        self.__entries__ = []

    
    def __contains__(self, symbol:str):
        for entry in self.__entries__:
            if symbol == entry.symbol:
                return True
        return False


    def append(self, entry:Entry):
        self.__entries__.append(entry)
    

    def get(self, symbol:str):
        for entry in self.__entries__:
            if symbol == entry.symbol:
                return entry
        return None


    def remove(self, symbol:str):
        removed = False
        for entry in self.__entries__:
            if symbol == entry.symbol:
                self.__entries__.remove(entry)
                removed = True
            break
        # if symbol isn't removed, the symbol is not found and raise a exception
        if not removed:
            raise Exception('symbol \'' + symbol + '\' not found' )


class HashStructure:
    __entries__:dict

    def __init__(self):
        self.__entries__ = {}


    def __contains__(self, symbol:str):
        return symbol in self.__entries__


    def append(self, entry:Entry):
        self.__entries__[entry.symbol] = entry
    

    def get(self, symbol:str):
       return self.__entries__.get(symbol, None)


    def remove(self, symbol:str):
        if symbol not in self.__entries__:
            raise Exception('symbol \'' + symbol + '\' not found' )
        del self.__entries__[symbol]