from ursina.prefabs.first_person_controller import FirstPersonController
from first_floor.ground import ground
from ursina import Audio
import player.flashlight as flashlight

class Game:
    def __init__(self):
        self.player = None
        self.flashlight_sound = Audio('assets/flashlight.wav', autoplay=False)

    def start(self):
        ground()
        self.player = FirstPersonController(y=2, origin_y=-.5)
        self.player.speed = 8
        flashlight.setup_flashlight()

    def input(self, key):
        if key == 'f' and self.player:  # only works after game starts
            if flashlight.flashlight_model and flashlight.flashlight_overlay:
                flashlight.flashlight_overlay.enabled = not flashlight.flashlight_overlay.enabled
                flashlight.flashlight_model.visible = flashlight.flashlight_overlay.enabled
                self.flashlight_sound.play()
