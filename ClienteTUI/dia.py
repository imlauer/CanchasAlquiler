from picotui.context import Context
from picotui.dialogs import *

with Context():
    d = DTextEntry(25, "Hello World", title="Wazzup?")
    res = d.result()

    d = DMultiEntry(25, 5, "Hello\nWorld".split("\n"),
    title="Comment:")
    res = d.result()

print(res)
