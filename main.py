import pygame
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

all_sprites = pygame.sprite.Group()


def load_image(name):
    fullname = f'data/{name}'
    image = pygame.image.load(fullname)
    return image


def load_mp(filename):
    # absolute path
    url = QUrl.fromLocalFile(os.path.abspath(f'data/{filename}'))
    content = QMediaContent(url)
    player = QMediaPlayer()
    player.setMedia(content)
    return player


class StartPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.player.play()

    def initUi(self):
        self.resize(625, 730)
        self.setWindowTitle('Galaxy Warrior')

        self.pixmap = QPixmap('data/start_background.jpg')
        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 625, 730)
        self.back.setPixmap(self.pixmap)

        self.title = QLabel('Welcome to the "Galaxy Warrior"!', self)
        self.title.setGeometry(100, 90, 441, 41)
        self.title.setStyleSheet('font: 30pt Standard;')

        self.lvl1 = QPushButton('Level1', self)
        self.lvl1.setGeometry(240, 210, 141, 51)
        self.lvl1.setStyleSheet('font: 30pt Standard; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);')

        self.lvl2 = QPushButton('Level2', self)
        self.lvl2.setGeometry(240, 290, 141, 51)
        self.lvl2.setStyleSheet('font: 30pt Standard; background-color: rgb(0, 0, 255);')

        self.boss = QPushButton('BOSS', self)
        self.boss.setGeometry(240, 370, 141, 51)
        self.boss.setStyleSheet('font: 30pt Standard; color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);')

        self.manual = QPushButton('Manual', self)
        self.manual.setGeometry(240, 500, 141, 51)
        self.manual.setStyleSheet('font: 30pt Standard;')

        self.manual_page = Manual()

        self.lvl1.clicked.connect(self.level1)
        self.lvl2.clicked.connect(self.level2)
        self.boss.clicked.connect(self.boss_game)
        self.manual.clicked.connect(self.man)

        self.player = load_mp('music.mp3')
        self.player.play()

    def man(self):
        self.manual_page.show()

    def level1(self):
        self.player.stop()
        self.close()
        GameWindow()

    def level2(self):
        self.f = FinishPage()
        self.f.show()
        self.player.stop()
        self.close()

    def boss_game(self):
        pass


class GameWindow:
    def __init__(self):
        super().__init__()
        self.sprites_init()
        self.main()

    def main(self):
        pygame.init()

        size = width, height = (690, 910)
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        pygame.display.set_caption('Galaxy Warrior')

        my_font = pygame.font.SysFont('Standard', 40)
        score_txt = my_font.render('SCORE:  0', False, (255, 255, 255))

        k = 20
        surf = pygame.Surface((650, 790))
        # pygame.mouse.set_visible(False)
        back = pygame.transform.scale(load_image('background.jpg'), (650, 790))

        surf.blit(back, (0, 0))
        pygame.draw.line(surf, 'white', (0, 0), (649, 0), 1)
        pygame.draw.line(surf, 'white', (649, 0), (649, 789), 1)
        pygame.draw.line(surf, 'white', (0, 789), (649, 789), 1)
        pygame.draw.line(surf, 'white', (0, 0), (0, 789), 1)

        ship = Ship(all_sprites)
        running = True
        while running:
            all_sprites.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    all_sprites.update(event.pos, event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Fire(all_sprites)
                        all_sprites.update(ship.rect, event)

            screen.fill((0, 0, 30))
            screen.blit(surf, (k, 100))
            screen.blit(score_txt, (40, 45))
            all_sprites.draw(screen)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

    def sprites_init(self):
        img = pygame.transform.scale(load_image('life.png'), (60, 50))

        life1 = pygame.sprite.Sprite()
        life1.image = img
        life1.rect = life1.image.get_rect()
        life1.rect.x = 590
        life1.rect.y = 30

        life2 = pygame.sprite.Sprite()
        life2.image = img
        life2.rect = life2.image.get_rect()
        life2.rect.x = 520
        life2.rect.y = 30

        life3 = pygame.sprite.Sprite()
        life3.image = img
        life3.rect = life3.image.get_rect()
        life3.rect.x = 450
        life3.rect.y = 30

        ship = pygame.sprite.Sprite()
        ship.image = pygame.transform.scale(load_image('ship.png'), (100, 100))
        ship.rect = ship.image.get_rect()
        ship.rect.x = 300
        ship.rect.y = 750

        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.transform.scale(load_image('enemy.png'), (100, 100))
        enemy.rect = ship.image.get_rect()
        enemy.rect.x = 300
        enemy.rect.y = 300

        all_sprites.add(life1)
        all_sprites.add(life2)
        all_sprites.add(life3)
        # all_sprites.add(ship)
        # all_sprites.add(enemy)


class Ship(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('ship.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 750

    def update(self, pos=(300, 750), *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            if pos[0] < 70:
                self.rect.x = 20
            elif pos[0] >= 620:
                self.rect.x = 569
            else:
                self.rect.x = pos[0] - 50


class Fire(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('fire.png'), (40, 60))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Fire.image
        self.rect = self.image.get_rect()

        # self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos=None, *args):
        if args and '768-KeyDown' in str(args[0]) and pos:
            self.rect.x = pos[0] + 30
            self.rect.y = pos[1] - 60
        self.rect = self.rect.move(0, -5)
        if self.rect.y < 95:
            self.rect.x = -100


class Manual(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(600, 400, 300, 300)
        self.setWindowTitle('Manual')
        self.label = QLabel(self)
        self.label.setGeometry(-15, 0, 420, 260)
        self.label.setText('''        RULES:
        
        You play for the space ship that has to 
        defend from a group of asteroids.
        
        By moving your mouse horizontally you 
        can control the position of your ship.
        
        By pressing "SPACE" you can 
        shoot and destroy asteroids. 
        
                                 Stay alive!''')
        self.label.setStyleSheet('font: 15pt Standard')

        self.close_btn = QPushButton('Close', self)
        self.close_btn.setGeometry(100, 250, 100, 40)
        self.close_btn.setStyleSheet('font: 20pt Standard')
        self.close_btn.clicked.connect(self.terminate)

    def terminate(self):
        self.close()


class FinishPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(625, 730)
        self.setWindowTitle('Galaxy Warrior')

        self.pixmap = QPixmap('data/end_background.jpg')
        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 625, 730)
        self.back.setPixmap(self.pixmap)

        self.title = QLabel('GAME OVER!', self)
        self.title.setGeometry(90, 50, 500, 65)
        self.title.setStyleSheet('font: 80pt Standard; color: rgb(255, 0, 0)')

        self.finish_btn = QPushButton('Quit', self)
        self.finish_btn.setGeometry(330, 600, 150, 70)
        self.finish_btn.setStyleSheet('font: 30pt Standard')

        self.restart_btn = QPushButton('Restart', self)
        self.restart_btn.setGeometry(150, 600, 150, 70)
        self.restart_btn.setStyleSheet('font: 30pt Standard')

        self.finish_btn.clicked.connect(self.finish)
        self.restart_btn.clicked.connect(self.restart_game)

        self.player = load_mp('fail.mp3')
        self.player.play()

    def finish(self):
        self.close()

    def restart_game(self):
        self.player.stop()
        self.close()
        ex.show()
        ex.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartPage()
    ex.show()
    sys.exit(app.exec())
