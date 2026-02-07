import pyglet

window = pyglet.window.Window(800, 600, resizable=True)

car1 = pyglet.image.load('car1.jpg')
car2 = pyglet.image.load('car2.jpg')
car3 = pyglet.image.load('car3.jpg')
images = [car1, car2, car3]

index = 0
sprite = pyglet.sprite.Sprite(images[index])

def center_sprite(img):
    sprite.image = img
    sprite.x = (window.width - img.width) // 2
    sprite.y = (window.height - img.height) // 2

center_sprite(images[index])

display_time = 0.5
timer = 0

@window.event
def on_draw():
    window.clear()
    sprite.draw()

@window.event
def on_resize(width, height):
    center_sprite(sprite.image)
    return pyglet.event.EVENT_HANDLED

def update(dt):
    global timer, index
    timer += dt
    if timer >= display_time:
        timer = 0
        index = (index + 1) % len(images)
        center_sprite(images[index])

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
