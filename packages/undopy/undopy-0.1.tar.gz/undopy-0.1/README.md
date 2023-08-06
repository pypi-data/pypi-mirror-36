# UndoPy

UndoPy is a library providing persistent Undo/Redo for two python data structures namely list and dict. 

## Implementation

This method is implemented using principles of inverse computations

### Undo and Redo Example

    >>> from UndoPy import UndoLog, undo_dict, undo_list
    >>> t = UndoLog()
    >>> d = dict_undo({1: "VU", 2: "UvA"})
    >>> l = list_undo([1, 2, 3])
    >>> t.adder(d)
    >>> t.adder(l)
    >>> l.append(1)
    >>> d[3] = "CWI"
    >>> l
    [1, 2, 3, 1]
    >>> d
    {1: 'VU', 2: 'UvA', 3: 'CWI'}
    >>> t.undo()
    >>> d
    {1: 'VU', 2: 'UvA'}
    >>> t.undo()
    >>> l
    [1, 2, 3]
    >>> t.redo()
    >>> t.redo()
    >>> l
    [1, 2, 3, 1]
    >>> d
    {1: 'VU', 2: 'UvA', 3: 'CWI'}
    >>> t.start_group("foo")
    True
    >>> d[42] = "student"
    >>> del d[3]
    >>> t.end_group("foo")
    >>> d
    {1: 'VU', 2: 'UvA', 42: 'student'}
    >>> t.undo()
    >>> d
    {1: 'VU', 2: 'UvA', 3: 'CWI'}

