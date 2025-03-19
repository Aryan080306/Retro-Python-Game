import simplegui
import random

# Window dimensions
WIDTH = 1920
HEIGHT = 1080

# Scaling factor for responsiveness
scale_x = WIDTH / 1920
scale_y = HEIGHT / 1080

# Image dimensions (scaled)
IMG_WIDTH = int(80 * scale_x)
IMG_HEIGHT = int(120 * scale_y)

# Collision platform properties (scaled)
COLLISION_Y = int(850 * scale_y)  # Vertical position of the platform (line)
COLLISION_X = 0  # Starting x-position of the platform
COLLISION_WIDTH = int(1920 * scale_x)  # Width of the platform

# Red Box Coordinates (scaled)
RED_BOX_TOP_LEFT = (int(37 * scale_x), int(230 * scale_y))
RED_BOX_TOP_RIGHT = (int(37 * scale_x), int(242 * scale_y))
RED_BOX_BOTTOM_LEFT = (int(400 * scale_x), int(230 * scale_y))
RED_BOX_BOTTOM_RIGHT = (int(400 * scale_x), int(242 * scale_y))

# Coin size
coin_size = (int(60 * scale_x), int(60 * scale_y))

# Player class
class Player:
    def __init__(self, image, pos=(int(300 * scale_x), int(HEIGHT - IMG_HEIGHT)), size=(IMG_WIDTH, IMG_HEIGHT)):
        self.image = image
        self.pos = list(pos)  # [x, y] position
        self.size = size
        self.velocity = [0, 0]  # [horizontal, vertical]
        self.gravity = 0.3 * scale_y
        self.jump_speed = -10 * scale_y
        self.is_jumping = False
        self.friction = 0.9
        self.direction = 1  # 1 for right, -1 for left

    def is_within_platform(self):
        return COLLISION_X <= self.pos[0] <= COLLISION_X + COLLISION_WIDTH - self.size[0]

    def is_on_collision_line(self):
        return self.is_within_platform() and self.pos[1] + self.size[1] == COLLISION_Y

    def update(self, keys):
        new_x = self.pos[0] + self.velocity[0]
        new_y = self.pos[1] + self.velocity[1]

        # Horizontal movement
        if keys['A']:
            self.velocity[0] = -6 * scale_x
            self.direction = -1
        elif keys['D']:
            self.velocity[0] = 6 * scale_x
            self.direction = 1
        else:
            self.velocity[0] = 0

        # Apply friction to horizontal velocity
        self.velocity[0] *= self.friction

        # Gravity and jumping logic
        if not self.is_on_collision_line():
            self.velocity[1] += self.gravity
            self.is_jumping = True
        else:
            self.pos[1] = COLLISION_Y - self.size[1]
            self.velocity[1] = 0
            self.is_jumping = False

        if keys['SPACE'] and not self.is_jumping:
            self.velocity[1] = self.jump_speed
            self.is_jumping = True  

        # Prevent falling below platform
        if new_y + self.size[1] > COLLISION_Y and self.is_within_platform():
            self.pos[1] = COLLISION_Y - self.size[1]
            self.velocity[1] = 0
        else:
            self.pos[1] = new_y

        # Update horizontal movement
        self.pos[0] = new_x

        # Prevent player from going out of bounds
        self.pos[0] = max(0, min(WIDTH - self.size[0], self.pos[0]))

    def draw(self, canvas):
        canvas.draw_image(self.image, (self.size[0] / 2, self.size[1] / 2), self.size, self.pos, self.size, self.direction)
        canvas.draw_line((COLLISION_X, COLLISION_Y), (COLLISION_X + COLLISION_WIDTH, COLLISION_Y), 5, 'Red')


# Load images
#First resolution, used when 1920x1080

player_image = simplegui.load_image('https://i.imgur.com/F9tqYuj.jpeg')  # Player
background_image = simplegui.load_image('https://i.imgur.com/irpOJU3.png')  # Background
health_bar = simplegui.load_image('https://i.imgur.com/WaNznUQ.png')
coin_image = simplegui.load_image('https://i.imgur.com/g0wHNrl.png')


#Second resolution, used when 1000x600

#background_image = simplegui.load_image('https://i.imgur.com/Q3mXUK3.png')  # Background
#health_bar = simplegui.load_image('https://i.imgur.com/vaTmjCg.png')



# Create player object
player = Player(player_image, pos=(int(250 * scale_x), int(200 * scale_y)))

# Stats tracking
coin_count = 0
lv_count = 0
exp_count = 0
kill_count = 0

# Coins list
coins = [(random.randint(100, WIDTH - 100), random.randint(int(500 * scale_y), int(800 * scale_y))) for _ in range(15)]

# Key states
keys = {'A': False, 'D': False, 'SPACE': False}

# Key event handlers
def keydown(key):
    if key == simplegui.KEY_MAP['a']:
        keys['A'] = True
    elif key == simplegui.KEY_MAP['d']:
        keys['D'] = True
    elif key == simplegui.KEY_MAP['space']:
        keys['SPACE'] = True

def keyup(key):
    if key == simplegui.KEY_MAP['a']:
        keys['A'] = False
    elif key == simplegui.KEY_MAP['d']:
        keys['D'] = False
    elif key == simplegui.KEY_MAP['space']:
        keys['SPACE'] = False

# Coin collection logic
def check_coin_collision():
    global coin_count, coins, exp_count, lv_count
    player_left = player.pos[0]
    player_right = player.pos[0] + player.size[0]
    player_top = player.pos[1]
    player_bottom = player.pos[1] + player.size[1]
    
    coins_to_remove = []
    
    for coin in coins:
        coin_left = coin[0]
        coin_right = coin[0] + coin_size[0]
        coin_top = coin[1]
        coin_bottom = coin[1] + coin_size[1]
        
        if (player_right > coin_left and player_left < coin_right and 
            player_bottom > coin_top and player_top < coin_bottom):
            coin_count += 1
            gained_exp = random.randint(5, 10)  # EXP increase between 5-10
            exp_count += gained_exp  
            coins_to_remove.append(coin)
    
    # Handle EXP overflow
    while exp_count >= 100:
        lv_count += 1
        exp_count -= 100  # Carry over excess EXP

    # Remove collected coins
    for coin in coins_to_remove:
        coins.remove(coin)

# Draw handler
def draw(canvas):
    global coins, lv_count, exp_count, kill_count

    canvas.draw_image(background_image, (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(health_bar, (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    for coin_pos in coins:
        canvas.draw_image(coin_image, (coin_size[0] / 2, coin_size[1] / 2), coin_size, coin_pos, coin_size)

    check_coin_collision()
    player.update(keys)
    player.draw(canvas)

    canvas.draw_polygon([RED_BOX_TOP_LEFT, RED_BOX_TOP_RIGHT, RED_BOX_BOTTOM_RIGHT, RED_BOX_BOTTOM_LEFT], 3, 'Red', 'Red')

    # Display stats (scaled)
    canvas.draw_text(f"{coin_count}", (int(90* scale_x), int(348 * scale_y)), int(40 * scale_x), 'Yellow')
    canvas.draw_text(f"{lv_count}", (int(325 * scale_x), int(75 * scale_y)), int(56 * scale_x), 'White')
    canvas.draw_text(f"{exp_count}/100", (int(365 * scale_x), int(130 * scale_y)), int(25 * scale_x), 'White')
    canvas.draw_text(f"{kill_count}", (int(90 * scale_x), int(420 * scale_y)), int(40 * scale_x), 'Red')

# Create and start frame
frame = simplegui.create_frame("Game", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.start()
