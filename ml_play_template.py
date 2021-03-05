"""
The template of the main script of the machine learning process
"""


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_RIGHT"
        else:
            if scene_info["ball"][0] > scene_info["platform"][0]:
                command = "MOVE_RIGHT"
            elif scene_info["ball"][0] < scene_info["platform"][0]:
                command = "MOVE_LEFT"
            else:
                command = "NONE"

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
