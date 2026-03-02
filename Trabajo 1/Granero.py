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
    def __init__(self, ancho=1000, alto=600):
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
            Almacen(50, None, x=200, y=250),
            Almacen(50, None, x=500, y=250),
            Almacen(50, None, x=800, y=250)
        ]

        self.mensaje = ""
        self.color_mensaje = (255, 255, 255)
        self.corriendo = True

        self.generar_camion()

    def generar_camion(self):
        tipos_disponibles = []

        for tipo in TipoGrano:
            silos_tipo = [a for a in self.almacenes if a.tipo_grano_asignado == tipo]
            if not silos_tipo or not all(a.esta_lleno() for a in silos_tipo):
                tipos_disponibles.append(tipo)

        if not tipos_disponibles:
            self.camion_tipo = None
            return

        self.camion_tipo = random.choice(tipos_disponibles)
        self.camion_cantidad = random.choice([10, 20])

    def tipo_ya_asignado(self, tipo):
        for alm in self.almacenes:
            if alm.tipo_grano_asignado == tipo:
                return alm
        return None

    def silo_vacio(self):
        for alm in self.almacenes:
            if alm.tipo_grano_asignado is None:
                return alm
        return None

    def descargar_en_contenedor(self, indice):

        almacen = self.almacenes[indice]
        tipo = self.camion_tipo
        cantidad = self.camion_cantidad

        silo_existente = self.tipo_ya_asignado(tipo)

        # Si el tipo ya está en otro silo diferente
        if silo_existente and silo_existente != almacen:
            self.mensaje = "Ese grano ya está en otro silo"
            self.color_mensaje = (255, 100, 100)
            return

        # Si el silo está vacío, lo asignamos
        if almacen.tipo_grano_asignado is None:
            almacen.tipo_grano_asignado = tipo

        espacio = almacen.espacio_disponible()

        # Caso normal: cabe completo
        if cantidad <= espacio:
            almacen.cantidad += cantidad
            self.mensaje = "Descarga exitosa"
            self.color_mensaje = (100, 255, 100)
            self.generar_camion()
            return

        # 🔥 Caso especial: no cabe completo
        sobrante = cantidad - espacio

        if espacio > 0:
            almacen.cantidad += espacio  # llenar el primero

        segundo_silo = self.silo_vacio()

        if segundo_silo:
            segundo_silo.tipo_grano_asignado = tipo
            segundo_silo.cantidad = sobrante

            self.mensaje = "Se abrió segundo silo - FIN"
            self.color_mensaje = (255, 255, 0)

            pygame.display.flip()
            pygame.time.delay(2500)
            self.corriendo = False
        else:
            self.mensaje = "No hay espacio adicional - FIN"
            self.color_mensaje = (255, 0, 0)
            pygame.display.flip()
            pygame.time.delay(2500)
            self.corriendo = False

    def dibujar_camion(self):
        pygame.draw.rect(self.pantalla, (100, 100, 100), (350, 50, 300, 80), border_radius=10)

        texto1 = self.fuente_md.render("CAMIÓN", True, (255, 255, 255))
        self.pantalla.blit(texto1, (450, 55))

        if self.camion_tipo:
            texto2 = self.fuente_sm.render(
                f"Grano: {self.camion_tipo.name}",
                True,
                self.colores_grano[self.camion_tipo]
            )
            texto3 = self.fuente_sm.render(
                f"Cantidad: {self.camion_cantidad} T",
                True,
                (255, 255, 255)
            )
            self.pantalla.blit(texto2, (400, 80))
            self.pantalla.blit(texto3, (400, 105))

    def dibujar_almacenes(self):
        for i, alm in enumerate(self.almacenes):

            ancho_silo, alto_silo = 140, 180
            rect_silo = pygame.Rect(alm.x - 70, alm.y, ancho_silo, alto_silo)

            pygame.draw.rect(self.pantalla, (20, 20, 20), rect_silo)

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

            esta_lleno = alm.esta_lleno()
            color_borde = (255, 0, 0) if esta_lleno else (200, 200, 200)
            pygame.draw.rect(self.pantalla, color_borde, rect_silo, 3)

            txt_nombre = self.fuente_md.render(f"Contenedor {i+1}", True, (255, 255, 255))
            self.pantalla.blit(txt_nombre, (alm.x - 60, alm.y - 40))

            txt_contador = self.fuente_lg.render(
                f"{alm.cantidad} / {alm.capacidad_max} T",
                True,
                (255, 255, 255)
            )
            self.pantalla.blit(txt_contador, (alm.x - 65, alm.y + alto_silo + 20))

    def dibujar_info(self):
        txt_info = self.fuente_md.render(self.mensaje, True, self.color_mensaje)
        self.pantalla.blit(txt_info, (20, 550))

    def ejecutar(self):
        while self.corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.descargar_en_contenedor(0)
                    elif evento.key == pygame.K_2:
                        self.descargar_en_contenedor(1)
                    elif evento.key == pygame.K_3:
                        self.descargar_en_contenedor(2)

            self.pantalla.fill(self.COLOR_FONDO)

            self.dibujar_camion()
            self.dibujar_almacenes()
            self.dibujar_info()

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Granero().ejecutar()