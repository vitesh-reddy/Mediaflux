import pyglet
from pyglet import shapes
from pyglet.gl import glClearColor
import os
import subprocess

if os.name == 'nt':
    machine_path = os.popen('powershell -command "[System.Environment]::GetEnvironmentVariable(\'Path\',\'Machine\')"').read().strip()
    user_path = os.popen('powershell -command "[System.Environment]::GetEnvironmentVariable(\'Path\',\'User\')"').read().strip()
    os.environ['PATH'] = machine_path + os.pathsep + user_path + os.pathsep + os.environ.get('PATH', '')

WIDTH = 800
HEIGHT = 600
TITLE = "Bouncing Ball Animation"

BALL_RADIUS = 30
BALL_COLOR = (75, 0, 130)
BALL_START_POS = (100, HEIGHT - BALL_RADIUS - 10)
BALL_VELOCITY = [200.0, 0.0]

GRAVITY = 800.0
BOUNCE_FACTOR = 1.0

TARGET_FPS = 60
DURATION = 5
TOTAL_FRAMES = TARGET_FPS * DURATION

OUTPUT_FILE = "bouncing_ball.mp4"

ffmpeg_process = None

window = pyglet.window.Window(WIDTH, HEIGHT, TITLE, visible=False)
glClearColor(1.0, 1.0, 1.0, 1.0)
batch = pyglet.graphics.Batch()

ball = shapes.Circle(x=BALL_START_POS[0], y=BALL_START_POS[1], radius=BALL_RADIUS, color=BALL_COLOR, batch=batch)

frame_count = 0

@window.event
def on_draw():
    global frame_count, ffmpeg_process
    
    if frame_count == 0:
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{WIDTH}x{HEIGHT}',
            '-pix_fmt', 'rgba',
            '-r', str(TARGET_FPS),
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            '-f', 'mp4',
            OUTPUT_FILE
        ]
        ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    window.clear()
    batch.draw()
    
    if frame_count < TOTAL_FRAMES:
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        image_data = buffer.get_image_data()
        data = image_data.get_data('RGBA', -WIDTH * 4)
        
        if ffmpeg_process:
            ffmpeg_process.stdin.write(data)
        
        frame_count += 1
        if frame_count % 60 == 0:
            print(f"Propcessing frame {frame_count}/{TOTAL_FRAMES}")

        dt = 1.0 / TARGET_FPS
        update(dt)
    else:
        if ffmpeg_process:
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()
            print(f"Video saved to {OUTPUT_FILE}")
        pyglet.app.exit()

def update(dt):
    global ball
    
    BALL_VELOCITY[1] -= GRAVITY * dt
    
    ball.x += BALL_VELOCITY[0] * dt
    ball.y += BALL_VELOCITY[1] * dt
    
    if ball.y - BALL_RADIUS < 0:
        ball.y = BALL_RADIUS
        BALL_VELOCITY[1] *= -1 * BOUNCE_FACTOR
        
    if ball.y + BALL_RADIUS > HEIGHT:
        ball.y = HEIGHT - BALL_RADIUS
        BALL_VELOCITY[1] *= -1 * BOUNCE_FACTOR

    if ball.x - BALL_RADIUS > WIDTH:
        ball.x = -BALL_RADIUS
        
    if ball.x + BALL_RADIUS < 0:
        ball.x = WIDTH + BALL_RADIUS

if __name__ == "__main__":
    print(f"Generating {TOTAL_FRAMES} frames for {DURATION} second animation...")
    pyglet.app.run()