import pygame
import random
import os

# Inisialisasi Pygame
pygame.init()

# --- Konfigurasi Layar ---
lebar_layar = 800
tinggi_layar = 600
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Game Tembak-tembakan Sederhana")

# --- Warna ---
hitam = (0, 0, 0)
putih = (255, 255, 255)
merah = (255, 0, 0)
hijau = (0, 255, 0)
biru = (0, 0, 255)

# --- Kelas Pemain (Player) ---
class Pemain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 40])
        self.image.fill(hijau)
        self.rect = self.image.get_rect()
        self.rect.centerx = lebar_layar // 2
        self.rect.bottom = tinggi_layar - 10
        self.kecepatan = 5

    def update(self):
        tekanan_tombol = pygame.key.get_pressed()
        if tekanan_tombol[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.kecepatan
        if tekanan_tombol[pygame.K_RIGHT] and self.rect.right < lebar_layar:
            self.rect.x += self.kecepatan

    def tembak(self):
        peluru = Peluru(self.rect.centerx, self.rect.top)
        semua_sprite.add(peluru)
        peluru_group.add(peluru)

# --- Kelas Musuh (Enemy) ---
class Musuh(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(merah)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(lebar_layar - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.kecepatan_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.kecepatan_y
        if self.rect.top > tinggi_layar:
            self.rect.x = random.randrange(lebar_layar - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.kecepatan_y = random.randrange(1, 8)

# --- Kelas Peluru (Bullet) ---
class Peluru(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(putih)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.kecepatan_y = -10

    def update(self):
        self.rect.y += self.kecepatan_y
        if self.rect.bottom < 0:
            self.kill()

# --- Kelompok Sprite ---
semua_sprite = pygame.sprite.Group()
musuh_group = pygame.sprite.Group()
peluru_group = pygame.sprite.Group()

# Buat Pemain
pemain = Pemain()
semua_sprite.add(pemain)

# Buat Musuh
for _ in range(8):
    musuh = Musuh()
    semua_sprite.add(musuh)
    musuh_group.add(musuh)

# --- Game Loop ---
berjalan = True
jam = pygame.time.Clock()

while berjalan:
    # Mengatur FPS
    jam.tick(50)

    # --- Proses Event ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                pemain.tembak()

    # --- Update ---
    semua_sprite.update()

    # Cek tabrakan antara peluru dan musuh
    tabrakan = pygame.sprite.groupcollide(musuh_group, peluru_group, True, True)
    for hit in tabrakan:
        musuh = Musuh()
        semua_sprite.add(musuh)
        musuh_group.add(musuh)

    # --- Gambar ---
    layar.fill(hitam)
    semua_sprite.draw(layar)

    # Update tampilan
    pygame.display.flip()

pygame.quit()