import gym
from gym import error, spaces, utils
from gym.utils import seeding
# from sense_hat import SenseHat
from sense_emu import SenseHat
from time import sleep
from random import randint


class CarEnv(gym.Env):
   metadata = {'render.modes': ['human']}

   def __init__(self):
      self.sense = SenseHat()
      self.score = 0

      self.car = [1, 7, 2, 7, 3, 7, 2, 6]
      self.pos = 0

      self.oppo = [1, 2, 3]
      self.opos = randint(0, 1)

      self.sense.set_rotation(270)

      self.r = 0
      self.car_distance = randint(9, 15)

      self.action_space  = spaces.Discrete(2)

   def step(self, action):
      self.sense.clear()
      self.draw_border()
      self.draw_car(action);
      self.draw_opponent(self.r);
      self.r += 1
      terminate = False
      reward = 0

      if (self.r == 8 or self.r == 9) and self.opos == self.pos:
         self.sense.show_message("Score " + str(self.score))
         terminate = True

      if (self.r == self.car_distance):
         self.r = 0

         self.car_distance = randint(9, 13)
         self.opos = randint(0, 1)
         self.score += 1
         reward = 1

      return self.sense.get_pixels(), reward, terminate, {}

   def reset(self):
      self.score = 0
      self.speed = 0.20
      self.pos = 0
      self.opos = randint(0, 1)
      self.car_distance = randint(9, 15)
      self.r = 0

   def render(self, mode='human'):
      self.sense.stick.direction_up = self.move_left
      self.sense.stick.direction_down = self.move_right
      lst = self.sense.get_pixels()

      print ([lst[i+1:i+7] for i in range(0,len(lst),8)])

   def close(self):
      raise Exception("Not implemented close")


   def draw_car(self, p):
      car = self.car
      if (p == 0):
         self.sense.set_pixel(car[0], car[1], 0, 127, 255)
         self.sense.set_pixel(car[2], car[3], 0, 127, 255)
         self.sense.set_pixel(car[4], car[5], 0, 127, 255)
         self.sense.set_pixel(car[6], car[7], 0, 255, 255)
      else:
         self.sense.set_pixel(car[0] + 3, car[1], 0, 127, 255)
         self.sense.set_pixel(car[2] + 3, car[3], 0, 127, 255)
         self.sense.set_pixel(car[4] + 3, car[5], 0, 127, 255)
         self.sense.set_pixel(car[6] + 3, car[7], 0, 255, 255)


   def draw_opponent(self, row):
      opos = self.opos
      oppo = self.oppo
      if (opos == 0):
         if row <= 7:
            self.sense.set_pixel(oppo[0], row, 255, 127, 0)
            self.sense.set_pixel(oppo[2], row, 255, 127, 0)
         if row >= 1 and row <= 8:
            self.sense.set_pixel(oppo[1], row - 1, 255, 127, 0)

      else:

         if row <= 7:
            self.sense.set_pixel(oppo[0] + 3, row, 255, 127, 0)
            self.sense.set_pixel(oppo[2] + 3, row, 255, 127, 0)
         if row >= 1 and row <= 8:
            self.sense.set_pixel(oppo[1] + 3, row - 1, 255, 127, 0)


   def draw_border(self):
      color = (150, 255, 100)
      for i in range(8):
         self.sense.set_pixel(0, i, color)
         self.sense.set_pixel(7, i, color)


   def move_left(self):
      self.pos = 1


   def move_right(self):
      self.pos = 0
