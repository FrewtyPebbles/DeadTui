from dataclasses import dataclass
from style import BorderStyle, FitType
from widget import _Widget, chunk_str, position_cursor

def chunk_words(string:str, chunk_size:int):
    raw_words = string.split(' ')
    words:list[str] = []
    for word in raw_words:
        if len(word) <= chunk_size:
            words.append(word)
        else:
            words.extend(chunk_str(word, chunk_size))

    ret_list = []
    chunk_buffer = []
    for word in words:
        chunk_len = sum([len(chunk) for chunk in chunk_buffer])
        if chunk_len + len(word) + 1 < chunk_size:
            chunk_buffer.append(word)
        else:
            chunked_str = ' '.join(chunk_buffer)
            ret_list.append(f"{chunked_str}{' ' * (chunk_size - len(chunked_str))}")
            chunk_buffer = [word]
    
    chunked_str = ' '.join(chunk_buffer)
    ret_list.append(f"{chunked_str}{' ' * (chunk_size - len(chunked_str))}")
    chunk_buffer = [word]

    return ret_list

@dataclass
class ContainerStyle:
    # BORDER
    border:bool = False
    border_weight:int = 1
    border_style:BorderStyle = BorderStyle.THIN_SOLID
    border_corner_rounded:bool = False
    border_connect:tuple[bool,bool,bool,bool] = (False, False, False, False)

    # POSITIONING
    fit:FitType = FitType.DEFAULT
    
    # TEXT
    split_words:bool = True
    
    

class Container(_Widget):
    def __init__(self, children:list[_Widget | str] | None = None, height:int | None = None, width:int | None = None, style:ContainerStyle | None = None) -> None:
        super().__init__()
        self.children = children if children != None else []
        if height:
            self.height = height
        if width:
            self.width = width
            self.actual_width = self.width
        self.style = style if style else ContainerStyle()
    
    def get_connections(self,                          #0,  1,  2,  3,  4,  5,  6,  7,  8
    con_set:tuple[str,str,str,str,str,str,str,str,] = ('┏','┓','┗','┛','┣','┫','┳','┻','╋')):
        con_up, con_right, con_down, con_left = self.style.border_connect
        tl_key, tr_key, bl_key, br_key = (('tl',),('tr',),('bl',),('br',))
        cons = {
            # '┏','┓','┗','┛'
            ('tl',) : con_set[0],
            ('tr',) : con_set[1],
            ('bl',) : con_set[2],
            ('br',) : con_set[3],
            # '┣','┫'
            ('tl','u') : con_set[4],
            ('tr','u') : con_set[5],
            ('bl','d') : con_set[4],
            ('br','d') : con_set[5],
            # '┳','┻'
            ('tl','l') : con_set[6],
            ('bl','l') : con_set[7],
            ('tr','r') : con_set[6],
            ('br','r') : con_set[7],
            # '╋'
            ('tl','u','l') : con_set[8],
            ('bl','d','l') : con_set[8],
            ('tr','u','r') : con_set[8],
            ('br','d','r') : con_set[8],
        }
        if con_up:
            tl_key += ('u',)
            tr_key += ('u',)
        if con_down:
            bl_key += ('d',)
            br_key += ('d',)
        if con_right:
            tr_key += ('r',)
            br_key += ('r',)
        if con_left:
            tl_key += ('l',)
            bl_key += ('l',)
        return cons[tl_key], cons[tr_key], cons[bl_key], cons[br_key]

    def render_border_horizontal(self, line_num:int, top:bool):
        ret_str = ""
        for _ in range(self.style.border_weight):
            match self.style.border_style:
                case BorderStyle.SOLID:
                    tl, tr, bl, br = self.get_connections(('┏','┓','┗','┛','┣','┫','┳','┻','╋'))
                    if top:
                        ret_str += position_cursor(self.x, self.y + line_num) + f"{self.parent_border}{tl}{'━'*(self.actual_width)}{tr}{self.parent_border}"
                    else:
                        ret_str += position_cursor(self.x, self.y + line_num) + f"{self.parent_border}{bl}{'━'*(self.actual_width)}{br}{self.parent_border}"
                case BorderStyle.THIN_SOLID:
                    tl, tr, bl, br = self.get_connections(('┌','┐','└','┘','├','┤','┬','┴','┼'))
                    if top:
                        ret_str += position_cursor(self.x, self.y + line_num) + f"{self.parent_border}{tl}{'─'*(self.actual_width)}{tr}{self.parent_border}"
                    else:
                        ret_str += position_cursor(self.x, self.y + line_num) + f"{self.parent_border}{bl}{'─'*(self.actual_width)}{br}{self.parent_border}"
                    
        return ret_str

    def get_border_vert_char(self):
        ret_str = ""
        for _ in range(self.style.border_weight):
            match self.style.border_style:
                case BorderStyle.SOLID:
                    ret_str += '┃'
                case BorderStyle.THIN_SOLID:
                    ret_str += '│'
                    
        return ret_str


    def render(self, line_num = 1):
        self.actual_width = self.width
        min_height = 0
        renderable_children:list[str] = []
        self.actual_width -= len(self.parent_border) * 2
        if self.style.border:
            self.actual_width -= self.style.border_weight * 2
            self.actual_height -= self.style.border_weight * 2
            renderable_children.append(self.render_border_horizontal(line_num, True))
            line_num += self.style.border_weight
            min_height += self.style.border_weight
            if self.style.border_connect[0]:
                line_num -= self.style.border_weight


        
        for child in self.children:
            if isinstance(child, str):
                lines = []
                if self.style.split_words:
                    lines = chunk_words(child, self.actual_width)
                else:
                    lines = chunk_str(child, self.actual_width)
                for line in lines:
                    if self.style.border:
                        renderable_children.append(f"{position_cursor(self.x, self.y + line_num)}{self.parent_border}{self.get_border_vert_char()}{line}{self.get_border_vert_char()}{self.parent_border}")
                    else:
                        renderable_children.append(f"{position_cursor(self.x, self.y + line_num)}{self.parent_border}{line}{self.parent_border}")
                    line_num += 1
                    min_height += 1
            elif isinstance(child, _Widget): # is a widget
                match self.style.fit:
                    case FitType.DEFAULT:
                        child.width = min(child.width, self.width)
                if self.style.border:
                    child.parent_border = self.get_border_vert_char()
                renderable_children.append(child.render(line_num))
                line_num += child.actual_height
                min_height += child.actual_height
        
        if self.style.fit == FitType.STATIC_SNUG or self.style.fit == FitType.STATIC:
            remaining_height = self.height - len(self.children)
            if remaining_height > 0:
                for _ in range(remaining_height):
                    if self.style.border:
                        renderable_children.append(f"{position_cursor(self.x, self.y + line_num)}{self.get_border_vert_char()}{' ' * self.actual_width}{self.get_border_vert_char()}")
                    else:
                        renderable_children.append(position_cursor(self.x, self.y + line_num) + {' ' * self.actual_width})
                    line_num += 1
                    min_height += 1

        if self.style.border:
            renderable_children.append(self.render_border_horizontal(line_num, False))
            line_num += self.style.border_weight
            min_height += self.style.border_weight

        self.actual_height = min_height
        
        render_str = ""
        for child in renderable_children:
            render_str += child
        return render_str