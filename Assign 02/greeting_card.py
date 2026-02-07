import pyglet
from pyglet import gl
import math
import random
from PIL import Image
import numpy as np

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
INPUT_IMAGE = "Alakh Pandey 2K.png"
OUTPUT_IMAGE = "greeting_card.png"
MESSAGE = "Happy Learning"

config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, 
                               caption="Greeting Card Generator",
                               config=config)


class GreetingCard:
    
    def __init__(self):
        try:
            self.main_image = pyglet.image.load(INPUT_IMAGE)
            self.setup_image()
        except Exception as e:
            print(f"Error loading image: {e}")
            pyglet.app.exit()
            return
        
        self.create_decorations()
        self.setup_text()
        self.auto_save_scheduled = False
        
        print("Greeting card ready!")
        print("Saving automatically...")
    
    def setup_image(self):
        padding = 80
        available_width = WINDOW_WIDTH - padding * 2
        available_height = WINDOW_HEIGHT - padding * 2
        
        img_ratio = self.main_image.width / self.main_image.height
        win_ratio = available_width / available_height
        
        if img_ratio > win_ratio:
            scale = available_width / self.main_image.width
        else:
            scale = available_height / self.main_image.height
        
        self.sprite = pyglet.sprite.Sprite(self.main_image)
        self.sprite.scale = scale
        
        self.sprite.x = (WINDOW_WIDTH - self.main_image.width * scale) / 2
        self.sprite.y = (WINDOW_HEIGHT - self.main_image.height * scale) / 2
        
        self.img_left = self.sprite.x
        self.img_right = self.sprite.x + self.main_image.width * scale
        self.img_bottom = self.sprite.y
        self.img_top = self.sprite.y + self.main_image.height * scale
        self.img_width = self.main_image.width * scale
        self.img_height = self.main_image.height * scale
    
    def create_decorations(self):
        self.flowers = []
        self.confetti = []
        self.sparkles = []
        
        random.seed(42)
        
        for i in range(12):
            angle = (i / 12) * 2 * math.pi
            distance = 80
            center_x = WINDOW_WIDTH // 2
            center_y = WINDOW_HEIGHT // 2
            
            if i % 3 == 0:
                x = self.img_left - random.uniform(20, 50)
                y = random.uniform(self.img_bottom + 50, self.img_top - 50)
            elif i % 3 == 1:
                x = self.img_right + random.uniform(20, 50)
                y = random.uniform(self.img_bottom + 50, self.img_top - 50)
            else:
                x = random.uniform(self.img_left + 50, self.img_right - 50)
                if random.random() > 0.5:
                    y = self.img_top + random.uniform(20, 50)
                else:
                    y = self.img_bottom - random.uniform(20, 50)
            
            self.flowers.append({
                'x': x, 'y': y,
                'size': random.uniform(15, 25),
                'color': random.choice([
                    (255, 105, 180), (255, 192, 203), (255, 182, 193),
                    (255, 160, 122), (255, 218, 185), (255, 240, 245)
                ])
            })
        
        for _ in range(40):
            x = random.uniform(0, WINDOW_WIDTH)
            y = random.uniform(0, WINDOW_HEIGHT)
            
            if (self.img_left - 80 < x < self.img_right + 80 and 
                self.img_bottom - 80 < y < self.img_top + 80):
                continue
            
            self.confetti.append({
                'x': x, 'y': y,
                'width': random.uniform(8, 15),
                'height': random.uniform(3, 6),
                'angle': random.uniform(0, 360),
                'color': random.choice([
                    (255, 215, 0), (255, 105, 180), (135, 206, 250),
                    (144, 238, 144), (255, 160, 122), (221, 160, 221)
                ])
            })
        
        for _ in range(60):
            x = random.uniform(0, WINDOW_WIDTH)
            y = random.uniform(0, WINDOW_HEIGHT)
            
            if (self.img_left - 60 < x < self.img_right + 60 and 
                self.img_bottom - 60 < y < self.img_top + 60):
                continue
            
            self.sparkles.append({
                'x': x, 'y': y,
                'size': random.uniform(2, 4),
                'color': (255, 255, 220)
            })
    
    def setup_text(self):
        self.main_label = pyglet.text.Label(
            MESSAGE,
            font_name='Brush Script MT',
            font_size=68,
            x=WINDOW_WIDTH // 2,
            y=self.img_bottom + 60,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)
        )
    
    def draw_background(self):
        bg1 = pyglet.shapes.Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, color=(250, 245, 240))
        bg1.draw()
        
        vignette_size = 200
        for i in range(20):
            alpha = int(10 * (1 - i / 20))
            border = i * 10
            rect = pyglet.shapes.BorderedRectangle(
                border, border,
                WINDOW_WIDTH - border * 2, WINDOW_HEIGHT - border * 2,
                border=0,
                color=(240, 220, 200),
            )
            rect.opacity = alpha
            rect.draw()
    
    def draw_shadow(self):
        shadow_offset = 15
        shadow = pyglet.shapes.Rectangle(
            self.img_left + shadow_offset,
            self.img_bottom - shadow_offset,
            self.img_width,
            self.img_height,
            color=(0, 0, 0)
        )
        shadow.opacity = 40
        shadow.draw()
    
    def draw_border(self):
        border_width = 12
        
        outer = pyglet.shapes.Rectangle(
            self.img_left - border_width,
            self.img_bottom - border_width,
            self.img_width + border_width * 2,
            self.img_height + border_width * 2,
            color=(64, 224, 208)
        )
        outer.draw()
        
        inner = pyglet.shapes.BorderedRectangle(
            self.img_left - border_width + 3,
            self.img_bottom - border_width + 3,
            self.img_width + border_width * 2 - 6,
            self.img_height + border_width * 2 - 6,
            border=2,
            color=(64, 224, 208),
            border_color=(0, 139, 139)
        )
        inner.draw()
    
    def draw_flowers(self):
        for flower in self.flowers:
            for petal in range(5):
                angle = (petal / 5) * 2 * math.pi
                offset = flower['size'] * 0.6
                px = flower['x'] + math.cos(angle) * offset
                py = flower['y'] + math.sin(angle) * offset
                
                petal_circle = pyglet.shapes.Circle(
                    px, py, flower['size'] * 0.5, 
                    color=flower['color']
                )
                petal_circle.opacity = 200
                petal_circle.draw()
            
            center = pyglet.shapes.Circle(
                flower['x'], flower['y'], flower['size'] * 0.3,
                color=(255, 215, 0)
            )
            center.draw()
    
    def draw_confetti(self):
        for piece in self.confetti:
            confetti_rect = pyglet.shapes.Rectangle(
                piece['x'], piece['y'],
                piece['width'], piece['height'],
                color=piece['color']
            )
            confetti_rect.rotation = piece['angle']
            confetti_rect.opacity = 180
            confetti_rect.draw()
    
    def draw_sparkles(self):
        for sparkle in self.sparkles:
            star = pyglet.shapes.Star(
                sparkle['x'], sparkle['y'],
                sparkle['size'] * 2, sparkle['size'],
                num_spikes=4,
                color=sparkle['color']
            )
            star.opacity = 200
            star.draw()
    
    def draw_text(self):
        shadow_distance = 6
        for offset in range(shadow_distance, 0, -1):
            alpha = int(180 * (1 - offset / (shadow_distance + 1)))
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx == 0 and dy == 0:
                        continue
                    shadow = pyglet.text.Label(
                        MESSAGE,
                        font_name='Brush Script MT',
                        font_size=68,
                        x=self.main_label.x + dx,
                        y=self.main_label.y + dy,
                        anchor_x='center',
                        anchor_y='center',
                        color=(0, 0, 0, alpha)
                    )
                    shadow.draw()
        
        self.main_label.draw()
    
    def draw(self):
        window.clear()
        
        self.draw_background()
        self.draw_sparkles()
        self.draw_confetti()
        self.draw_flowers()
        self.draw_shadow()
        self.draw_border()
        self.sprite.draw()
        self.draw_text()
        
        if not self.auto_save_scheduled:
            pyglet.clock.schedule_once(self.save_to_file, 2.0)
            self.auto_save_scheduled = True
    
    def save_to_file(self, dt=None):
        print(f"\nSaving greeting card to {OUTPUT_IMAGE}...")
        try:
            gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
            data = (gl.GLubyte * (3 * WINDOW_WIDTH * WINDOW_HEIGHT))(0)
            gl.glReadPixels(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, data)
            image = Image.frombytes('RGB', (WINDOW_WIDTH, WINDOW_HEIGHT), data)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image.save(OUTPUT_IMAGE)
            print(f"Greeting card saved successfully!")
            print("You can close the window or press ESC to exit")
        except Exception as e:
            print(f"Error saving: {e}")


card = GreetingCard()


@window.event
def on_draw():
    card.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        card.save_to_file()
    elif symbol == pyglet.window.key.ESCAPE:
        pyglet.app.exit()


if __name__ == "__main__":
    pyglet.app.run()
