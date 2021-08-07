import random
import pygame
from colors import *
from carrito import Car 
from alimento import Alimento
from tools import check_collision

pygame.init()

# Configura ancho y alto de la ventana
size = (420, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Corriendo Saludable")
# Se usa para administrar qué tan rápido se actualiza la pantalla 
clock = pygame.time.Clock()

# cargar las fuentes
font_40 = pygame.font.SysFont("Arial", 40, True, False)
font_30 = pygame.font.SysFont("Arial", 30, True, False)
text_title = font_40.render("Correr Saludable", True, TEXT_COLOR)
text_ins = font_30.render("Click para jugar!", True, TEXT_COLOR)

def draw_main_menu():
    screen.blit(text_title, [size[0] / 4 - 100, size[1] / 4 - 100])
    
    score_text = font_40.render("Score total: " + str(score), True, TEXT_COLOR)
    score_sano = font_40.render("Score bueno: " + str(scoreSs), True, TEXT_COLOR)
    score_insano = font_40.render("Score malo: " + str(scoreNs), True, TEXT_COLOR)
    screen.blit(score_text, [size[0] / 4 - 60, size[1]/4-30])
    screen.blit(score_sano, [size[0] / 4 - 60, size[1]/4+10])
    screen.blit(score_insano, [size[0] / 4 - 60, size[1]/4+50])

    screen.blit(text_ins, [size[0] / 4 - 45, size[1]/4+100])
    pygame.display.flip()

# Crear un objeto player
player = Car(175, 475, 0, 0, 70, 131, RED)
player.load_image("white_car.png")
player.load_audio("soundtrack.wav")

# Configuración de carros enemigos
cars = []
car_count = 2
#for i in range(car_count):
x = random.randrange(0, 340)
car = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10), 60, 60, CAR_COLOR)
car.load_image("blue_car.png")
cars.append(car)

x = random.randrange(0, 340)
car1 = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10), 60, 60, CAR_COLOR)
car1.load_image("red_car.png")
cars.append(car1)

#Configuracion de Alimentos Saludables
alimentoSano = []
aliment_count = 2

x = random.randrange(0,340)
ali = Alimento(x,random.randrange(-150,-50),0,random.randint(5,10),60,60, CAR_COLOR)
ali.load_image("manza.png")
alimentoSano.append(ali)

x = random.randrange(0,340)
ali1 = Alimento(x,random.randrange(-150,-50),0,random.randint(5,10),60,60, CAR_COLOR)
ali1.load_image("zana.png")
alimentoSano.append(ali1)

#configuracion de alimentos dañinos

alimentoDanino = []

x = random.randrange(0,340)
alid = Alimento(x,random.randrange(-150,-50),0,random.randint(5,10),60,60, CAR_COLOR)
alid.load_image("lays.png")
alimentoDanino.append(alid)

x = random.randrange(0,340)
alid1 = Alimento(x,random.randrange(-150,-50),0,random.randint(5,10),60,60, CAR_COLOR)
alid1.load_image("coca.png")
alimentoDanino.append(alid1)

# Configurar los stripes.
stripes = []
stripe_count = 20
stripe_x = 185
stripe_y = -10
stripe_width = 20
stripe_height = 80
space = 40
for i in range(stripe_count):
    stripes.append([190, stripe_y])
    stripe_y += stripe_height + space

collision = True
score = 0
scoreSs = 0
scoreNs = 0
done = False

player.play_audio()


velocidad = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Restablece todo cuando la usuaria inicia el juego.(carritos)
        if collision and event.type == pygame.MOUSEBUTTONDOWN:
            collision = False
            for i in range(car_count):
                cars[i].y = random.randrange(-150, -50)
                cars[i].x = random.randrange(0, 350)
                alimentoSano[i].y = random.randrange(-150,-50)
                alimentoSano[i].x = random.randrange(0,350)
                alimentoDanino[i].y = random.randrange(-150,-50)
                alimentoDanino[i].x = random.randrange(0,350)
            player.x = 175
            player.dx = 0
            score = 0
            scoreSs = 0
            scoreNs = 0
            velocidad = 4
            pygame.mouse.set_visible(False)

        if not collision:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 4
                elif event.key == pygame.K_LEFT:
                    player.dx = -4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.dx = 0
                elif event.key == pygame.K_RIGHT:
                    player.dx = 0

    screen.fill(GRAY)

    if not collision:
        # Dibujar los stripes
        for i in range(stripe_count):
            pygame.draw.rect(screen, WHITE, [stripes[i][0], stripes[i][1], stripe_width, stripe_height])
        # mover los stripes
        for i in range(stripe_count):
            stripes[i][1] += 3
            if stripes[i][1] > size[1]:
                stripes[i][1] = -40 - stripe_height

        player.draw_image(screen)
        player.move_x()
        player.check_out_of_screen()

        # Comprueba si los coches enemigos salen de la pantalla.
        for i in range(car_count):
            cars[i].draw_image(screen)
            cars[i].y += cars[i].dy
            if cars[i].y > size[1]:
                score += 10
                cars[i].y = random.randrange(-150, -50)
                cars[i].x = random.randrange(0, 340)
                cars[i].dy = 4 + velocidad #random.randint(4, 9)
                
        # Comprueba si los coches enemigos salen de la pantalla.
        for i in range(car_count):
            alimentoSano[i].draw_image(screen)
            alimentoSano[i].y += alimentoSano[i].dy
            if check_collision(player.x, player.y, player.width, \
                               player.height, alimentoSano[i].x, alimentoSano[i].y, \
                               alimentoSano[i].width, alimentoSano[i].height):
                score += 20
                scoreSs += 20
                alimentoSano[i].y = random.randrange(-150, -50)
                alimentoSano[i].x = random.randrange(0, 340)
                alimentoSano[i].dy = 4 #random.randint(4, 9)
                pygame.mouse.set_visible(True)
                if velocidad > 1:
                    velocidad -= 1
                else:
                    velocidad = 0
            if alimentoSano[i].y > size[1]:
                alimentoSano[i].y = random.randrange(-150, -50)
                alimentoSano[i].x = random.randrange(0, 340)
                alimentoSano[i].dy = 4 #random.randint(4, 9)

        # Comprueba si los coches enemigos salen de la pantalla.
        for i in range(car_count):
            alimentoDanino[i].draw_image(screen)
            alimentoDanino[i].y += alimentoDanino[i].dy
            if check_collision(player.x, player.y, player.width, \
                               player.height, alimentoDanino[i].x, alimentoDanino[i].y, \
                               alimentoDanino[i].width, alimentoDanino[i].height):
                score -= 30
                scoreNs += 30
                alimentoDanino[i].y = random.randrange(-150, -50)
                alimentoDanino[i].x = random.randrange(0, 340)
                alimentoDanino[i].dy = 4 #random.randint(4, 9)
                pygame.mouse.set_visible(True)
                velocidad += 1
            if alimentoDanino[i].y > size[1]:
                alimentoDanino[i].y = random.randrange(-150, -50)
                alimentoDanino[i].x = random.randrange(0, 340)
                alimentoDanino[i].dy = 4 #random.randint(4, 9)


        # Comprueba la colisión del jugador con el coche.
        for i in range(car_count):
            if check_collision(player.x, player.y, player.width, \
                               player.height, cars[i].x, cars[i].y, \
                               cars[i].width, cars[i].height):
                collision = True
                pygame.mouse.set_visible(True)
                break

        txt_score = font_30.render("Score: "+str(score), True, WHITE)
        txt_salu = font_30.render("Saludable: "+str(scoreSs),True,WHITE)
        txt_insa = font_30.render("NoSaludable: "+str(scoreNs),True,WHITE)
        screen.blit(txt_score, [15, 15])
        screen.blit(txt_salu, [15, 50])
        screen.blit(txt_insa, [15, 85])

        pygame.display.flip()
    else:
        draw_main_menu()

    clock.tick(60)

pygame.quit()
