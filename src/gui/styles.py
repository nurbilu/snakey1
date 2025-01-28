KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<GameWindow>:
    orientation: 'vertical'
    
    MDTopAppBar:
        id: toolbar
        title: "Snake Game"
        elevation: 10
        pos_hint: {"top": 1}
        md_bg_color: get_color_from_hex("#1B1B1B")
        specific_text_color: get_color_from_hex("#FFFFFF")

    SnakeGame:
        id: game
        canvas.before:
            Color:
                rgba: get_color_from_hex("#004400")
            Rectangle:
                pos: self.pos
                size: self.size

<GameOverLabel@Label>:
    color: 1, 1, 1, 1
    font_size: '40sp'
    bold: True
    halign: 'center'

<InstructionLabel@Label>:
    color: 1, 1, 1, 1
    font_size: '24sp'
    halign: 'center'
''' 