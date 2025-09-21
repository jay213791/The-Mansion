from ursina import *
from ursina.audio import Audio


def start_instruction(game, cursor):
    cursor.enabled = False
    mouse.visible = False
    dialogue = [
        "Welcome to the Mansion...\n"
        "Legends say it’s haunted \n"
        "by a spirit trapped for decades.\n"
        "No one who enters comes out the same...",
        "Use WASD to move around the mansion.\n"
        "Look around with your mouse to explore.\n"
        "Press F to turn on your flashlight. \n"
        "Some rooms are very dark.\n"
        "Press E to interact with objects \n"
        "or read notes you find.",
        "The ghost has left fragments \n"
        "of its memories scattered here.\n"
        "Find all the memories to set the spirit free...\n"
        "Be careful — \n"
        "it may appear when you least expect it.",
        "The mansion awaits you. \n"
        "Step inside, if you dare...\n"
        "Remember: some secrets are hidden in plain sight."
    ]

    backgrounds = [load_texture(path) for path in [
        'assets/bg1.png',
        'assets/bg2.png',
        'assets/bg4.png',
        'assets/bg5.png',
    ]]
    current_index = 0

    bg = Entity(
        model='quad',
        scale=(16, 9),
        texture=backgrounds[0]
    )

    story_text = Text(
        text='',
        origin=(0, 0),
        y=.2,
        scale=3,
        font='assets/GideonRoman-Regular.ttf',
        color=color.white
    )

    continue_text = Text(
        text='Press SPACE to continue',
        origin=(0, 0),
        y=-.3,
        scale=1.2,
        color=color.yellow,
        enabled=False,
    )

    def fade_in(entity, duration=0.1):
        entity.color = color.clear
        entity.animate_color(color.white, duration=duration)

    def type_writer(text, delay=3):
        story_text.text = ''
        continue_text.enabled = False
        for char in text:
            story_text.text += char
            if char.strip():
                Audio('assets/typewriter.wav', autoplay=True)
            for _ in range(delay):
                yield
        continue_text.enabled = True

    text_animation = type_writer(dialogue[current_index])

    def instruction_update():
        nonlocal text_animation
        try:
            next(text_animation)
        except StopIteration:
            pass

    bg.update = instruction_update


    def instruction_input(key):
        nonlocal current_index, text_animation
        if key == 'space' and continue_text.enabled:
            current_index += 1
            if current_index < len(dialogue):
                bg.texture = backgrounds[current_index]
                fade_in(bg, duration=0.5)
                text_animation = type_writer(dialogue[current_index])
            else:
                story_text.enabled = False
                continue_text.enabled = False
                bg.enabled = False
                game.start()

    bg.input = instruction_input
