from container import Container, chunk_words
from widget import _Widget, chunk_str, position_cursor
from style import FitType

class Row(Container):

    def render(self, line_num = 1):
        self.actual_width = self.width
        min_height = 0
        x_buffer = 0
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
                        renderable_children.append(f"{position_cursor(self.x + x_buffer, self.y + line_num)}{self.parent_border}{self.get_border_vert_char()}{line}{self.get_border_vert_char()}{self.parent_border}")
                    else:
                        renderable_children.append(f"{position_cursor(self.x + x_buffer, self.y + line_num)}{self.parent_border}{line}{self.parent_border}")
                    #line_num += 1
                    #min_height += 1
            elif isinstance(child, _Widget): # is a widget
                child.x = self.x + x_buffer
                match self.style.fit:
                    case FitType.DEFAULT:
                        child.width = min(child.width, self.width)
                if self.style.border:
                    child.parent_border = self.get_border_vert_char()
                renderable_children.append(child.render(line_num))
                #line_num = max(child.actual_height, line_num)
                #min_height = max(child.actual_height, min_height)
                x_buffer += child.actual_width + child.style.border_weight*2
        
        if self.style.fit == FitType.STATIC_SNUG or self.style.fit == FitType.STATIC:
            remaining_height = self.height - len(self.children)
            if remaining_height > 0:
                for _ in range(remaining_height):
                    if self.style.border:
                        renderable_children.append(f"{position_cursor(self.x + x_buffer, self.y + line_num)}{self.get_border_vert_char()}{' ' * self.actual_width}{self.get_border_vert_char()}")
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
