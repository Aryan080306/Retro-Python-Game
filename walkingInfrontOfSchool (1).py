import math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

class Spritesheet:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.sprite_sheet = simplegui.load_image("spritesheet.png")  # will put a thing here when ready
        self.image_loaded = False
        self.sprite_sheet_width = 0
        self.sprite_sheet_height = 0
        self.current_frame = 0
        self.frame_width = 0
        self.frame_height = 0
        self.position = Vector(100, 250)  # Start position of the sprite
        self.target_position = 130 # Target position where the sprite will stop

    def draw(self, canvas):
        # Check if the image is loaded
        if not self.image_loaded:
            self.sprite_sheet_width = self.sprite_sheet.get_width()
            self.sprite_sheet_height = self.sprite_sheet.get_height()
            if self.sprite_sheet_width > 0 and self.sprite_sheet_height > 0:
                self.image_loaded = True
                self.update_frame_dimensions()
            else:
                return  # Image not yet loaded, skip drawing

        # Calculate the position of the current frame
        x_offset = (self.current_frame % self.columns) * self.frame_width
        y_offset = (self.current_frame // self.columns) * self.frame_height
        
        # Draw the current frame on the canvas at the updated position
        canvas.draw_image(self.sprite_sheet, 
                          (x_offset + self.frame_width // 2, y_offset + self.frame_height // 2), 
                          (self.frame_width, self.frame_height), 
                          (self.position.x, self.position.y),  # Move sprite based on position
                          (self.frame_width, self.frame_height))

    def next_frame(self):
        #Move to the next frame, looping back to the first frame when needed.
        self.current_frame = (self.current_frame + 1) % (self.rows * self.columns)

    def update_frame_dimensions(self):
        #Calculate the dimensions of each frame.
        self.frame_width = self.sprite_sheet_width // self.columns
        self.frame_height = self.sprite_sheet_height // self.rows

    def move(self):
        #Move the sprite horizontally to the right until it reaches the target."""
        if self.position.x < self.target_position:  # Move until target is reached
            self.position.x += 5  # Adjust this value for faster/slower movement
        else:
            # Once the target position is reached, stop moving
            self.position.x = self.target_position

class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        #Increments the value of time by 1."""
        self.time += 1

    def transition(self, frame_duration):
        #Checks if it's time to transition to the next frame."""
        if self.time >= frame_duration:
            self.time = 0  # Reset the time after the transition
            return True  # It's time to move to the next frame
        return False  # Not yet time to move to the next frame

# Main Code
frame = simplegui.create_frame("Sprite Animation", 500, 500)
spritesheet = Spritesheet(2, 3)  # 2x3 sprite sheet
clock = Clock()  # Create a Clock instance

frame.set_draw_handler(spritesheet.draw)

# Define the frame duration (e.g., each frame lasts for 10 ticks)
frame_duration = 1

# Timer to move to the next frame every tick (frame duration)
def frame_timer_handler():
    clock.tick()  # Increment the clock time by 1 tick
    if clock.transition(frame_duration):  # If it's time to move to the next frame
        spritesheet.next_frame()  # Move to the next frame
    spritesheet.move()  # Move the sprite horizontally until it reaches the target position

frame_timer = simplegui.create_timer(100, frame_timer_handler)  # Set timer to 100 ms

frame.start()  # Start the frame animation loop
frame_timer.start()  # Start the timer to update the clock
