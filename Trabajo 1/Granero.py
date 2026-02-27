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
    tipo_grano_asignado: TipoGrano  # Tipo fijo para este granero
    cantidad: int = 0
    x: int = 0
    y: int = 0

    def puede_agregar(self, tipo: TipoGrano, cantidad: int) -> bool:
        # Solo permite si el tipo coincide con su asignación y hay espacio
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
        pygame.display.set_caption("Sistema de Granero - Especializado por Grano")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 20)
        self.fuente_grande = pygame.font.Font(None, 30)

        # Cada almacén nace con un tipo de grano asignado de forma fija
        self.almacenes = [
            Almacen(50, TipoGrano.TRIGO, x=150, y=200),
            Almacen(50, TipoGrano.MAIZ, x=450, y=200),
            Almacen(50, TipoGrano.CEBADA, x=750, y=200)
        ]

        self.camion_x = 500
        self.camion_y = 450
        self.capacidad_total_sistema = 150
        self.ultima_carga = 0
        self.mensaje_error = ""
        self.corriendo = True

    def dibujar_almacenes(self):
        colores = {
            TipoGrano.TRIGO: (220, 180, 0),
            TipoGrano.MAIZ: (180, 120, 0),
            TipoGrano.CEBADA: (100, 80, 50)
        }

        for alm in self.almacenes:
            # Color del borde según el grano asignado para identificarlo
            color_borde = colores[alm.tipo_grano_asignado]
            pygame.draw.rect(self.pantalla, color_borde, (alm.x - 40, alm.y - 40, 80, 80), 3)

            # Relleno
            if alm.cantidad > 0:
                altura_relleno = int((alm.cantidad / alm.capacidad_max) * 60)
                pygame.draw.rect(self.pantalla, color_borde,
                                 (alm.x - 35, alm.y + 15 - altura_relleno, 70, altura_relleno))

            # Etiquetas de tipo y capacidad
            texto_tipo = self.fuente.render(f"{alm.tipo_grano_asignado.name}", True, (255, 255, 255))
            texto_cap = self.fuente.render(f"Cap: {alm.capacidad_max}T", True, (200, 200, 200))
            texto_cant = self.fuente.render(f"{alm.cantidad}T", True, (255, 255, 255))

            self.pantalla.blit(texto_tipo, (alm.x - 35, alm.y - 80))
            self.pantalla.blit(texto_cap, (alm.x - 35, alm.y - 60))
            self.pantalla.blit(texto_cant, (alm.x - 25, alm.y + 45))

    def dibujar_interfaz(self):
        self.pantalla.fill((50, 150, 50))
        self.dibujar_almacenes()

        # Camion (dibujo simple)
        pygame.draw.rect(self.pantalla, (200, 0, 0), (self.camion_x - 50, self.camion_y - 20, 100, 40))

        titulo = self.fuente_grande.render("GRANEROS ESPECIALIZADOS (Cap: 50T c/u)", True, (255, 255, 255))
        self.pantalla.blit(titulo, (280, 20))

        instrucciones = [
            "1: Descargar TRIGO | 2: Descargar MAIZ | 3: Descargar CEBADA",
            f"Última carga: {self.ultima_carga}T",
            f"Estado: {self.mensaje_error if self.mensaje_error else 'Listo'}"
        ]

        for i, instr in enumerate(instrucciones):
            color_texto = (255, 100, 100) if "Error" in instr or "lleno" in instr else (255, 255, 255)
            texto = self.fuente.render(instr, True, color_texto)
            self.pantalla.blit(texto, (20, 560 - i * 20))

        pygame.display.flip()

    def descargar_grano(self, tipo: TipoGrano):
        cantidad = random.choice([10, 20])
        self.ultima_carga = cantidad
        exito = False

        for alm in self.almacenes:
            if alm.tipo_grano_asignado == tipo:
                if alm.agregar(tipo, cantidad):
                    self.mensaje_error = f"Éxito: +{cantidad}T de {tipo.name}"
                    exito = True
                else:
                    self.mensaje_error = f"Error: Almacén de {tipo.name} lleno o sin espacio"
                break

        if not exito and not self.mensaje_error:
            self.mensaje_error = "Error: Tipo de grano no reconocido"

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

            self.dibujar_interfaz()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    granero = Granero()
    granero.ejecutar()
