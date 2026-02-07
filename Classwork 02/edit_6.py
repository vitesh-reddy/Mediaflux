import pyglet

window = pyglet.window.Window(800, 600, resizable=True)

car1 = pyglet.image.load('car1.jpg')
car2 = pyglet.image.load('car2.jpg')
car3 = pyglet.image.load('car3.jpg')
car4 = pyglet.image.load('car4.jpg')
car5 = pyglet.image.load('car5.jpg')
car6 = pyglet.image.load('car6.jpg')
images = [car1, car2, car3, car4, car5, car6]

index = 0
sprite = pyglet.sprite.Sprite(images[index])

def ease_in(t):
    return t * t

display_time = 0.5
slide_duration = 0.2

timer = 0.0
sliding = True

start_x = 0
start_y = 0
target_x = 0
target_y = 0
scaled_width = 0
scaled_height = 0

def calculate_scale(img):
    img_ratio = img.width / img.height
    win_ratio = window.width / window.height
    
    if img_ratio > win_ratio:
        scale = window.width / img.width
    else:
        scale = window.height / img.height
    
    return scale

def set_targets_for_image(i):
    global start_x, start_y, target_x, target_y, scaled_width, scaled_height

    img = images[i]
    scale = calculate_scale(img)
    sprite.scale = scale
    
    scaled_width = img.width * scale
    scaled_height = img.height * scale
    
    target_x = (window.width - scaled_width) / 2
    target_y = (window.height - scaled_height) / 2

    if i % 6 == 0:
        start_x = -scaled_width
        start_y = target_y
    elif i % 6 == 1:
        start_x = target_x
        start_y = window.height
    elif i % 6 == 2:
        start_x = window.width
        start_y = target_y
    elif i % 6 == 3:
        start_x = target_x
        start_y = -scaled_height
    elif i % 6 == 4:
        start_x = -scaled_width
        start_y = target_y
    else:
        start_x = target_x
        start_y = window.height

def set_image(i):
    global index
    index = i % len(images)
    img = images[index]
    sprite.image = img
    set_targets_for_image(index)
    sprite.x = start_x
    sprite.y = start_y

def start_slide_in():
    global timer, sliding
    timer = 0.0
    sliding = True

set_image(index)
start_slide_in()

@window.event
def on_draw():
    window.clear()
    sprite.draw()

@window.event
def on_resize(width, height):
    set_targets_for_image(index)
    return pyglet.event.EVENT_HANDLED

def update(dt):
    global timer, sliding

    timer += dt

    if sliding:
        t = min(timer / slide_duration, 1.0)
        e = ease_in(t)
        sprite.x = start_x + (target_x - start_x) * e
        sprite.y = start_y + (target_y - start_y) * e

        if t >= 1.0:
            sliding = False
            timer = 0.0
    else:
        if timer >= display_time:
            set_image(index + 1)
            start_slide_in()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
