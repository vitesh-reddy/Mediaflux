import pyglet

window = pyglet.window.Window(800, 600, resizable=True)

car1 = pyglet.image.load('car1.jpg')
car2 = pyglet.image.load('car2.jpg')
car3 = pyglet.image.load('car3.jpg')
images = [car1, car2, car3]

index = 0
sprite = pyglet.sprite.Sprite(images[index])

def ease_in(t):
    return t * t  # quadratic ease-in

display_time = 0.5      # hold time
slide_duration = 0.2    # slide-in time

timer = 0.0
sliding = True

start_x = 0
start_y = 0
target_x = 0
target_y = 0

def set_targets_for_image(i):
    global start_x, start_y, target_x, target_y

    img = images[i]
    target_x = (window.width - img.width) // 2
    target_y = (window.height - img.height) // 2

    # Different direction per image:
    # 0 -> from left, 1 -> from top, 2 -> from right
    if i % 3 == 0:         # from left
        start_x = -img.width
        start_y = target_y
    elif i % 3 == 1:       # from top
        start_x = target_x
        start_y = window.height
    else:                  # from right
        start_x = window.width
        start_y = target_y

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
    # Recalculate targets for current image on resize
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
            timer = 0.0  # start hold time
    else:
        if timer >= display_time:
            set_image(index + 1)
            start_slide_in()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
