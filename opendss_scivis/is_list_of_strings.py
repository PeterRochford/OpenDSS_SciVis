def is_list_of_strings(lst):
    '''
    Check if list contains only strings.

    Input:
    lst : list that may be all strings

    Returns:
      true if all strings
      false if not all strings

    Author: Peter A. Rochford
            Xator Corporation
            www.xatorcorp.com
    
    Created on Apr 22, 2022
    '''
    
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False
