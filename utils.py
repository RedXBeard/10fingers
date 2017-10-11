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


def write_text(root, color='#000000'):
    prev = root.original_text[:root.initial_index]
    rest = root.original_text[root.initial_index + 1:]
    root.upcoming_text.text = "{0}[color={2}][u]{3}[/u][/color]{1}".format(
        prev, rest, color, root.original_text[root.initial_index],
    )
