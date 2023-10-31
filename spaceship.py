#   https://www.youtube.com/watch?v=w_l9YINjK2I

#   pip install pygame os-sys

import pygame
import os

#   Iniciamos los módulos y mixer para dibujar textos en pantalla e introducir sonidos.

pygame.font.init()
pygame.mixer.init()

#   CONSTANTES

#   Tamaño de la ventana principal (display.set_mode), título (display.set_caption).

ANCHO, ALTO = 900, 500   
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SpaceWar!")

#   Colores.

BLANCO = (255, 255 , 255)
NEGRO = (0, 0, 0)
ROJO  = (255, 0, 0)
AMARILLO = (255, 255, 0)

#   Borde central (rect)

BORDE_CENTRO = pygame.Rect(ANCHO/2 - 5, 0, 10, ALTO)

#   Sonidos (mixer).

SONIDO_COLISION = pygame.mixer.Sound('assets/Grenade+1.wav')
SONIDO_DISPARO = pygame.mixer.Sound('assets/Shot.wav')

#   Texto para las vidas y mostrar ganador.

FUENTE_VIDAS = pygame.font.SysFont('comicsans', 20)
FUENTE_GANADOR = pygame.font.SysFont('comicsans', 20)

#   Fotogramas por segundo.

FPS = 60

#   Velocidad de movimiento. Cada vez que un usuario pulse una tecla, la nave se moverá 5 px.

VELOCIDAD = 5

#   Número de balas que puede disparar una nave a la vez y velocidad.

MAX_BALAS = 3
VELOCIDAD_BALAS = 7

#   Tamaño de las naves.

NAVE_ANCHO, NAVE_ALTO = 90, 70

#   Eventos propios (pygame.userevent) para cuando una de las naves colisiona con una bala.

CHOQUE_NAVE_AMARILLA = pygame.USEREVENT + 1
CHOQUE_NAVE_ROJA = pygame.USEREVENT + 2

#   Rutas a las imágenes, dimensiones y rotación de las naves (pygame.transform.rotate(pygame.transform.scale)).

IMAGEN_NAVE_AMARILLA = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))

NAVE_AMARILLA = pygame.transform.rotate(pygame.transform.scale(IMAGEN_NAVE_AMARILLA, (NAVE_ANCHO, NAVE_ALTO)), 90)

IMAGEN_NAVE_ROJA = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))

NAVE_ROJA = pygame.transform.rotate(pygame.transform.scale(IMAGEN_NAVE_ROJA, (NAVE_ANCHO, NAVE_ALTO)), 270)

ESPACIO = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (ANCHO, ALTO))


#   Función para dibujar cosas en pantalla con las funciones blit y draw.rect para el borde central. Actualizamos con la función display.update.

    #   Parámetros en blit: qué queremos mostrar y en qué posición.
    #   Parámetros en draw.rect: en qué pantalla queremos dibujar, el color y qué rectángulo queremos dibujar.

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


#   Función para controlar el movimiento de la nave amarilla.

def movimiento_nave_amarilla (teclas_pulsadas, rectangulo_amarillo):

  #   Izquierda

  if teclas_pulsadas[pygame.K_a] and rectangulo_amarillo.x - VELOCIDAD > 0:

    rectangulo_amarillo.x -= VELOCIDAD

  #   Derecha

  if teclas_pulsadas[pygame.K_d] and rectangulo_amarillo.x + VELOCIDAD + rectangulo_amarillo.width < BORDE_CENTRO.x:

    rectangulo_amarillo.x += VELOCIDAD

  #   Arriba

  if teclas_pulsadas[pygame.K_w] and rectangulo_amarillo.y - VELOCIDAD > 0:

    rectangulo_amarillo.y -= VELOCIDAD

  #   Abajo
  
  if teclas_pulsadas[pygame.K_s] and rectangulo_amarillo.y + VELOCIDAD + rectangulo_amarillo.height < ALTO - 15:

    rectangulo_amarillo.y += VELOCIDAD


#   Función para controlar el movimiento de la nave roja.

def movimiento_nave_roja (teclas_pulsadas, rectangulo_rojo):

  #   Izquierda

  if teclas_pulsadas[pygame.K_LEFT] and rectangulo_rojo.x - VELOCIDAD > BORDE_CENTRO.x + BORDE_CENTRO.width:

    rectangulo_rojo.x -= VELOCIDAD

  #   Derecha

  if teclas_pulsadas[pygame.K_RIGHT] and rectangulo_rojo.x + VELOCIDAD + rectangulo_rojo.width < ANCHO:

    rectangulo_rojo.x += VELOCIDAD

  #   Arriba

  if teclas_pulsadas[pygame.K_UP] and rectangulo_rojo.y - VELOCIDAD > 0:

    rectangulo_rojo.y -= VELOCIDAD

  #   Abajo
  
  if teclas_pulsadas[pygame.K_DOWN] and rectangulo_rojo.y + VELOCIDAD + rectangulo_rojo.height < ALTO - 15:

    rectangulo_rojo.y += VELOCIDAD


#   Función para el movimiento de las balas. Comprueba si las balas colisionan con el rectángulo del oponente o si se sale del mapa. En cualquiera de los casos se elimina la bala y se llama al evento de colisiones (event.post(pygame.event.Event)).

def movimiento_balas(balas_rojas, balas_amarillas, rectangulo_rojo, rectangulo_amarillo):

  #   Balas de la nave amarilla.

  for bala in balas_amarillas:

    bala.x -= VELOCIDAD_BALAS

    if rectangulo_rojo.colliderect(bala):

      balas_amarillas.remove(bala)
      pygame.event.post(pygame.event.Event(CHOQUE_NAVE_ROJA))

    elif bala.x < 0:

      balas_amarillas.remove(bala)

  #   Balas de la nave roja.

  for bala in balas_rojas:

    bala.x += VELOCIDAD_BALAS

    if rectangulo_amarillo.colliderect(bala):

      balas_rojas.remove(bala)
      pygame.event.post(pygame.event.Event(CHOQUE_NAVE_AMARILLA))
      
    elif bala.x > ANCHO:

      balas_rojas.remove(bala)


#   Función para mostrar un texto felicitando al ganador.

def mostrar_ganador(texto):

  mostrar_texto = FUENTE_GANADOR.render(texto, 1, BLANCO)
  VENTANA.blit(mostrar_texto, (ANCHO / 2 - mostrar_texto.get_width() / 2, ALTO / 2 - mostrar_texto.get_height() / 2))

  pygame.display.update()
  pygame.time.delay(5000)


#   Función principal.

def main():

  #   Rectángulos que representan las naves (rect)

  rectangulo_rojo = pygame.Rect(700,300, NAVE_ANCHO, NAVE_ALTO)
  rectangulo_amarillo = pygame.Rect(100,300, NAVE_ANCHO, NAVE_ALTO)

  #   Balas que aún están en el mapa. Las que colisionan con la otra nave o se salen del mapa se eliminan de la lista.

  balas_amarillas = []
  balas_rojas = []

  #   Vidas.

  vidas_nave_amarilla = 10
  vidas_nave_roja = 10

  #   Reloj (time.Clock)

  reloj = pygame.time.Clock()

  #   Mientras el juego no finaliza...

  en_ejecucion = True

  while en_ejecucion:

    #  Pasamos como parámetro FPS a la función tick para que el programa muestre 60 fotogramas por segundo.

    reloj.tick(FPS)

    #   Lista de eventos con los botones y teclas que pulsa cada jugador. 

    for evento in pygame.event.get():

      # 	Botón de salir

      if evento.type == pygame.QUIT:
        
          en_ejecucion = False
          pygame.quit()
      
      #   Botones de disparar. Se crea la bala en la posición de cada nave, se lanza y se produce el sonido de un disparo.

      if evento.type == pygame.KEYDOWN:

        #   Nave amarilla (control izquierda).

        if evento.key == pygame.K_LCTRL and len(balas_amarillas) < MAX_BALAS:

          bala = pygame.Rect(rectangulo_amarillo.x + rectangulo_amarillo.width,  rectangulo_amarillo.y + rectangulo_amarillo.height // 2 + 5, 10, 5)

          balas_amarillas.append(bala)
          SONIDO_DISPARO.play()

        #   Nave roja (control derecha).
  
        if evento.key == pygame.K_RCTRL and len(balas_rojas) < MAX_BALAS:

          bala = pygame.Rect(rectangulo_rojo.x + rectangulo_rojo.width,  rectangulo_rojo.y + rectangulo_rojo.height // 2 + 5, 10, 5)

          balas_rojas.append(bala)
          SONIDO_DISPARO.play()
      
      #   Si se produce una colisión se resta una vida a la nave y también se produce un sonido.
      
      if evento.type == CHOQUE_NAVE_AMARILLA:

        vidas_nave_roja -= 1
        SONIDO_COLISION.play()

      if evento.type == CHOQUE_NAVE_ROJA:

        vidas_nave_amarilla -= 1
        SONIDO_COLISION.play()   

    #   Comprobamos si hay un ganador
    
    texto_ganador = ""

    if vidas_nave_roja <= 0:

      texto_ganador = "Enhorabuena nave amrilla! Has ganado la partida"

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


  #   Comprobamos si el fichero se llama main, es decir, si este es el archivo principal.

if __name__ == "__main__":

  main()



