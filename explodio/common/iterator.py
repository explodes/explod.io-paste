

def pair_left(left_seq, right_seq, searcher=lambda left, right: bool(right), default=None, match_once=False):
    """
    Zip items in `left_seq` with items in `right_seq` matched by `searcher`.
    Right hand side contains `default` if there is no real match.
    example:
        >>> left = 'abcd'
        >>> right = 'BDE'
        >>> searcher = lambda l, r: l.upper() == r.upper()
        >>> result = pair_left(left, right, searcher, 'X')
        >>> print result
        [('a', 'X'), ('b', 'B'), ('c', 'X'), ('d', 'D')]
    :param left_seq: Left-hand-side sequence
    :param right_seq: Right-hand-side sequence
    :param searcher: bool func(left, right) indicating a match or not
    :param default: default value when no match was found
    :param match_once: match right-item with up to one left-item
    :return: zip(left_seq, matching_right_seq)
    :rtype : list
    """
    return pair_left_factory(left_seq, right_seq, searcher=searcher,
        default_factory=lambda left: default, match_once=match_once)

def pair_left_factory(left_seq, right_seq, searcher=lambda left, right: bool(right), default_factory=lambda left:None, match_once=False):
    """
    Zip items in `left_seq` with items in `right_seq` matched by `searcher`.
    Right hand side contains `default_factory(left)` if there is no real match.
    example:
        >>> left = 'abcd'
        >>> right = 'BDE'
        >>> searcher = lambda l, r: l.upper() == r.upper()
        >>> factory = lambda l: l * 5
        >>> result = pair_left_factory(left, right, searcher, factory)
        >>> print result
        [('a', 'aaaaa'), ('b', 'B'), ('c', 'ccccc'), ('d', 'D')]
    :param left_seq: Left-hand-side sequence
    :param right_seq: Right-hand-side sequence
    :param searcher: bool func(left, right) indicating a match or not
    :param default_factory: object func(left) returning a default value when
        no match was found
    :param match_once: match right-item with up to one left-item
    :return: zip(left_seq, matching_right_seq)
    :rtype : list
    """
    if match_once:
        right_seq = list(right_seq)
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
        elif match_once:
            print 'match_once', right_item
            right_seq.remove(right_item)
    return paired

def no_duplicates(sequence, key=lambda x:x):
    """
    Iterate over a sequence, skipping duplicates as indicated by key
    :param sequence: Sequence to iterate over
    :param key: obj func(item) returning key to test duplicity for
    :return: generator of sequence's objects
    """
    history = set()
    for item in sequence:
        dup_key = key(item)
        if dup_key not in history:
            history.add(dup_key)
            yield item
