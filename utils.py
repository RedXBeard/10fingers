MAPPER = dict(
    Ğ=['Ğ', 'G'],
    ğ=['ğ', 'g'],
    Ç=['Ç', 'C'],
    ç=['ç', 'c'],
    İ=['İ', 'I'],
    ı=['ı', 'i'],
    Ü=['Ü', 'U'],
    ü=['ü', 'u'],
    Ş=['Ş', 'S'],
    ş=['ş', 's'],
    Ö=['Ö', 'O'],
    ö=['ö', 'o'],
)


def find_parent(cur_class, target_class):
    """find wanted widget from selected or current one"""
    req_class = cur_class
    target_class_name = str(target_class().__class__).split('.')[1].replace("'>", "")
    while True:
        cls = str(req_class.__class__).split('.')[1].replace("'>", "")
        if cls == target_class_name:
            break
        elif cls == 'core':
            req_class = None
            break

        req_class = req_class.parent
    return req_class


def check_char(expected, pressed):
    expected = MAPPER.get(expected) or expected
    if pressed in expected:
        return True
    return False


def check_wordish(expected, typed):
    index = 0
    expected = expected[::-1].zfill(len(typed))[::-1]
    for t in typed:
        result = check_char(expected[index] or '', t)
        if not result:
            return False
        index += 1
    return True


def write_text(root, color='#000000'):
    prev = root.original_text[:root.initial_index]
    rest = root.original_text[root.initial_index + 1:]
    root.upcoming_text.text = "[color={2}][u]{0}{3}[/u][/color]{1}".format(
        prev, rest, color, root.original_text[root.initial_index],
    )

