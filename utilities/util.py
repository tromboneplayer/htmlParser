def fix_unprintable(string_parm: str) -> str:
    '''Replace any unprintable characters as needed.'''
    
    return string_parm.replace(chr(8212), "-") #8212 is an emdash, repace with a regular en dash