from __future__ import annotations
import math
import os
from enum import Enum

# TODO sort the component rendering order by some sort of z-index.

def chunk_str(string:str, chunk_size:int):
    ret_list:list[str] = []
    for i in range(0, len(string), chunk_size):
        chunk = string[i:min(i+chunk_size, len(string))]
        ret_list.append(f"{chunk}{' ' * (chunk_size - len(chunk))}")
    return ret_list

def position_cursor(x:int, y:int):
        return f"\033[{y};{x}H"



class _Widget:
    def __init__(self) -> None:
        t_size = os.get_terminal_size()
        self.children = []
        self.x = 0
        self.y = 0
        self.width = t_size.columns
        self.actual_width = self.width
        self.height = 0
        self.actual_height = 0
        self.parent_border = ""

    def render(self, line_num = 1):
        min_height = 0
        renderable_children:list[str] = []
        for child in self.children:
            if isinstance(child, str):
                for line in chunk_str(child, self.actual_width):
                    renderable_children.append(position_cursor(self.x, self.y + line_num) + line)
                    line_num += 1
                    min_height += 1
            elif isinstance(child, _Widget): # is a widget
                renderable_children.append(child.render(line_num))
                line_num += child.actual_height
                min_height += child.actual_height
        
        self.actual_height = min_height
        render_str = ""
        for child in renderable_children:
            render_str += child
        
        return render_str

    def __str__(self) -> str:
        return self.render()

    def append_child(self, child):
        self.children.append(child)

    
    
if __name__ == "__main__":
    t_size = os.get_terminal_size()
    print("\033c")
    wid = _Widget()
    wid.children = [
        "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
        "hewwo"
    ]
    print(wid)

    while True:
        pass