# put this code in code skulptor: https://py3.codeskulptor.org/
import simplegui
import random
import time

class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 600
        
        self.coin_size = (33,33)  
        self.screen_index = 0
        self.load_assets() 
        
        self.COLLISION_Y = 550
        self.COLLISION_X = 0 
        self.COLLISION_WIDTH = 1000
        
        self.vampires_timer = None
        self.keys = {'A': False, 'D': False, 'W': False, 'SPACE': False}
        
        self.x = 100
        self.y = 200
        self.dx = 5
        self.damage = 50
        self.boss_health = 300
        
        self.init_objects()  
        
        self.frame = simplegui.create_frame("Game", self.WIDTH, self.HEIGHT)
        self.set_handlers()
        self.frame.start()
        self.spawn_vamps()
        self.show_level_transition = False
        self.current_level = None
        self.boss_defeated = False
        self.congrats_time = 0
        
        self.music = Music(self)
    
    def spawn_vamps(self):
        for _ in range(2):   
            vamp_type = random.randint(1, 4)
            if vamp_type == 1:
                Vampires.HealthVamp.append(Vampires(90, 0.5, 65, self.health_vamp_image))
            elif vamp_type == 2:
                Vampires.DamageVamp.append(Vampires(70, 1, 90, self.damage_vamp_image))
            elif vamp_type == 3:
                Vampires.SpeedVamp.append(Vampires(70, 2.5, 60, self.speed_vamp_image))
            else:
                Vampires.RegularVamp.append(Vampires(70, 1.5, 70, self.vampire_image))
    
    def spawn_coin(self):
        if len(self.coins) < 7:  
            new_coin = Coin(self, self.coin_image)
            self.coins.append(new_coin)  
                    
    def all_vampires_dead(self):
        return (len(Vampires.HealthVamp) == 0 and len(Vampires.DamageVamp) == 0 and 
                len(Vampires.SpeedVamp) == 0 and len(Vampires.RegularVamp) == 0)     
        
    def load_assets(self):
        self.player_right = simplegui.load_image('https://i.imgur.com/7HbYBpY.png')
        self.player_left = simplegui.load_image('https://i.imgur.com/rakNiAk.png')
        self.coin_image = simplegui.load_image('https://i.imgur.com/tAEdRrb.png')
        
        self.vampire_image = simplegui.load_image('https://i.imgur.com/JSR4Aoy.png')
        self.health_vamp_image = simplegui.load_image('https://i.imgur.com/4HuOkaS.png')
        self.damage_vamp_image = simplegui.load_image('https://i.imgur.com/myMfEbg.png')
        self.speed_vamp_image = simplegui.load_image('https://i.imgur.com/SKFvEbq.png')
        
        self.leveltwo = simplegui.load_image("https://i.imgur.com/8zHodzH.png")
        self.boss_image = simplegui.load_image("https://i.imgur.com/lK80793.png")
        
        self.background_image = simplegui.load_image('https://i.imgur.com/Q3mXUK3.png')
        self.health_bar = simplegui.load_image('https://i.imgur.com/vaTmjCg.png')
        
        image_paths = [
            "https://i.imgur.com/cJ9hLzg.png",
            "https://i.imgur.com/U1D8297.png",
            "https://i.imgur.com/y7HzWBx.png",
            "https://i.imgur.com/kTj9Goq.png",
            "https://i.imgur.com/fo18wkF.png",
        ]
        self.images = [simplegui.load_image(path) for path in image_paths]
      
    def keydown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.keys['A'] = True
        elif key == simplegui.KEY_MAP['d']:
            self.keys['D'] = True
        elif key == simplegui.KEY_MAP['space']:
            self.keys['SPACE'] = True
        elif key == simplegui.KEY_MAP['w']:
            self.projectile.shoot(self)

    def keyup(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.keys['A'] = False
        elif key == simplegui.KEY_MAP['d']:
            self.keys['D'] = False
        elif key == simplegui.KEY_MAP['space']:
            self.keys['SPACE'] = False   

    def init_objects(self):
        self.player = Player(self, self.player_right, self.player_left)
        self.boss = Boss(self, self.boss_image)
        self.counts = Counts()
        self.coins = []
        self.vampires = Vampires(self,90, 90 ,self.vampire_image)
        self.interaction = Interaction(self.player, self.coins, self.counts, self, self.vampires)
        self.projectile = Projectile(self, self.x ,self.y,self.dx, self.damage)
        self.collision = Collision(self.player, self.vampires, self.projectile, self.counts)
        self.settings = Settings(self, self.boss)

    def set_handlers(self):
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.player.keydown)
        self.frame.set_keyup_handler(self.player.keyup)
        self.frame.set_mouseclick_handler(self.advance_screen)
        self.frame.set_mouseclick_handler(self.mouse_click_dispatcher)
        
        self.coin_timer = simplegui.create_timer(200, self.spawn_coin)
        self.coin_timer.start()
        
        self.vampires_timer = simplegui.create_timer(3000, self.spawn_vamps)
        self.vampires_timer.start()
        
    def mouse_click_dispatcher(self, position):
        if self.screen_index < 6:
            self.advance_screen(position)
        else:
            self.mouse_handler(position)    
            
        if self.show_level_transition and not self.current_level:
            self.show_level_transition = False 
            self.current_level = LevelTwo(self.counts, self.coins, self.settings, self.player, self)  
            self.frame.set_keydown_handler(self.current_level.keydown)
            self.frame.set_keyup_handler(self.current_level.keyup)
        
    def mouse_handler(self, pos):
        self.settings.handle_click(pos)     

    def advance_screen(self, _):
        if self.screen_index < 6:
            self.screen_index += 1
            
    def reset_game(self):
        """Resets the game and returns to the welcome screen."""
        self.player.lives = 3  # Reset lives
        self.counts.coin_count = 0  # Reset coin count
        self.counts.kill_count = 0  # Reset kill count
        self.current_level = None  # Reset level
        self.screen_index = 0  # Go to the welcome screen        
            
    

    def draw(self, canvas):
        self.music.update()
        if self.screen_index == 0:
            welcome_screen = self.images[0]
            canvas.draw_image(welcome_screen, (welcome_screen.get_width() / 2, welcome_screen.get_height() / 2), 
                             (welcome_screen.get_width(), welcome_screen.get_height()), 
                             (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
            self.vampires_timer.stop()
            self.coin_timer.stop()
       
        elif self.screen_index < 6:
            image = self.images[self.screen_index - 1]
            canvas.draw_image(image, (image.get_width() / 2, image.get_height() / 2), 
                            (image.get_width(), image.get_height()), 
                            (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
            self.vampires_timer.stop()
            self.coin_timer.stop()
        
        elif self.all_vampires_dead() and self.counts.coin_count >= 15 and self.counts.kill_count >=10 and not self.current_level:
            self.show_level_transition = True
            self.vampires_timer.stop()
            self.coin_timer.stop()
            canvas.draw_image(self.leveltwo, 
                          (self.leveltwo.get_width() / 2, self.leveltwo.get_height() / 2), 
                          (self.leveltwo.get_width(), self.leveltwo.get_height()), 
                          (self.WIDTH / 2, self.HEIGHT / 2), 
                          (self.WIDTH, self.HEIGHT))
        
        elif self.current_level:
            self.current_level.draw(canvas)
            
        else:
            canvas.draw_image(self.background_image, (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT), 
                              (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
            canvas.draw_image(self.health_bar, (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT), 
                              (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
            self.vampires_timer.start()
            self.coin_timer.start()
            self.interaction.check_coin_collisions()
            
            self.collision.check_collision()
            
            if not self.settings.is_paused:
                self.player.update()
                
            self.player.draw(canvas)
            self.settings.draw(canvas)            
            
            if not self.settings.is_paused:
                for vamp in Vampires.HealthVamp:
                    vamp.update(self.player.pos)
                    vamp.draw(canvas)
                for vamp in Vampires.DamageVamp:
                    vamp.update(self.player.pos)
                    vamp.draw(canvas)
                for vamp in Vampires.SpeedVamp:
                    vamp.update(self.player.pos)
                    vamp.draw(canvas)
                for vamp in Vampires.RegularVamp:
                    vamp.update(self.player.pos)
                    vamp.draw(canvas) 
            
            for coin in self.coins:
                coin.draw(canvas)
           
            canvas.draw_text(f"{self.counts.coin_count}", (50,192), 20, 'Yellow')
            canvas.draw_text(f"{self.counts.lv_count}", (185,41), 28, 'White')
            canvas.draw_text(f"{self.counts.exp_count}/100", (205,71), 15, 'White')
            canvas.draw_text(f"{self.counts.kill_count}", (50,235), 20, 'Red')

class LevelTwo:
    def __init__(self, counts, coins, settings, player, game):
        self.counts = counts
        self.coins = coins
        self.settings = settings
        self.player = player
        self.game = game
        self.boss = Boss(self.game, self.game.boss_image)
        self.boss_health = 300  
        self.congrats_time = 0
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.image = simplegui.load_image('https://i.imgur.com/GX3cack.png')
        self.game.vampires_timer.stop()
        self.game.coin_timer.stop()
        
    def keydown(self, key):
        self.player.keydown(key)

    def keyup(self, key):
        self.player.keyup(key) 

    def draw(self, canvas):
        canvas.draw_image(self.game.background_image, (self.game.WIDTH / 2, self.game.HEIGHT / 2), 
                         (self.game.WIDTH, self.game.HEIGHT), 
                         (self.game.WIDTH / 2, self.game.HEIGHT / 2), 
                         (self.game.WIDTH, self.game.HEIGHT))
        canvas.draw_image(self.game.health_bar, (self.game.WIDTH / 2, self.game.HEIGHT / 2), 
                         (self.game.WIDTH, self.game.HEIGHT), 
                         (self.game.WIDTH / 2, self.game.HEIGHT / 2), 
                         (self.game.WIDTH, self.game.HEIGHT))
        
        if not self.settings.is_paused:
            self.player.update()
            self.player.draw(canvas)
            self.settings.draw(canvas)
        
        if self.boss_health > 0:
            self.boss.update_frame()
            self.boss.draw(canvas)  
            self.boss.start(canvas)
            
            # Boss health bar
            boss_health_width = 200 * (self.boss_health / 300)
            canvas.draw_line((self.game.WIDTH // 2 - 100, 100), 
                           (self.game.WIDTH // 2 - 100 + boss_health_width, 100), 
                           10, 'Red')
            
            # Player projectiles hitting boss
            for shot in self.player.projectile.shots[:]:
                if (self.boss.x - 128 < shot.x < self.boss.x + 128 and
                    self.boss.y - 128 < shot.y < self.boss.y + 128):
                    self.boss_health -= self.player.damage
                    self.player.projectile.shots.remove(shot)
                    #if self.boss_health <= 0:
                    #    self.congrats_time = time.time()
        
        # Boss attacks hitting player - estimating hitbox
        for attack in self.boss.boss_attacks[:]:
            attack.move()

            attack_left = attack.x - attack.image_width//2
            attack_right = attack.x + attack.image_width//2
            attack_top = attack.y - attack.image_height//2
            attack_bottom = attack.y + attack.image_height//2

            player_left = self.player.pos[0]
            player_right = player_left + self.player.size[0]
            player_top = self.player.pos[1]
            player_bottom = player_top + self.player.size[1]

            # Check for collision
            if (player_right > attack_left and player_left < attack_right and 
                player_bottom > attack_top and player_top < attack_bottom):

                # Damage player (30 damage in phase 2, 20 in phase 1)
                damage = 30 if self.boss_health < 150 else 20
                self.player.take_damage(damage)

                self.boss.boss_attacks.remove(attack)
                self.player.hurt_time = time.time()

                # Return to level 1 if player dies
                if self.player.health <= 0:
                    self.game.reset_game()
                    
                   # self.game.current_level = None
                   # self.player.reset_position(200, 200 - self.player.size[1])
                   # self.player.health = 100
                    break
        
        # Remove attacks that go off-screen
        for attack in self.boss.boss_attacks[:]:
            if attack.x < -100:
                self.boss.boss_attacks.remove(attack)

        # Congrats msg
        if self.boss_health <= 0 :
            # shows a congrats PNG then 
            
            # fake image
            #image = simplegui.load_image("https://i.imgur.com/fo18wkF.png")
            
            canvas.draw_image(self.image, (self.image.get_width() / 2, self.image.get_height() / 2), (self.image.get_width(), self.image.get_height()), (self.WIDTH / 2, self.HEIGHT / 2), (self.WIDTH, self.HEIGHT))
            
            
            # click on it to call reset game
            
            
            # this just goes back to the welcome screen
            #self.game.reset_game()
            
            
            
        
        
        
        # Stats
        canvas.draw_text(f"{self.counts.coin_count}", (50,192), 20, 'Yellow')
        canvas.draw_text(f"{self.counts.lv_count}", (185,41), 28, 'White')
        canvas.draw_text(f"{self.counts.exp_count}/100", (205,71), 15, 'White')
        canvas.draw_text(f"{self.counts.kill_count}", (50,235), 20, 'Red')

class Player:
    def __init__(self, game, player_right, player_left):
        self.game = game
        self.size = (128, 128)
        self.pos = [300, 300 - self.size[1]] 
        self.velocity = [0, 0]
        self.gravity = 0.3 
        self.jump_speed = -10 
        self.is_jumping = False
        self.friction = 0.92
        self.player_right = player_right
        self.player_left = player_left
        
        self.hurt_image = simplegui.load_image('https://i.imgur.com/5PlCpwM.png')
        self.hurt_time = 0
        self.hurt_duration = 0.15
        
        self.lives = 3
        self.health = 100
        self.damage = 40
        
        self.projectile = Projectile(self.game, self.pos[0], self.pos[1], 10, self.damage)
        
    def take_damage(self, amount):
        self.health -= amount
        self.hurt_time = time.time()  

    def reset_position(self, x, y):
        self.pos = [x, y]
        self.velocity = [0, 0]
    
    def update(self):
        if self.game.keys['A']:
            self.velocity[0] = -5 
        elif self.game.keys['D']:
            self.velocity[0] = 5
        else:
            self.velocity[0] *= self.friction

        if self.pos[1] + self.size[1] < self.game.COLLISION_Y:
            self.velocity[1] += self.gravity
        else:
            self.velocity[1] = 0
            self.is_jumping = False
            self.pos[1] = self.game.COLLISION_Y - self.size[1]

        if self.game.keys['W'] and not self.is_jumping:
            self.velocity[1] = self.jump_speed
            self.is_jumping = True

        self.pos[0] = max(0, min(self.game.WIDTH - self.size[0], self.pos[0] + self.velocity[0]))
        self.pos[1] += self.velocity[1]

    def draw(self, canvas):
        if self.game.keys['A']:
            canvas.draw_image(self.player_left, (self.size[0] // 2, self.size[1] // 2), self.size, self.pos, self.size)
        elif self.game.keys['D']:
            canvas.draw_image(self.player_right, (self.size[0] // 2, self.size[1] // 2), self.size, self.pos, self.size)
        else:
            canvas.draw_image(self.player_right, (self.size[0] // 2, self.size[1] // 2), self.size, self.pos, self.size)
        
        self.projectile.update()
        self.projectile.draw(canvas)
        
        if self.health <= 0:
            self.health = 100
            if self.lives > 0:
                self.lives -= 1
                self.reset_position(200, 200 - self.size[1])
            
        if self.lives == 2:
            self.draw_circle(canvas, 200, 106, 16) 
        elif self.lives == 1:
            self.draw_circle(canvas, 200, 106, 16) 
            self.draw_circle(canvas, 168, 106, 16)
        elif self.lives == 0:
            self.game.reset_game()
            print("Return To Welcome Screen")
        
        if self.hurt_image and time.time() - self.hurt_time < self.hurt_duration:
            canvas.draw_image(self.hurt_image, (self.game.WIDTH / 2, self.game.HEIGHT / 2), 
                             (self.game.WIDTH, self.game.HEIGHT), 
                             (self.game.WIDTH / 2, self.game.HEIGHT / 2), 
                             (self.game.WIDTH, self.game.HEIGHT))
      
        max_health_bar_width = 220
        health_bar_width = int(max_health_bar_width * (self.health / 100))
        
        RED_BOX_TOP_LEFT = (22, 129)
        RED_BOX_TOP_RIGHT = (22 + health_bar_width, 129)
        RED_BOX_BOTTOM_RIGHT = (22 + health_bar_width, 133)
        RED_BOX_BOTTOM_LEFT = (22, 133)

        canvas.draw_polygon(
            [RED_BOX_TOP_LEFT, RED_BOX_TOP_RIGHT, RED_BOX_BOTTOM_RIGHT, RED_BOX_BOTTOM_LEFT], 
            3, 'Red', 'Red'
        )
   
    def draw_circle(self, canvas, x, y, radius):
        canvas.draw_circle((x, y), radius, 2, 'Black', 'Black')  
        
    def keydown(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.game.keys['A'] = True
            self.is_moving_left = True
            
        elif key == simplegui.KEY_MAP['d']:
            self.game.keys['D'] = True
            self.is_moving_right = True
            
        elif key == simplegui.KEY_MAP['w']:
            self.game.keys['W'] = True
            
        elif key == simplegui.KEY_MAP['k']:
            self.projectile.shoot(self)

    def keyup(self, key):
        if key == simplegui.KEY_MAP['a']:
            self.game.keys['A'] = False
            self.is_moving_left = False
            
        elif key == simplegui.KEY_MAP['d']:
            self.game.keys['D'] = False
            self.is_moving_right = False
            
        elif key == simplegui.KEY_MAP['w']:
            self.game.keys['W'] = False

class Boss:
    FRAME_COUNT = 4
    FRAME_WIDTH = 256
    FRAME_HEIGHT = 256

    def __init__(self, game, boss_image):
        self.game = game
        self.boss_image = boss_image
        self.timer = simplegui.create_timer(200, self.update_frame)
        
        self.current_frame = 0
        self.frame_counter = 0 
        self.frame_delay = 70
                
        self.x = 860
        self.y = 380
        
        self.boss_attacks = []
        self.shoot_timer = simplegui.create_timer(1000, self.shoot)
       
        
    def stop(self,canvas):
          self.timer.stop()
          self.shoot_timer.stop() 
          return
    
    def update_frame(self):
        if self.frame_counter % self.frame_delay == 0:
            self.current_frame = (self.current_frame + 1) % self.FRAME_COUNT
        self.frame_counter += 1 
        
        if self.game.boss_health <= 0:
            self.stop()
            
            return
        
    def draw(self, canvas):
        source_x = self.current_frame * self.FRAME_WIDTH + self.FRAME_WIDTH / 2
        source_y = self.FRAME_HEIGHT / 2 
        
        canvas.draw_image(
            self.boss_image,
            (source_x, source_y),
            (self.FRAME_WIDTH, self.FRAME_HEIGHT),
            (self.x, self.y),
            (self.FRAME_WIDTH, self.FRAME_HEIGHT) 
        )
        
        for attack in self.boss_attacks:
            attack.draw(canvas)
    
    def shoot(self):
        attack_speed = 6
        attack_x = self.x - 110 
        attack_y = self.y + 60 
        
        if self.game.boss_health < 150:  # Phase 2
            attack_speed = 8
            # Triple attack in phase 2
            self.boss_attacks.append(Boss_Attack(attack_x, attack_y - 40, attack_speed))
            self.boss_attacks.append(Boss_Attack(attack_x, attack_y, attack_speed))
            self.boss_attacks.append(Boss_Attack(attack_x, attack_y + 40, attack_speed))
        else:
            # Single attack in phase 1
            self.boss_attacks.append(Boss_Attack(attack_x, attack_y, attack_speed))
    def start(self, canvas):
        self.timer.start()
        self.shoot_timer.start()   
        
class Boss_Attack:
    def __init__(self, x, y, speed=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.attack_image = simplegui.load_image("https://i.imgur.com/cmdZc6M.png")
        self.image_width = 64
        self.image_height = 64

    def move(self):
        self.x -= self.speed
    
    def draw(self, canvas):
        canvas.draw_image(
            self.attack_image, 
            (self.image_width / 2, self.image_height / 2),
            (self.image_width, self.image_height),
            (self.x, self.y),
            (self.image_width, self.image_height)
        )        
        
class Coin:
    def __init__(self, game, image):
        self.game = game
        self.image = image
        self.pos = (random.randint(100, game.WIDTH - 100), random.randint(int(300), int(450)))
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
    def __init__(self, player, coins, counts, game, vampires):
        self.player = player
        self.coins = coins
        self.counts = counts
        self.game = game
        self.vampires = vampires

    def check_coin_collisions(self):
        collected = [coin for coin in self.coins if coin.check_collision(self.player)]
        for coin in collected:
            self.counts.coin_count += 1
            self.counts.gain_exp(random.randint(5, 10))
            if 0 < self.player.health != 100:
                self.player.health += 2
            self.coins.remove(coin)
                      
    def check_platform_collision(self):
        if (self.player.pos[1] + self.player.size[1] > self.game.COLLISION_Y and
            self.game.COLLISION_X < self.player.pos[0] + self.player.size[0] and
            self.game.COLLISION_X + self.game.COLLISION_WIDTH > self.player.pos[0]):
            
            self.player.pos[1] = self.game.COLLISION_Y - self.player.size[1]
            self.player.velocity[1] = 0
            self.player.is_jumping = False
            
    def update(self):
        self.check_coin_collisions()
        self.check_platform_collision()
        self.check_vamp_collision()
   
class Vampires:
    HealthVamp = []
    DamageVamp = []
    SpeedVamp = []
    RegularVamp = []
   
    def __init__(self, damage, speed, health, vampire_image):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.vampire_image = vampire_image
        self.pos = [random.randint(400, 600), 432]
        
        self.width = 96
        self.height = 96

    def update(self, player_pos):
        if self.pos[0] < player_pos[0]:
            self.pos[0] += self.speed
        elif self.pos[0] > player_pos[0]:
            self.pos[0] -= self.speed
            
    def draw(self, canvas):
        canvas.draw_image(self.vampire_image,
                      (self.width // 2, self.height // 2),
                      (self.width, self.height),
                      self.pos,
                      (self.width, self.height))   

class Collision:
    def __init__(self, Player, Vampires, projectile, counts):
        self.Player = Player
        self.Vampires = Vampires
        self.projectile = projectile
        self.vamp_player_collision = False
        self.vamp_projectile_collision = False
        self.player_alive = True
        self.counts = counts
        self.last_damage_time = 0

    def check_collision(self):
        current_time = time.time()
        for vamp in Vampires.HealthVamp + Vampires.DamageVamp + Vampires.SpeedVamp + Vampires.RegularVamp:
            x1, y1 = vamp.pos  
            width1, height1 = vamp.width, vamp.height  
            x2, y2 = self.Player.pos[0], self.Player.pos[1]  
            width2, height2 = self.Player.size[0], self.Player.size[1]  
            
            if (x1 < x2 + width2 and x1 + width1 > x2 and
                y1 < y2 + height2 and y1 + height1 > y2):  
                if current_time - self.last_damage_time >= 1:
                    self.vamp_player_collision = True
                    self.Player.take_damage(17)
                    self.last_damage_time = current_time
            else:
                self.vamp_player_collision = False
        return self.vamp_player_collision
         
    def check_projectile_vamp_collision(self, projectile):
        for vamp in Vampires.HealthVamp + Vampires.DamageVamp + Vampires.SpeedVamp + Vampires.RegularVamp:
            x1, y1 = vamp.pos
            width1, height1 = vamp.width, vamp.height

            for shotter in projectile.shots[:]:
                x2, y2 = shotter.x, shotter.y
                width2, height2 = shotter.width, shotter.height

                if x2 + width2 > x1 and x2 < x1 + width1 and y2 + height2 > y1 and y2 < y1 + height1:
                    self.vamp_projectile_collision = True
                    vamp.health -= self.Player.damage
                    if vamp.health <= 0:
                        if vamp in Vampires.HealthVamp:
                            Vampires.HealthVamp.remove(vamp)
                        elif vamp in Vampires.DamageVamp:
                            Vampires.DamageVamp.remove(vamp)
                        elif vamp in Vampires.SpeedVamp:
                            Vampires.SpeedVamp.remove(vamp)
                        elif vamp in Vampires.RegularVamp:
                            Vampires.RegularVamp.remove(vamp)
                        self.counts.kill_count += 1
                    projectile.shots.remove(shotter)
                    return True 
        return False

    def fight_vamp(self, projectile):        
        if self.vamp_projectile_collision:
            print(f"Collision detected! Vampire has {self.Vampires.health} hp left")
            if self.Vampires in Vampires.HealthVamp:
                self.Vampires.health -= self.Player.damage
                if self.Vampires.health <= 0:
                    Vampires.HealthVamp.remove(self.Vampires)
                    self.counts.kill_count += 1 
            elif self.Vampires in Vampires.DamageVamp:
                self.Vampires.health -= self.Player.damage
                if self.Vampires.health <= 0:
                    Vampires.DamageVamp.remove(self.Vampires)
                    self.counts.kill_count += 1 
            elif self.Vampires in Vampires.SpeedVamp:
                self.Vampires.health -= self.Player.damage
                if self.Vampires.health <= 0:
                    Vampires.SpeedVamp.remove(self.Vampires)
                    self.counts.kill_count += 1 
            elif self.Vampires in Vampires.RegularVamp:
                self.Vampires.health -= self.Player.damage
                if self.Vampires.health <= 0:
                    Vampires.RegularVamp.remove(self.Vampires)
                    self.counts.kill_count += 1 
                   
            for shotter in projectile.shots:
                if self.vamp_projectile_collision:  
                    projectile.shots.remove(shotter)
                    break
                   
class Projectile:
    shots = []

    def __init__(self, game, x, y, dx, damage):
        self.game = game
        self.x = x
        self.y = y
        self.damage = damage
        self.image = simplegui.load_image('https://i.imgur.com/2N2ZiUq.png')
        self.width = int(self.image.get_width() * 0.8)
        self.height = int(self.image.get_height() * 0.8)
        self.dx = dx 
        
    def shoot(self, player):
        shot_dx = 0
       
        if player.game.keys['A']:
            shot_dx = -10
        elif player.game.keys['D']:
            shot_dx = 10
        else:
            shot_dx = 10

        shot = Projectile(self.game, player.pos[0], player.pos[1], shot_dx, 50)
        self.shots.append(shot)
       
    def update(self):
        for shot in self.shots[:]:
            shot.x += shot.dx

    def draw(self, canvas):
        for shot in self.shots:
            canvas.draw_image(shot.image,
                              (shot.width // 2, shot.height // 2),
                              (shot.width, shot.height),
                              (shot.x+50, shot.y),
                              (shot.width, shot.height))
        for shot in self.shots[:]:
            shot.x += shot.dx
            if shot.x < 0 or shot.x > self.game.WIDTH:
                self.shots.remove(shot)
                print("shot removed")
            else:
                for vampire in Vampires.HealthVamp + Vampires.DamageVamp + Vampires.SpeedVamp + Vampires.RegularVamp:
                    collision = Collision(self.game.player, vampire, self, self.game.counts)
                    if collision.check_projectile_vamp_collision(self):
                        collision.fight_vamp(self)  
                                
class Settings:
    def __init__(self, game, boss):
        self.game = game
        self.is_paused = False        
        self.button_size = (50, 50)
        self.button_pos = (game.WIDTH - 60, 10)
        
        self.menu_size = (300, 200)
        self.menu_pos = ((game.WIDTH - self.menu_size[0]) // 2, (game.HEIGHT - self.menu_size[1]) // 2)
        
        self.close_button_size = (30, 30)
        self.close_button_pos = (self.menu_pos[0] + self.menu_size[0] - 40, self.menu_pos[1] + 10)
        
        self.boss = boss

    def draw(self, canvas):
        canvas.draw_polygon([
            self.button_pos,
            (self.button_pos[0] + self.button_size[0], self.button_pos[1]),
            (self.button_pos[0] + self.button_size[0], self.button_pos[1] + self.button_size[1]),
            (self.button_pos[0], self.button_pos[1] + self.button_size[1])
        ], 2, 'White', 'Gray')
        canvas.draw_text("O", (self.button_pos[0] + 10, self.button_pos[1] + 35), 30, 'White')
        
        if self.is_paused:
            canvas.draw_polygon([
                self.menu_pos,
                (self.menu_pos[0] + self.menu_size[0], self.menu_pos[1]),
                (self.menu_pos[0] + self.menu_size[0], self.menu_pos[1] + self.menu_size[1]),
                (self.menu_pos[0], self.menu_pos[1] + self.menu_size[1])
            ], 2, 'White', 'Black')
            
            canvas.draw_polygon([
                self.close_button_pos,
                (self.close_button_pos[0] + self.close_button_size[0], self.close_button_pos[1]),
                (self.close_button_pos[0] + self.close_button_size[0], self.close_button_pos[1] + self.close_button_size[1]),
                (self.close_button_pos[0], self.close_button_pos[1] + self.close_button_size[1])
            ], 2, 'White', 'Red')
            canvas.draw_text("X", (self.close_button_pos[0] + 7, self.close_button_pos[1] + 25), 25, 'White')

    def handle_click(self, pos):
        if not self.is_paused:
            if (self.button_pos[0] <= pos[0] <= self.button_pos[0] + self.button_size[0] and
                self.button_pos[1] <= pos[1] <= self.button_pos[1] + self.button_size[1]):
                self.game.vampires_timer.stop()
                self.game.coin_timer.stop()
                if hasattr(self.game, 'boss'):
                    self.boss.timer.stop()
                    self.boss.shoot_timer.stop()
                self.is_paused = True
                return True
        else:
            if (self.close_button_pos[0] <= pos[0] <= self.close_button_pos[0] + self.close_button_size[0] and
                self.close_button_pos[1] <= pos[1] <= self.close_button_pos[1] + self.close_button_size[1]):
                self.is_paused = False
                self.game.vampires_timer.start()
                self.game.coin_timer.start()
                if hasattr(self.game, 'boss'):
                    self.boss.timer.start()
                    self.boss.shoot_timer.start()
                return False        
                      
class Music:
    def __init__(self, game):
        self.game = game
        self.welcome_music = simplegui.load_sound("https://ia801307.us.archive.org/25/items/welcome_screen_music.mp3/welcome_screen_music.mp3")
        self.game_music = simplegui.load_sound("https://ia800708.us.archive.org/8/items/game_music_202503.mp3/game_music.mp3")
        self.current_music = None

    def play_welcome_music(self):
        if self.current_music != self.welcome_music: 
            self.stop_music()
            self.welcome_music.play()
            self.current_music = self.welcome_music

    def play_game_music(self):
        if self.current_music != self.game_music:
            self.stop_music()  
            self.game_music.play()
            self.current_music = self.game_music

    def stop_music(self):
        if self.current_music:
            self.current_music.pause()

    def update(self):
        if 0 <= self.game.screen_index < 6:
            self.play_welcome_music()
        elif self.game.screen_index == 6:
            self.play_game_music()  
        elif self.game.screen_index != 0 and self.game.screen_index != 6:
            self.stop_music()
            
if __name__ == "__main__":
    Game()