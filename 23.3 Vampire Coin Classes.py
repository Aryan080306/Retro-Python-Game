import simplegui
import random

class Game:
    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.scale_x = self.WIDTH / 1920
        self.scale_y = self.HEIGHT / 1080
        self.coin_size = (int(60 * self.scale_x), int(60 * self.scale_y))  
        self.screen_index = 0
        self.load_assets() 
        self.COLLISION_Y = int(850 * self.scale_y)  # Vertical position of the platform (line)
        self.COLLISION_X = 0  # Starting x-position of the platform
        self.COLLISION_WIDTH = int(1920 * self.scale_x)  # Width of the platform
        self.init_objects()        
        self.keys = {'A': False, 'D': False, 'SPACE': False}
        self.frame = simplegui.create_frame("Game", self.WIDTH, self.HEIGHT)
        self.set_handlers()
        self.frame.start()
        
           # Collision platform properties (scaled)
       

    def load_assets(self):
        self.player_image = simplegui.load_image('https://i.imgur.com/E6gHGcW.png')
        self.coin_image = simplegui.load_image('https://i.imgur.com/g0wHNrl.png')
        self.enemy_image = simplegui.load_image('https://i.imgur.com/E6gHGcW.png')
        self.background_image = simplegui.load_image('https://i.imgur.com/irpOJU3.png')
        self.health_bar = simplegui.load_image('https://i.imgur.com/PQ7GEsh.png')
        
        #self.background_image = simplegui.load_image('https://i.imgur.com/Q3mXUK3.png')
        #self.health_bar = simplegui.load_image('https://i.imgur.com/vaTmjCg.png')
        
        image_paths = [
            "https://i.imgur.com/U1D8297.png",
            "https://i.imgur.com/y7HzWBx.png",
            "https://i.imgur.com/kTj9Goq.png",
            "https://i.imgur.com/fo18wkF.png",
        ]
        self.images = [simplegui.load_image(path) for path in image_paths]
        self.welcome_messages = ["Welcome", "Click to continue..."]

    def init_objects(self):
        self.player = Player(self, self.player_image)
        self.counts = Counts()
        self.coins = [Coin(self, self.coin_image) for _ in range(15)]
        self.interaction = Interaction(self.player, self.coins, self.counts, self)
        self.enemy = Enemy(self, self.enemy_image)

    def set_handlers(self):
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_keyup_handler(self.keyup)
        self.frame.set_mouseclick_handler(self.advance_screen)

    def advance_screen(self, _):
        if self.screen_index < 5:
            self.screen_index += 1

    def keydown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.keys['A'] = True
        elif key == simplegui.KEY_MAP['d']:
            self.keys['D'] = True
        elif key == simplegui.KEY_MAP['space']:
            self.keys['SPACE'] = True

    def keyup(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.keys['A'] = False
        elif key == simplegui.KEY_MAP['d']:
            self.keys['D'] = False
        elif key == simplegui.KEY_MAP['space']:
            self.keys['SPACE'] = False

    def draw(self, canvas):
        # Draw welcome screen
        if self.screen_index == 0:
            sizes = [int(self.WIDTH * 0.12), int(self.WIDTH * 0.06)]
            y = int(self.HEIGHT * 0.4)
            for i, msg in enumerate(self.welcome_messages):
                canvas.draw_text(msg, [self.WIDTH * 0.25, y], sizes[i], "Red")
                y += sizes[i]
        
        # Draw other screens (images)
        elif self.screen_index < 5:
            image = self.images[self.screen_index - 1]
            canvas.draw_image(image, (image.get_width() / 2, image.get_height() / 2), (image.get_width(), image.get_height()), (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
        
        # Game screen
        else:
            canvas.draw_image(self.background_image, (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT), (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
            canvas.draw_image(self.health_bar, (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT), (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))

            self.interaction.check_coin_collisions()
            self.player.update()
            self.player.draw(canvas)
            self.enemy.update(self.player.pos)
            self.enemy.draw(canvas)
            
            for coin in self.coins:
                coin.draw(canvas)
                

            # New coordinates for the red box
            RED_BOX_TOP_LEFT = (int(37 * self.scale_x), int(230 * self.scale_y))
            RED_BOX_TOP_RIGHT = (int(37 * self.scale_x), int(242 * self.scale_y))
            RED_BOX_BOTTOM_LEFT = (int(400 * self.scale_x), int(230 * self.scale_y))
            RED_BOX_BOTTOM_RIGHT = (int(400 * self.scale_x), int(242 * self.scale_y))

            # Draw red box
            canvas.draw_polygon(
                [RED_BOX_TOP_LEFT, RED_BOX_TOP_RIGHT, RED_BOX_BOTTOM_RIGHT, RED_BOX_BOTTOM_LEFT], 
                3, 'Red', 'Red'
            )

            # Draw counts (coin, level, EXP, kills)
            canvas.draw_text(f"{self.counts.coin_count}", (int(90 * self.scale_x), int(348 * self.scale_y)), int(40 * self.scale_x), 'Yellow')
            canvas.draw_text(f"{self.counts.lv_count}", (int(325 * self.scale_x), int(75 * self.scale_y)), int(56 * self.scale_x), 'White')
            canvas.draw_text(f"{self.counts.exp_count}/100", (int(365 * self.scale_x), int(130 * self.scale_y)), int(25 * self.scale_x), 'White')
            canvas.draw_text(f"{self.counts.kill_count}", (int(90 * self.scale_x), int(420 * self.scale_y)), int(40 * self.scale_x), 'Red')

class Player:
    def __init__(self, game, image):
        self.game = game
        self.image = image
        self.size = (128, 128)
        self.pos = [300 * game.scale_x, game.COLLISION_Y - self.size[1]]  # Initial position, adjusted below
        self.velocity = [0, 0]
        self.gravity = 0.4 * game.scale_y
        self.jump_speed = -10 * game.scale_y
        self.is_jumping = False
        self.friction = 0.9

    def update(self):
        # Horizontal movement
        if self.game.keys['A']:
            self.velocity[0] = -6 * self.game.scale_x
        elif self.game.keys['D']:
            self.velocity[0] = 6 * self.game.scale_x
        else:
            self.velocity[0] *= self.friction

        # Gravity application
        if self.pos[1] + self.size[1] < self.game.COLLISION_Y:
            self.velocity[1] += self.gravity
        else:
            # When player hits the ground (platform), stop downward velocity
            self.velocity[1] = 0
            self.is_jumping = False
            self.pos[1] = self.game.COLLISION_Y - self.size[1]  # Correct position for bottom of the player

        # Jumping logic (upward velocity)
        if self.game.keys['SPACE'] and not self.is_jumping:
            self.velocity[1] = self.jump_speed
            self.is_jumping = True

        # Update the player's position based on velocity
        self.pos[0] = max(0, min(self.game.WIDTH - self.size[0], self.pos[0] + self.velocity[0]))
        self.pos[1] += self.velocity[1]

    def draw(self, canvas):
        canvas.draw_image(self.image, (int(64*self.game.scale_x), int(64*self.game.scale_y)), self.size, self.pos, self.size)

class Coin:
    def __init__(self, game, image):
        self.game = game
        self.image = image
        self.pos = (random.randint(100, game.WIDTH - 100), random.randint(int(500 * game.scale_y), int(825 * game.scale_y)))
        self.size = game.coin_size

    def draw(self, canvas):
        canvas.draw_image(self.image, (self.size[0] / 2, self.size[1] / 2), self.size, self.pos, self.size)

    def check_collision(self, player):
        player_left, player_right = player.pos[0], player.pos[0] + player.size[0]
        player_top, player_bottom = player.pos[1], player.pos[1] + player.size[1]
      
        coin_left, coin_right = self.pos[0], self.pos[0] + self.size[0]
        coin_top, coin_bottom = self.pos[1], self.pos[1] + self.size[1]
        
        return (player_right > coin_left and player_left < coin_right and 
                player_bottom > coin_top and player_top < coin_bottom)
class Counts:
    def __init__(self):
        self.coin_count = 0
        self.lv_count = 0
        self.exp_count = 0
        self.kill_count = 0

    def gain_exp(self, exp):
        self.exp_count += exp
        while self.exp_count >= 100:
            self.lv_count += 1
            self.exp_count -= 100

class Interaction:
    def __init__(self, player, coins, counts, game):
        self.player = player
        self.coins = coins
        self.counts = counts

    def check_coin_collisions(self):
        collected = [coin for coin in self.coins if coin.check_collision(self.player)]
        for coin in collected:
            self.counts.coin_count += 1
            self.counts.gain_exp(random.randint(5, 10))
            self.coins.remove(coin)
    def check_platform_collision(self):
        # Check if the player is below the platform and adjust accordingly
        if (self.player.pos[1] + self.player.size[1] > self.game.COLLISION_Y and  # Player is falling below the platform
            self.game.COLLISION_X < self.player.pos[0] + self.player.size[0] and  # Player is within the horizontal bounds of the platform
            self.game.COLLISION_X + self.game.COLLISION_WIDTH > self.player.pos[0]):  # Player is within the horizontal bounds of the platform
            
            # Stop player from falling below the platform
            self.player.pos[1] = self.game.COLLISION_Y - self.player.size[1]  # Place player on top of the platform
            self.player.velocity[1] = 0  # Stop downward velocity
            self.player.is_jumping = False  # Ensure player is not considered jumping

    def update(self):
        # Check for both coin collisions and platform collision
        self.check_coin_collisions()
        self.check_platform_collision()
class Enemy:
    def __init__(self, game, image):
        self.game = game
        self.image = image
        # Set enemy to spawn above the collision platform
        self.pos = [600, self.game.COLLISION_Y- 55]  # 150 pixels above the collision platform
        self.size = (128, 128)
        self.speed = 3


    def update(self, player_pos):
        if self.pos[0] < player_pos[0]:
            self.pos[0] += self.speed
        elif self.pos[0] > player_pos[0]:
            self.pos[0] -= self.speed

    def draw(self, canvas):
        canvas.draw_image(self.image, (int(64*self.game.scale_x), int(64*self.game.scale_y)), self.size, self.pos, self.size)

if __name__ == "__main__":
    Game()
