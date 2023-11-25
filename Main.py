import pygame
from pygame.locals import *

from Shaders import *
from GlOpen import *
from ModelOGL import Model

from math import cos, sin, radians

width = 960
height = 540

def createModel(direction : str, texture : str, texture_for_mixture : str, position = [0, 0], scales = [0, 0, 0]):
    model = Model(direction, texture, texture_for_mixture)
    model.position.y -= position[0]
    model.position.z -= position[1]
    model.scale.x = scales[0]
    model.scale.y = scales[1]
    model.scale.z = scales[2]
    return model

def all_keyboard_input(keys):

    # ZOOM
    if keys[K_q]:
        if rend.cam_distance > 2:
            rend.cam_distance -= 2 * delta_time
    elif keys[K_e]:
        if rend.cam_distance < 10:
            rend.cam_distance += 2 * delta_time

# HORIZONTAL MOVEMENT
    if keys[K_a]:
        rend.angle_x -= 30 * delta_time
    elif keys[K_d]:
        rend.angle_x += 30 * delta_time
# VERTICAL MOVEMENT
    if keys[K_w]:
        rend.angle_y += 30 * delta_time
    elif keys[K_s]:
        rend.angle_y -= 30 * delta_time
# X ROTATION
    rend.cam_position.x = rend.target.x + sin(radians(rend.angle_x)) * rend.cam_distance
    rend.cam_position.z = rend.target.z + cos(radians(rend.angle_x)) * rend.cam_distance
# Y ROTATION
    rend.cam_position.y = rend.target.y + sin(radians(rend.angle_y)) * rend.cam_distance
# LIGHT HANDLER
    if keys[K_LEFT]:
        rend.point_light.x -= 10 * delta_time
    elif keys[K_RIGHT]:
        rend.point_light.x += 10 * delta_time
    elif keys[K_UP]:
        rend.point_light.y += 10 * delta_time
    elif keys[K_DOWN]:
        rend.point_light.y -= 10 * delta_time
# SHADER HANDLER
    if keys[K_1]:
        rend.set_shaders(vertex_shader, fragment_shader)
    if keys[K_2]:
        rend.set_shaders(vertex_shader_animation, fragment_shader_animation)
    if keys[K_3]:
        rend.set_shaders(vertex_shader_color, fragment_shader_color)
    if keys[K_4]:
        rend.set_shaders(vertex_shader_best, toon_shader_fs)
    if keys[K_5]:
        rend.set_shaders(vertex_shader_best, rainbow_fs)
    if keys[K_6]:
        rend.set_shaders(mix_two_textures_vs, mix_two_textures_fs)    
    if keys[K_7]:
        rend.set_shaders(party_extreme_vs, multicolor_shader)
# CHANGE MODEL
    if keys[K_f]: # CAT
        model_actual = model_1
        rend.scene[0] = model_actual
    if keys[K_g]: 
        model_actual = model_2
        rend.scene[0] = model_actual
    if keys[K_h]: #
        model_actual = model_3
        rend.scene[0] = model_actual
    if keys[K_j]: # 
        model_actual = model_4
        rend.scene[0] = model_actual

if __name__ == "__main__":

    delta_time = 0 
    sensitivity = 0.5
    min_zoom = 1.0  
    max_zoom = 10.0 
    zoom_speed = 0.3  



    pygame.init()
    pygame.mixer.init()

    screen_menu = pygame.display.set_mode((width, height))
    pygame.mixer.music.load('resources/music/mainTheme.mp3')
    pygame.mixer.music.play(-1)  

    background_image = pygame.image.load('resources/textures/main.jpg').convert()
    background_image = pygame.transform.scale(background_image, (width, height))

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    in_menu = False

        screen_menu.blit(background_image, (0, 0))
        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    
    rend = Renderer(screen)

    rend.set_shaders(vertex_shader, fragment_shader)

    rend.target.z = -5

    model_actual = None
    model_1 = createModel("resources/models/Charizard.obj", "resources/textures/charizard.bmp", "resources/textures/earthDay.bmp", [1, 5], [0.07, 0.07, 0.07])
    model_2 = createModel("resources/models/11.obj", "resources/textures/groudon.bmp", "resources/textures/earthDay.bmp", [1.5, 5], [0.1, 0.1, 0.1])
    model_3 = createModel("resources/models/Pokeball.obj", "resources/textures/pokeball.bmp", "resources/textures/earthDay.bmp", [1.5, 5], [0.75, 0.75, 0.75])
    model_4 = createModel("resources/models/CaveCrystal01.obj", "resources/textures/CaveCrystal1_Lava1_Diffuse.bmp", "resources/textures/earthDay.bmp", [0, 2], [0.01, 0.01, 0.01])
    model_actual = model_1
    rend.scene.append(model_actual)
    is_running = True
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

    while is_running:

        keys = pygame.key.get_pressed()
        x, y = pygame.mouse.get_pos()
# KEYBOARD INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

                elif event.key == pygame.K_z:
                    rend.filled_mode()
                elif event.key == pygame.K_x:
                    rend.wireframe_mode()

            if event.type == pygame.MOUSEMOTION:
                # Captura el movimiento del mouse
                x, y = event.rel

                # Aplica rotación horizontal y vertical basada en el movimiento del mouse
                rend.angle_x += x * sensitivity 
                rend.angle_y -= y * sensitivity 

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll hacia arriba
                    rend.cam_distance = max(min_zoom, rend.cam_distance - zoom_speed)
                elif event.button == 5:  # Scroll hacia abajo
                    rend.cam_distance = min(max_zoom, rend.cam_distance + zoom_speed)
        all_keyboard_input(keys) 

        delta_time = clock.tick(60) / 1000
        rend.time += delta_time

        rend.update()
        rend.render()
        pygame.display.flip()

    pygame.quit()
