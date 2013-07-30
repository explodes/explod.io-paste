

def left_outer_join(left_seq, right_seq, searcher=lambda left, right: bool(right), default=None):
    return left_outer_join_factory(left_seq, right_seq, searcher=searcher,
        default_factory=lambda left: default)

def left_outer_join_factory(left_seq, right_seq, searcher=lambda left, right: bool(right), default_factory=lambda left:None):
    """ Zip items in `left` with items in `right` matched by `func`. Right hand
    side contains `default_factory(left)` if there is no real match.
    example:
        >>> left = 'abcd'
        >>> right = 'BDE'
        >>> searcher = lambda l, r: l.upper() == r.upper()
        >>> result = left_outer_join(left, right, searcher, 'X')
        >>> print result
        [('a', 'X'), ('b', 'B'), ('c', 'X'), ('d', 'D')]


        >>> left = 'abcd'
        >>> right = 'BDE'
        >>> searcher = lambda l, r: l.upper() == r.upper()
        >>> factory = lambda l: l * 5
        >>> result = left_outer_join_factory(left, right, searcher, factory)
        >>> print result
        [('a', 'aaaaa'), ('b', 'B'), ('c', 'ccccc'), ('d', 'D')]
    """
    paired = []
    for left_item in left_seq:
        found = False
        for right_item in right_seq:
            if searcher(left_item, right_item):
                paired.append((left_item, right_item))
                found = True
                break
        if not found:
            paired.append((left_item, default_factory(left_item)))
    return paired

def no_duplicates(sequence, key=lambda x:x):
    history = set()
    for item in sequence:
        dup_key = key(item)
        if dup_key not in history:
            history.add(dup_key)
            yield item
