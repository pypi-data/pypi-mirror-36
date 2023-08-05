
from urwid import Pile, MainLoop, Filler, Divider, Frame, Text

from ..utils import PALETTE
from ..uweird.decorators import Border
from ..uweird.tabs import Root


class App(MainLoop):

    def __init__(self, log, title, msgbar, body, tab_list, session):
        self.root = Root(log, Border(Frame(Filler(body, valign='top'),
                                           header=Pile([Text(title), Divider()]),
                                           footer=Pile([Divider(), msgbar]))),
                         tab_list, session=session)
        self.root.discover()
        super().__init__(self.root, palette=PALETTE)
