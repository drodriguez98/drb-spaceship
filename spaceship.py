#   https://www.youtube.com/watch?v=w_l9YINjK2I

import pygame
import os

pygame.font.init()
pygame.mixer.init()

ANCHO, ALTO = 900, 500   
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SpaceWar!")

BLANCO = (255, 255 , 255)
NEGRO = (0, 0, 0)
ROJO  = (255, 0, 0)
AMARILLO = (255, 255, 0)

BORDE_CENTRO = pygame.Rect(ANCHO/2 - 5, 0, 10, ALTO)

SONIDO_COLISION = pygame.mixer.Sound('assets/Grenade+1.wav')
SONIDO_DISPARO = pygame.mixer.Sound('assets/Shot.wav')

FUENTE_VIDAS = pygame.font.SysFont('comicsans', 20)
FUENTE_GANADOR = pygame.font.SysFont('comicsans', 20)

FPS = 60

VELOCIDAD = 5

MAX_BALAS = 3
VELOCIDAD_BALAS = 14

NAVE_ANCHO, NAVE_ALTO = 90, 70

CHOQUE_NAVE_AMARILLA = pygame.USEREVENT + 1
CHOQUE_NAVE_ROJA = pygame.USEREVENT + 2

IMAGEN_NAVE_AMARILLA = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))

NAVE_AMARILLA = pygame.transform.rotate(pygame.transform.scale(IMAGEN_NAVE_AMARILLA, (NAVE_ANCHO, NAVE_ALTO)), 90)

IMAGEN_NAVE_ROJA = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))

NAVE_ROJA = pygame.transform.rotate(pygame.transform.scale(IMAGEN_NAVE_ROJA, (NAVE_ANCHO, NAVE_ALTO)), 270)

ESPACIO = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (ANCHO, ALTO))


def dibujar_ventana(rectangulo_rojo, rectangulo_amarillo, balas_rojas, balas_amarillas, vidas_nave_roja, vidas_nave_amarilla):

  VENTANA.blit(ESPACIO, (0, 0))
  pygame.draw.rect(VENTANA, NEGRO, BORDE_CENTRO)

  VENTANA.blit(NAVE_AMARILLA, (rectangulo_amarillo.x, rectangulo_amarillo.y))
  VENTANA.blit(NAVE_ROJA, (rectangulo_rojo.x, rectangulo_rojo.y))

  vidas_nave_roja_text = FUENTE_VIDAS.render("Vidas: " + str(vidas_nave_roja), 1, BLANCO)
  vidas_nave_amarilla_text = FUENTE_VIDAS.render("Vidas: " +str(vidas_nave_amarilla), 1, BLANCO)

  VENTANA.blit(vidas_nave_roja_text, (ANCHO - vidas_nave_roja_text.get_width() - 10, 10))
  VENTANA.blit(vidas_nave_amarilla_text, (10, 10))

  for bala in balas_rojas:

    pygame.draw.rect(VENTANA, ROJO, bala)

  for bala in balas_amarillas:

    pygame.draw.rect(VENTANA, AMARILLO, bala)

  pygame.display.update()


def movimiento_nave_amarilla (teclas_pulsadas, rectangulo_amarillo):

  if teclas_pulsadas[pygame.K_a] and rectangulo_amarillo.x - VELOCIDAD > 0:

    rectangulo_amarillo.x -= VELOCIDAD

  if teclas_pulsadas[pygame.K_d] and rectangulo_amarillo.x + VELOCIDAD + rectangulo_amarillo.width < BORDE_CENTRO.x:

    rectangulo_amarillo.x += VELOCIDAD

  if teclas_pulsadas[pygame.K_w] and rectangulo_amarillo.y - VELOCIDAD > 0:

    rectangulo_amarillo.y -= VELOCIDAD
  
  if teclas_pulsadas[pygame.K_s] and rectangulo_amarillo.y + VELOCIDAD + rectangulo_amarillo.height < ALTO - 15:

    rectangulo_amarillo.y += VELOCIDAD


def movimiento_nave_roja (teclas_pulsadas, rectangulo_rojo):

  if teclas_pulsadas[pygame.K_LEFT] and rectangulo_rojo.x - VELOCIDAD > BORDE_CENTRO.x + BORDE_CENTRO.width:

    rectangulo_rojo.x -= VELOCIDAD

  if teclas_pulsadas[pygame.K_RIGHT] and rectangulo_rojo.x + VELOCIDAD + rectangulo_rojo.width < ANCHO:

    rectangulo_rojo.x += VELOCIDAD

  if teclas_pulsadas[pygame.K_UP] and rectangulo_rojo.y - VELOCIDAD > 0:

    rectangulo_rojo.y -= VELOCIDAD
  
  if teclas_pulsadas[pygame.K_DOWN] and rectangulo_rojo.y + VELOCIDAD + rectangulo_rojo.height < ALTO - 15:

    rectangulo_rojo.y += VELOCIDAD


def movimiento_balas(balas_rojas, balas_amarillas, rectangulo_rojo, rectangulo_amarillo):

  for bala in balas_amarillas:

    bala.x -= VELOCIDAD_BALAS

    if rectangulo_rojo.colliderect(bala):

      balas_amarillas.remove(bala)
      pygame.event.post(pygame.event.Event(CHOQUE_NAVE_ROJA))

    elif bala.x < 0:

      balas_amarillas.remove(bala)

  for bala in balas_rojas:

    bala.x += VELOCIDAD_BALAS

    if rectangulo_amarillo.colliderect(bala):

      balas_rojas.remove(bala)
      pygame.event.post(pygame.event.Event(CHOQUE_NAVE_AMARILLA))
      
    elif bala.x > ANCHO:

      balas_rojas.remove(bala)


def mostrar_ganador(texto):

  mostrar_texto = FUENTE_GANADOR.render(texto, 1, BLANCO)
  VENTANA.blit(mostrar_texto, (ANCHO / 2 - mostrar_texto.get_width() / 2, ALTO / 2 - mostrar_texto.get_height() / 2))

  pygame.display.update()
  pygame.time.delay(5000)


def main():

  rectangulo_rojo = pygame.Rect(700,300, NAVE_ANCHO, NAVE_ALTO)
  rectangulo_amarillo = pygame.Rect(100,300, NAVE_ANCHO, NAVE_ALTO)

  balas_amarillas = []
  balas_rojas = []

  vidas_nave_amarilla = 10
  vidas_nave_roja = 10

  reloj = pygame.time.Clock()

  en_ejecucion = True

  while en_ejecucion:

    reloj.tick(FPS)

    for evento in pygame.event.get():

      if evento.type == pygame.QUIT:
        
          en_ejecucion = False
          pygame.quit()

      if evento.type == pygame.KEYDOWN:

        if evento.key == pygame.K_LCTRL and len(balas_amarillas) < MAX_BALAS:

          bala = pygame.Rect(rectangulo_amarillo.x + rectangulo_amarillo.width,  rectangulo_amarillo.y + rectangulo_amarillo.height // 2 + 5, 10, 5)

          balas_amarillas.append(bala)
          SONIDO_DISPARO.play()

        if evento.key == pygame.K_RCTRL and len(balas_rojas) < MAX_BALAS:

          bala = pygame.Rect(rectangulo_rojo.x + rectangulo_rojo.width,  rectangulo_rojo.y + rectangulo_rojo.height // 2 + 5, 10, 5)

          balas_rojas.append(bala)
          SONIDO_DISPARO.play()

      if evento.type == CHOQUE_NAVE_AMARILLA:

        vidas_nave_roja -= 1
        SONIDO_COLISION.play()

      if evento.type == CHOQUE_NAVE_ROJA:

        vidas_nave_amarilla -= 1
        SONIDO_COLISION.play()   
    
    texto_ganador = ""

    if vidas_nave_roja <= 0:

      texto_ganador = "Enhorabuena nave amarilla! Has ganado la partida"

    if vidas_nave_amarilla <= 0:

      texto_ganador = "Enhorabuena nave roja! Has ganado la partida"

    if texto_ganador != "":

      mostrar_ganador(texto_ganador)
      break
    
    teclas_pulsadas = pygame.key.get_pressed()

    movimiento_nave_amarilla(teclas_pulsadas, rectangulo_amarillo)
    movimiento_nave_roja(teclas_pulsadas, rectangulo_rojo)
    movimiento_balas(balas_amarillas, balas_rojas, rectangulo_amarillo, rectangulo_rojo) 
    dibujar_ventana(rectangulo_rojo, rectangulo_amarillo, balas_rojas, balas_amarillas, vidas_nave_roja, vidas_nave_amarilla)

  main()


if __name__ == "__main__":

  main()
