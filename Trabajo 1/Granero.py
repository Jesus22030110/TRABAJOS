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
    tipo_grano_asignado: TipoGrano
    cantidad: int = 0
    x: int = 0
    y: int = 0

    def puede_agregar(self, tipo: TipoGrano, cantidad: int) -> bool:
        return self.tipo_grano_asignado == tipo and (self.cantidad + cantidad) <= self.capacidad_max

    def agregar(self, tipo: TipoGrano, cantidad: int) -> bool:
        if self.puede_agregar(tipo, cantidad):
            self.cantidad += cantidad
            return True
        return False


class Granero:
    def __init__(self, ancho=1000, alto=600):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Monitor de Graneros Pro")
        self.reloj = pygame.time.Clock()

        # Fuentes
        self.fuente_sm = pygame.font.Font(None, 24)
        self.fuente_md = pygame.font.Font(None, 32)
        self.fuente_lg = pygame.font.Font(None, 45)

        # Colores
        self.COLOR_FONDO = (30, 60, 30)  # Verde oscuro para contraste
        self.colores_grano = {
            TipoGrano.TRIGO: (255, 215, 0),  # Dorado
            TipoGrano.MAIZ: (255, 140, 0),  # Naranja
            TipoGrano.CEBADA: (160, 120, 90)  # Café claro
        }

        self.almacenes = [
            Almacen(50, TipoGrano.TRIGO, x=200, y=300),
            Almacen(50, TipoGrano.MAIZ, x=500, y=300),
            Almacen(50, TipoGrano.CEBADA, x=800, y=300)
        ]

        self.ultima_carga = 0
        self.mensaje = "Esperando descarga..."
        self.color_mensaje = (255, 255, 255)
        self.corriendo = True

    def dibujar_botones(self):
        """Dibuja los indicadores de botones en la parte superior central"""
        opciones = [
            ("1", "TRIGO", self.colores_grano[TipoGrano.TRIGO], 300),
            ("2", "MAÍZ", self.colores_grano[TipoGrano.MAIZ], 500),
            ("3", "CEBADA", self.colores_grano[TipoGrano.CEBADA], 700)
        ]

        for tecla, nombre, color, x_pos in opciones:
            rect_btn = pygame.Rect(x_pos - 60, 30, 120, 50)
            pygame.draw.rect(self.pantalla, (50, 50, 50), rect_btn, border_radius=10)
            pygame.draw.rect(self.pantalla, color, rect_btn, 2, border_radius=10)

            txt_tecla = self.fuente_md.render(tecla, True, color)
            txt_grano = self.fuente_sm.render(nombre, True, (255, 255, 255))
            self.pantalla.blit(txt_tecla, (x_pos - 50, 43))
            self.pantalla.blit(txt_grano, (x_pos - 20, 48))

    def dibujar_almacenes(self):
        for alm in self.almacenes:
            # Color base
            color = self.colores_grano[alm.tipo_grano_asignado]
            esta_lleno = alm.cantidad >= alm.capacidad_max

            # Dibujar el "Silo" (Contenedor)
            ancho_silo, alto_silo = 140, 180
            rect_silo = pygame.Rect(alm.x - 70, alm.y, ancho_silo, alto_silo)

            # Fondo del silo
            pygame.draw.rect(self.pantalla, (20, 20, 20), rect_silo)

            # Relleno de grano
            if alm.cantidad > 0:
                altura_pixeles = int((alm.cantidad / alm.capacidad_max) * alto_silo)
                rect_grano = pygame.Rect(alm.x - 65, alm.y + alto_silo - altura_pixeles, ancho_silo - 10,
                                         altura_pixeles)
                pygame.draw.rect(self.pantalla, color, rect_grano)

            # Borde del silo (Rojo si está lleno)
            color_borde = (255, 0, 0) if esta_lleno else color
            pygame.draw.rect(self.pantalla, color_borde, rect_silo, 3, border_radius=5)

            # Etiquetas
            txt_nombre = self.fuente_md.render(alm.tipo_grano_asignado.name, True, (255, 255, 255))

            # Contador Dinámico (Cambia a ROJO si está lleno)
            color_texto_cont = (255, 50, 50) if esta_lleno else (255, 255, 255)
            txt_contador = self.fuente_lg.render(f"{alm.cantidad} / {alm.capacidad_max} T", True, color_texto_cont)

            self.pantalla.blit(txt_nombre, (alm.x - 40, alm.y - 40))
            self.pantalla.blit(txt_contador, (alm.x - 65, alm.y + alto_silo + 20))

    def dibujar_info_inferior(self):
        # Panel de mensajes
        txt_info = self.fuente_md.render(self.mensaje, True, self.color_mensaje)
        self.pantalla.blit(txt_info, (20, 550))

        if self.ultima_carga > 0:
            txt_carga = self.fuente_sm.render(f"Último camión: {self.ultima_carga}T", True, (200, 200, 200))
            self.pantalla.blit(txt_carga, (800, 555))

    def descargar_grano(self, tipo: TipoGrano):
        cantidad = random.choice([10, 20])
        self.ultima_carga = cantidad

        # Buscar el almacén correspondiente
        almacen_destino = next(a for a in self.almacenes if a.tipo_grano_asignado == tipo)

        if almacen_destino.agregar(tipo, cantidad):
            self.mensaje = f"DESCARGA EXITOSA: +{cantidad}T de {tipo.name}"
            self.color_mensaje = (100, 255, 100)  # Verde éxito
        else:
            self.mensaje = f"¡ALERTA! El granero de {tipo.name} no tiene espacio para {cantidad}T"
            self.color_mensaje = (255, 100, 100)  # Rojo error

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

            self.pantalla.fill(self.COLOR_FONDO)
            self.dibujar_botones()
            self.dibujar_almacenes()
            self.dibujar_info_inferior()

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Granero().ejecutar()
