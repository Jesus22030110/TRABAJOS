import pygame
import sys
from enum import Enum
from dataclasses import dataclass

class TipoGrano(Enum):
    TRIGO = 1
    MAIZ = 2
    CEBADA = 3

@dataclass
class Almacen:
    capacidad_max: int
    tipo_grano: TipoGrano = None
    cantidad: int = 0
    x: int = 0
    y: int = 0
    
    def puede_agregar(self, tipo: TipoGrano, cantidad: int) -> bool:
        if self.cantidad == 0:
            return cantidad <= self.capacidad_max
        return self.tipo_grano == tipo and (self.cantidad + cantidad) <= self.capacidad_max
    
    def agregar(self, tipo: TipoGrano, cantidad: int) -> bool:
        if self.puede_agregar(tipo, cantidad):
            self.tipo_grano = tipo
            self.cantidad += cantidad
            return True
        return False

class Granero:
    def __init__(self, ancho=1000, alto=600):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Sistema de Granero - Descarga de Granos")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 20)
        self.fuente_grande = pygame.font.Font(None, 30)
        
        self.almacenes = [
            Almacen(10, x=150, y=200),
            Almacen(20, x=450, y=200),
            Almacen(10, x=750, y=200)
        ]
        
        self.camion_x = 500
        self.camion_y = 450
        self.capacidad_total = 50
        self.carga_actual = 0
        self.tipo_descargando = None
        self.cantidad_descargando = 0
        self.almacen_actual = -1
        self.en_descarga = False
        self.tiempo_descarga = 0
        
        self.historial = []
        self.corriendo = True
    
    def dibujar_almacenes(self):
        colores = {TipoGrano.TRIGO: (220, 180, 0), TipoGrano.MAIZ: (180, 120, 0), TipoGrano.CEBADA: (100, 80, 50)}
        
        for i, alm in enumerate(self.almacenes):
            # Marco del almacén
            pygame.draw.rect(self.pantalla, (100, 100, 100), (alm.x - 40, alm.y - 40, 80, 80), 2)
            
            # Relleno según carga
            if alm.cantidad > 0:
                altura_relleno = int((alm.cantidad / alm.capacidad_max) * 60)
                color = colores[alm.tipo_grano]
                pygame.draw.rect(self.pantalla, color, (alm.x - 35, alm.y + 15 - altura_relleno, 70, altura_relleno))
            
            # Etiquetas
            texto_cap = self.fuente.render(f"Cap: {alm.capacidad_max}T", True, (255, 255, 255))
            texto_cant = self.fuente.render(f"{alm.cantidad}T", True, (255, 255, 255))
            self.pantalla.blit(texto_cap, (alm.x - 35, alm.y - 60))
            self.pantalla.blit(texto_cant, (alm.x - 25, alm.y + 45))
    
    def dibujar_camion(self):
        # Cuerpo del camión
        pygame.draw.rect(self.pantalla, (200, 0, 0), (self.camion_x - 50, self.camion_y - 20, 100, 40))
        # Ruedas
        pygame.draw.circle(self.pantalla, (0, 0, 0), (self.camion_x - 30, self.camion_y + 25), 8)
        pygame.draw.circle(self.pantalla, (0, 0, 0), (self.camion_x + 30, self.camion_y + 25), 8)
        # Cabina
        pygame.draw.polygon(self.pantalla, (100, 0, 0), [(self.camion_x + 50, self.camion_y - 20), (self.camion_x + 70, self.camion_y - 20), (self.camion_x + 65, self.camion_y + 20)])
        
        texto = self.fuente.render(f"Carga: {self.carga_actual}T", True, (255, 255, 255))
        self.pantalla.blit(texto, (self.camion_x - 40, self.camion_y - 50))
    
    def dibujar_interfaz(self):
        self.pantalla.fill((50, 150, 50))
        self.dibujar_almacenes()
        self.dibujar_camion()
        
        titulo = self.fuente_grande.render("SISTEMA DE GRANERO", True, (255, 255, 255))
        self.pantalla.blit(titulo, (350, 20))
        
        # Instrucciones
        instrucciones = [
            "1: Descargar TRIGO (5T) | 2: Descargar MAIZ (8T) | 3: Descargar CEBADA (7T)",
            f"Capacidad total granero: {sum(a.cantidad for a in self.almacenes)}/{self.capacidad_total}T"
        ]
        
        for i, instr in enumerate(instrucciones):
            texto = self.fuente.render(instr, True, (255, 255, 255))
            self.pantalla.blit(texto, (20, 550 - i*25))
        
        pygame.display.flip()
    
    def descargar_grano(self, tipo: TipoGrano, cantidad: int):
        cantidad = int(cantidad)
        
        if sum(a.cantidad for a in self.almacenes) + cantidad > self.capacidad_total:
            print(f"❌ No hay espacio en el granero")
            return
        
        for alm in self.almacenes:
            if alm.agregar(tipo, cantidad):
                print(f"✓ Descargados {cantidad}T de {tipo.name} en almacén")
                self.historial.append(f"{tipo.name}: {cantidad}T")
                return
        
        print(f"❌ No hay almacén disponible para {tipo.name}")
    
    def ejecutar(self):
        while self.corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.descargar_grano(TipoGrano.TRIGO, 5)
                    elif evento.key == pygame.K_2:
                        self.descargar_grano(TipoGrano.MAIZ, 8)
                    elif evento.key == pygame.K_3:
                        self.descargar_grano(TipoGrano.CEBADA, 7)
            
            self.dibujar_interfaz()
            self.reloj.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    granero = Granero()
    granero.ejecutar()