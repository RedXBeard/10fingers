import os
from subprocess import Popen, PIPE

from kivy.storage.jsonstore import JsonStore

def run_syscall(cmd):
    """
    run_syscall; handle sys calls this function used as shortcut.
    ::cmd: String, shell command is expected.
    """
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.rstrip().decode()


PATH_SEPERATOR = '/'
if os.path.realpath(__file__).find('\\') != -1:
    PATH_SEPERATOR = '\\'

PROJECT_PATH = PATH_SEPERATOR.join(os.path.realpath(__file__).split(PATH_SEPERATOR)[:-1])
if PATH_SEPERATOR == '/':
    cmd = "echo $HOME"
else:
    cmd = "echo %USERPROFILE%"
out = run_syscall(cmd)
DEF_USER = out.split('%s' % PATH_SEPERATOR)[-1]
REPOFILE = "{0}{1}.kivy-word-hunter{1}jsonfile".format(out, PATH_SEPERATOR)

directory = os.path.dirname(REPOFILE)
if not os.path.exists(directory):
    os.makedirs(directory)
DB = JsonStore(REPOFILE)
if not DB.exists('language'):
    DB.store_put('language', 'TR')
DB.store_sync()

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
        result = check_char(get_char(expected, index), t)
        if not result:
            return False
        index += 1
    return True


def write_text(root, color='#000000'):
    prev = root.original_text[:root.initial_index]
    rest = root.original_text[root.initial_index + 1:]
    root.upcoming_text.text = "[color={2}][u]{0}{3}[/u][/color]{1}".format(
        prev, rest, color, get_char(root.original_text, root.initial_index),
    )


def get_char(text, index):
    try:
        result = text[index]
    except IndexError:
        result = ''
    return result
