
s = [0, 1, 5, 6, 7, 8, 9, 2, 3, 4]
t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def reorder_list(source, target):
    """Reorder a list to match target by moving a sequence at a time.

    Written for QtAbstractItemModel.moveRows.
    """
    i = 0
    while i < len(source):

        if source[i] == target[i]:
            i += 1
            continue
        else:
            i0 = i
            j0 = source.index(target[i0])
            j = j0 + 1
            while j < len(source):
                if source[j] == target[j - j0 + i0]:
                    j += 1
                    continue
                else:
                    break
            move_elements(source, i0, j0, j - j0)
            i += j - j0


def move_elements(target, index_to, index_from, length):
    """Move a sub sequence in a list"""

    sublist = [target.pop(index_from) for _ in range(length)]

    for _ in range(length):
        target.insert(index_to, sublist.pop())

