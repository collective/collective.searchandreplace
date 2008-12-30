class Proxy:
    def __init__( self, subject ):
        self.__subject = subject
    def __getattr__( self, name ):
        return getattr( self.__subject, name )      

