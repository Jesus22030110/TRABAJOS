import pygame
import sys
import random
from enum import Enum
from dataclasses import dataclass


class TipoGrano(Enum):
    TRIGO = 1
    MAIZ = 2
    CEBADA = 3


@dataclass
class Almacen:
    capacidad_max: int
    tipo_grano_asignado: TipoGrano | None
    cantidad: int = 0
    x: int = 0
    y: int = 0

    def espacio_disponible(self):
        return self.capacidad_max - self.cantidad

    def esta_lleno(self):
        return self.cantidad >= self.capacidad_max


class Granero:
    def __init__(self, ancho=1100, alto=650):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Simulador de Granero")
        self.reloj = pygame.time.Clock()

        self.fuente_sm = pygame.font.Font(None, 24)
        self.fuente_md = pygame.font.Font(None, 32)
        self.fuente_lg = pygame.font.Font(None, 40)

        self.COLOR_FONDO = (30, 60, 30)
        self.colores_grano = {
            TipoGrano.TRIGO: (255, 215, 0),
            TipoGrano.MAIZ: (255, 140, 0),
            TipoGrano.CEBADA: (160, 120, 90)
        }

        self.almacenes = [
            Almacen(50, TipoGrano.TRIGO, x=150, y=250),
            Almacen(50, TipoGrano.MAIZ, x=400, y=250),
            Almacen(50, TipoGrano.CEBADA, x=650, y=250)
        ]

        # Mensaje inicial súper simple
        self.mensaje = "Esperando..."
        self.color_mensaje = (200, 200, 200)
        self.corriendo = True

        self.generar_camion()

    def generar_camion(self):
        self.camion_cantidad = random.choice([10, 20])

    def descargar_grano(self, tipo):
        silo = next((s for s in self.almacenes if s.tipo_grano_asignado == tipo), None)

        cantidad = self.camion_cantidad
        espacio = silo.espacio_disponible()

        if cantidad <= espacio:
            silo.cantidad += cantidad

            # Mensaje simplificado
            self.mensaje = f"Descarga: {cantidad}T"
            self.color_mensaje = (100, 255, 100)

            if all(s.esta_lleno() for s in self.almacenes[:3]):
                self.mensaje = "Sin capacidad libre - FIN"
                self.color_mensaje = (255, 255, 0)
                self.dibujar_todo()
                pygame.time.delay(3500)
                self.corriendo = False
            else:
                self.generar_camion()

        else:
            sobrante = cantidad - espacio
            silo.cantidad += espacio

            nuevo_silo = Almacen(capacidad_max=50, tipo_grano_asignado=tipo, cantidad=sobrante, x=900, y=250)
            self.almacenes.append(nuevo_silo)

            # Mensaje simplificado para cuando se excede
            self.mensaje = "Límite excedido - FIN"
            self.color_mensaje = (255, 100, 100)

            self.dibujar_todo()
            pygame.time.delay(4500)
            self.corriendo = False

    def dibujar_camion(self):
        # Caja del camión
        pygame.draw.rect(self.pantalla, (80, 80, 80), (400, 30, 300, 80), border_radius=10)

        texto1 = self.fuente_md.render("CAMIÓN EN ESPERA", True, (255, 255, 255))
        rect1 = texto1.get_rect(center=(550, 50))
        self.pantalla.blit(texto1, rect1)

        texto2 = self.fuente_md.render(f"Carga: {self.camion_cantidad} T", True, (200, 255, 200))
        rect2 = texto2.get_rect(center=(550, 85))
        self.pantalla.blit(texto2, rect2)

        # AQUÍ ESTÁ EL MENSAJE (Lo movimos justo debajo del camión, centrado)
        txt_info = self.fuente_md.render(self.mensaje, True, self.color_mensaje)
        rect_info = txt_info.get_rect(center=(550, 135))
        self.pantalla.blit(txt_info, rect_info)

    def dibujar_almacenes(self):
        for i, alm in enumerate(self.almacenes):
            ancho_silo, alto_silo = 140, 180
            rect_silo = pygame.Rect(alm.x - 70, alm.y, ancho_silo, alto_silo)

            pygame.draw.rect(self.pantalla, (40, 40, 40), rect_silo)

            if alm.cantidad > 0:
                altura_pixeles = int((alm.cantidad / alm.capacidad_max) * alto_silo)
                color = self.colores_grano.get(alm.tipo_grano_asignado, (100, 100, 100))

                rect_grano = pygame.Rect(
                    alm.x - 65,
                    alm.y + alto_silo - altura_pixeles,
                    ancho_silo - 10,
                    altura_pixeles
                )
                pygame.draw.rect(self.pantalla, color, rect_grano)

            color_borde = (255, 100, 100) if alm.esta_lleno() else (200, 200, 200)
            pygame.draw.rect(self.pantalla, color_borde, rect_silo, 3)

            nombre = alm.tipo_grano_asignado.name
            if i == 3:
                nombre = f"{nombre} (EXTRA)"

            txt_nombre = self.fuente_md.render(nombre, True, (255, 255, 255))
            rect_nombre = txt_nombre.get_rect(center=(alm.x, alm.y - 20))
            self.pantalla.blit(txt_nombre, rect_nombre)

            txt_contador = self.fuente_lg.render(f"{alm.cantidad} / {alm.capacidad_max} T", True, (255, 255, 255))
            rect_contador = txt_contador.get_rect(center=(alm.x, alm.y + alto_silo + 25))
            self.pantalla.blit(txt_contador, rect_contador)

    def dibujar_info(self):
        # ELIMINAMOS EL TEXTO AZUL INNECESARIO
        # Ahora solo dibujamos los botones de control centrados en la parte inferior

        controles = [
            ("TECLA [ 1 ] = TRIGO", self.colores_grano[TipoGrano.TRIGO], 220),
            ("TECLA [ 2 ] = MAÍZ", self.colores_grano[TipoGrano.MAIZ], 550),
            ("TECLA [ 3 ] = CEBADA", self.colores_grano[TipoGrano.CEBADA], 880)
        ]

        for texto, color, pos_x in controles:
            txt_ctrl = self.fuente_lg.render(texto, True, color)
            rect_ctrl = txt_ctrl.get_rect(center=(pos_x, 580))
            self.pantalla.blit(txt_ctrl, rect_ctrl)

    def dibujar_todo(self):
        self.pantalla.fill(self.COLOR_FONDO)
        self.dibujar_camion()
        self.dibujar_almacenes()
        self.dibujar_info()
        pygame.display.flip()

    def ejecutar(self):
        while self.corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.descargar_grano(TipoGrano.TRIGO)
                    elif evento.key == pygame.K_2:
                        self.descargar_grano(TipoGrano.MAIZ)
                    elif evento.key == pygame.K_3:
                        self.descargar_grano(TipoGrano.CEBADA)

            if self.corriendo:
                self.dibujar_todo()
                self.reloj.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Granero().ejecutar()
