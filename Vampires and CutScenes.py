import simplegui  

# screen index: 0 = Welcome, 1-4 = Cutscene images, 5 = Game Screen
screen_index = 0  

# Frame dimensions
WIDTH = 1000  
HEIGHT = 600

# load images for cutscenes and game screen
image_paths = [
    "https://i.imgur.com/U1D8297.png",  # Walking scene
    "https://i.imgur.com/y7HzWBx.png",  # Bus crash
    "https://i.imgur.com/kTj9Goq.png",  # Quote
    "https://i.imgur.com/fo18wkF.png",  # Catacombs door
]
images = [simplegui.load_image(path) for path in image_paths]

# background, sprite, enemy images
sprite_image = simplegui.load_image('https://i.imgur.com/F9tqYuj.jpeg')  # white box
background_image = simplegui.load_image('https://i.imgur.com/tI6lb6Q.png')
health_bar = simplegui.load_image('https://i.imgur.com/Lzf05MU.png')
enemy_image = simplegui.load_image('https://i.imgur.com/ybc8oYp.png')  # Enemy image

# text for welcome screen
welcome_messages = ["Welcome", "Click to continue..."]

# key states
keys = {'A': False, 'D': False, 'SPACE': False}

# class for main sprite 
class Sprite:
    def __init__(self, image, pos=(300, HEIGHT - 80), size=(40, 80)):
        self.image = image
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.gravity = 0.3
        self.jump_speed = -10
        self.is_jumping = False  # jump
        self.friction = 0.9
        self.direction = 1
        
        
    def update(self):
        new_x = self.pos[0] + self.velocity[0]
        new_y = self.pos[1] + self.velocity[1]

        if keys['A']:
            self.velocity[0] = -6
            self.direction = -1
        elif keys['D']:
            self.velocity[0] = 6
            self.direction = 1
        else:
            self.velocity[0] = 0

        self.velocity[0] *= self.friction
        self.velocity[1] += self.gravity
        
        if keys['SPACE'] and not self.is_jumping:
            self.velocity[1] = self.jump_speed
            self.is_jumping = True

        if new_y + self.size[1] > 480:
            self.pos[1] = 480 - self.size[1]
            self.velocity[1] = 0
            self.is_jumping = False
        else:
            self.pos[1] = new_y

        self.pos[0] = max(0, min(WIDTH - self.size[0], new_x))

    def draw(self, canvas):
        canvas.draw_image(self.image, (self.size[0] / 2, self.size[1] / 2), self.size, self.pos, self.size, self.direction)
        canvas.draw_line((0, 480), (WIDTH, 480), 5, 'Red')

        
# class for vampire        
class Enemy:
    def __init__(self, image, pos=(600, HEIGHT - 80), size=(128, 128)):
        self.image = image
        self.pos = list(pos)
        self.size = size
        self.speed = 2
    
    # movement of vampire
    def update(self, player_pos):
        if self.pos[0] < player_pos[0]:
            self.pos[0] += self.speed
        elif self.pos[0] > player_pos[0]:
            self.pos[0] -= self.speed
        
        if self.pos[1] < player_pos[1]:
            self.pos[1] += self.speed
        elif self.pos[1] > player_pos[1]:
            self.pos[1] -= self.speed
    
    # draws vampire
    def draw(self, canvas):
        canvas.draw_image(self.image, (self.size[0] / 2, self.size[1] / 2), self.size, self.pos, self.size)

sprite = Sprite(sprite_image, pos=(250, 200))
enemy = Enemy(enemy_image, pos=(600, 480))

def advance_screen(_):
    global screen_index
    if screen_index < 5:
        screen_index += 1

# Movement of main sprite        
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


def draw(canvas):
    if screen_index == 0:
        sizes = [int(WIDTH * 0.12), int(WIDTH * 0.06)]
        line_spacing = [int(WIDTH * 0.12), int(WIDTH * 0.1)]
        x_position = int(WIDTH * 0.25)
        y_start = int(HEIGHT * 0.4)
        y = y_start
        for i, msg in enumerate(welcome_messages):
            canvas.draw_text(msg, [x_position, y], sizes[i], "Red")
            y += line_spacing[i]
    elif screen_index < 5:
        image = images[screen_index - 1]
        canvas.draw_image(image, (image.get_width() / 2, image.get_height() / 2), (image.get_width(), image.get_height()), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    else:
        # draws background
        canvas.draw_image(background_image, (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT), (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        # draws health bar
        canvas.draw_image(health_bar, (WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT), ((WIDTH / 2) - 250, (HEIGHT / 2) - 150), (WIDTH / 2, HEIGHT / 2))
        # draws movement for sprite and enemies
        sprite.update()
        enemy.update(sprite.pos)
        sprite.draw(canvas)
        enemy.draw(canvas)

frame = simplegui.create_frame("Game", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(advance_screen)
frame.start()
