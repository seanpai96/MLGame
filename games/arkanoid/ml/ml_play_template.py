"""
The template of the main script of the machine learning process
"""
import random


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        random.seed()
        self.servePosition = random.randint(1, 180)

    last_x = 0
    last_y = 0
    servePosition = 100
    # lowestBlock = (500, 500)
    dropPoint = (-1, -1)

    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            print(scene_info["platform"][0])
            self.servePosition = random.randint(1, 160)
            print(self.servePosition)
            return "RESET"

        if not self.ball_served:
            if abs(scene_info["platform"][0] - self.servePosition) > 10:
                # print(self.servePosition)
                if scene_info["platform"][0] < self.servePosition:
                    command = "MOVE_RIGHT"
                elif scene_info["platform"][0] > self.servePosition:
                    command = "MOVE_LEFT"
            else:
                if random.random() > 0.5:
                    command = "SERVE_TO_RIGHT"
                    self.ball_served = True
                else:
                    command = "SERVE_TO_LEFT"
                    self.ball_served = True

            self.last_x = scene_info["ball"][0]
            self.last_y = scene_info["ball"][1]
            self.dropPoint = (-1, -1)
        else:
            # if scene_info["ball"][0]+2 > scene_info["platform"][0]+20:
            #     command = "MOVE_RIGHT"
            # elif scene_info["ball"][0]+2 < scene_info["platform"][0]+20:
            #     command = "MOVE_LEFT"
            # else:
            #     command = "NONE"
            current_x = scene_info["ball"][0]
            current_y = scene_info["ball"][1]
            # self.lowestBlock = max(scene_info["bricks"], key=self.getY)
            # print(self.lowestBlock)
            # print(current_x, current_y)
            # if current_y > self.lowestBlock[1] and current_y > self.last_y:  # dropping
            if current_y > self.last_y:  # dropping
                # if self.dropPoint == (-1, -1):
                slope = self.getSlope(self.last_x, current_x, self.last_y, current_y)
                print(slope)
                # c = current_y - (slope * current_x)
                self.dropPoint = self.getPoint((current_x, current_y), slope)
                print(self.dropPoint)
                if self.dropPoint[0] + 5 < scene_info["platform"][0] + 20:
                    command = "MOVE_LEFT"
                else:
                    command = "MOVE_RIGHT"
            else:
                self.dropPoint = (-1, -1)
                if scene_info["ball"][0] + 5 > scene_info["platform"][0] + 20:
                    command = "MOVE_RIGHT"
                elif scene_info["ball"][0] + 5 < scene_info["platform"][0] + 20:
                    command = "MOVE_LEFT"
                else:
                    command = "NONE"
            self.last_x = current_x
            self.last_y = current_y
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

    def getSlope(self, x0, x, y0, y):
        return (y-y0)/(x-x0)

    def getY(self, data):
        return data[1]

    def getPoint(self, point, slope):
        print(point, slope)
        if 0 <= ((400-point[1])/slope) + point[0] <= 200:
            return ((400-point[1])/slope) + point[0], 400
        else:
            if slope > 0:  # \
                y = slope*(200-point[0]) + point[1]
                return self.getPoint((200, y), slope*-1)
            else:  # /
                y = slope*(0-point[0]) + point[1]
                return self.getPoint((0, y), slope * -1)

    # def getPoint(self, point, slope, c):
    #     print(point, slope, c)
    #     if 0 <= (point[1]-c)/slope <= 200:
    #         return (point[1]-c)/slope + point[0], 400
    #     else:
    #         y = slope * point[0] + c
    #         c = y - slope * point[0]
    #         return self.getPoint((200, y), slope*-1, c)

    # def getPoint(self, point, slope, c):
    #     print(point, slope, c)
    #     finalPoint = (400 - c) / slope
    #     print(finalPoint)
    #     minusCount = 0
    #     while not 0 <= finalPoint <= 200:
    #         if finalPoint > 200:
    #             finalPoint -= 200
    #             minusCount += 1
    #         else:
    #             finalPoint *= -1
    #         print(finalPoint)
    #
    #     if minusCount % 2 == 1:
    #         return 200 - finalPoint, 400
    #     return finalPoint, 400
