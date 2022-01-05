import pygame
import time
import random

class Nappi:
    '''Luodaan toimivia nappeja peliin'''

    def __init__(self, x: int, y: int, width: int, height: int,
                colour, rounding = False) -> None:
        self.rect = pygame.Rect(x,y,width, height)
        self.colour = colour
        self.active = False
        self.round = rounding
    
    def draw(self, ikkuna, tapahtuma, teksti: str) -> None:
        '''Piirtää ja aktivoi napin'''

        # Tarkastetaan kursorin paikka ja muutetaan väriä jos napilla
        mouse = pygame.mouse.get_pos()
        collide = self.rect.collidepoint(mouse)
        colour = (self.colour[0] + 20,
                 self.colour[1] + 20,
                 self.colour[2] + 20) if collide else self.colour
        


        # Napin piirtäminen ja tekstin lisääminen
        arial18 = pygame.font.SysFont('Arial', 18)
        if self.round:
            pygame.draw.rect(ikkuna,
                            colour,
                            self.rect,
                            border_top_right_radius = self.rect.height//2,
                            border_bottom_right_radius = self.rect.height//2)
        else:
            pygame.draw.rect(ikkuna,
                            colour,
                            self.rect,
                            border_radius = 4)
        
        teksti = arial18.render(teksti, True, (200, 200, 200))
        teksti_rect = teksti.get_rect(center = self.rect.center)
        ikkuna.blit(teksti, teksti_rect)
        
        # Napin aktivointi
        if tapahtuma.type == pygame.MOUSEBUTTONDOWN and collide and not self.active:
            self.active = True             

class Hahmo:
    '''Hahmo, jolla on paikka, kuva ja rect törmäysten havaitsemiseen'''
    def __init__(self, x, y, kuva: str) -> None:
        self.kuva = pygame.image.load(kuva)
        self.rect = self.kuva.get_rect()
        self.rect.x, self.rect.y = x, y
    
    def piirra(self, naytto):
        naytto.blit(self.kuva, self.rect)
        pygame.display.flip()
    
    def liiku(self, liike: list):
        self.rect.x += int(liike[0])
        self.rect.y += int(liike[1])

    def kolikko(self):
        '''Käytetään vain hahmolle kolikko!'''
        self.rect.x = random.randint(20, 620 - self.rect.width)
        self.rect.y = random.randint(40, 460 - self.rect.height)

class Peli:
    '''Pelin pääkoodi ja sen funktiot'''

    def __init__(self) -> None:
        '''Luodaan kaksi luokkamuuttujaa helpompaa käyttöä varten'''
        self.naytto = pygame.display.set_mode((640, 480))
        self.kello = pygame.time.Clock()

    def whiteout(self) -> None:
        '''Laajeneva ympyräefekti'''
        for i in range(100):
            time.sleep(0.01)
            pygame.draw.circle(self.naytto, (40, 40, 40), (320, 240), i*5)
            pygame.display.flip()

    def menu(self) -> bool:
        '''Pelin päävalikko'''

        # Alustetaan kuvat ja fontit
        robo = pygame.image.load('robo.png')
        arial32 = pygame.font.SysFont('Arial', 32)

        # Piirretään valikon tausta, kuvat ja tekstit
        pygame.draw.rect(self.naytto, (8, 8, 50), (20, 20, 600, 440), border_radius = 4)
        otsikko_rect = pygame.Rect(20, 60, 580, 80)
        pygame.draw.rect(self.naytto, (20, 20, 70), otsikko_rect,
                        border_top_right_radius = 40,
                        border_bottom_right_radius = 40)
        self.naytto.blit(robo, (450, 230))
        otsikko = arial32.render('CoinRobot', True, (200, 200, 200))
        teksti_rect = otsikko.get_rect(center = otsikko_rect.center)
        self.naytto.blit(otsikko, teksti_rect)

        # Luodaan päävalikon napit
        aloita_peli = Nappi(20, 180, 300, 60, (20, 20, 70), True)
        ohjeet = Nappi(20, 260, 300, 60, (20, 20, 70), True)
        poistu = Nappi(20, 340, 300, 60, (20, 20, 70), True)


        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    self.whiteout()
                    exit()
                
                # Piirretään ja aktivoidaan päävalikon napit
                aloita_peli.draw(self.naytto, tapahtuma, 'Aloita peli')
                ohjeet.draw(self.naytto, tapahtuma, 'Ohjeet')
                poistu.draw(self.naytto, tapahtuma, 'Sulje peli')
                pygame.display.flip()
                
                if poistu.active:
                    self.whiteout()
                    exit()
                if ohjeet.active:
                    self.whiteout()
                    return False
                if aloita_peli.active:
                    self.whiteout()
                    return True
    
    def pause(self) -> bool:
        '''Pause menun looppi'''

        # Tehdään pausemenun tausta, otsikko ja painikkeet
        arial32 = pygame.font.SysFont('Arial', 32)
        otsikko = arial32.render('Pause', True, (200, 200, 200))
        pygame.draw.rect(self.naytto, (8, 8, 50), (120, 120, 400, 200), border_radius = 4)
        self.naytto.blit(otsikko, (270, 160))
        jatka = Nappi(130, 240, 180, 60, (20, 20, 70))
        poistu = Nappi(330, 240, 180, 60, (20, 20, 70))

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    self.whiteout()
                    exit()
                jatka.draw(self.naytto, tapahtuma, 'Jatka peliä')
                poistu.draw(self.naytto, tapahtuma, 'Palaa päävalikkoon')
                pygame.display.flip()

                if poistu.active:
                    self.whiteout()
                    return True
                if jatka.active:
                    return False
    
    def ohjeet(self) -> None:
        '''Pelin ohjeet'''

        pygame.draw.rect(self.naytto, (8, 8, 50), (20, 20, 600, 440), border_radius = 4)
        poistu = Nappi(20, 340, 300, 60, (20, 20, 70), True)
        arial32 = pygame.font.SysFont('Arial', 32)
        arial18 = pygame.font.SysFont('Arial', 18)
        otsikko = arial32.render('Pelin ohjeet:', True, (200, 200, 200))
        self.naytto.blit(otsikko, (40, 40))

        teksti = [f'Pelin tarkoituksena on kerätä kolikkoja',
                 f'mahdollisimman paljon ennen kuin aika loppuu.',
                 f'Rahojen kerääminen lisää aikaa, ja mörköön',
                 f'osuminen vähentää sitä.','',
                 f'Robotti liikkuu aina hiiren kursoria kohti',
                 f'omaan rauhalliseen tahtiinsa, mutta mörön vauhti vain kasvaa!','',
                 f'Pelin ollessa kesken pääset pausemenuun Esc-näppäimestä.']
        korkeus = 100
        for rivi in teksti:
            rivi = arial18.render(rivi, True, (200, 200, 200))
            self.naytto.blit(rivi, (40, korkeus))
            korkeus += 24

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    self.whiteout()
                    exit()

                poistu.draw(self.naytto, tapahtuma, 'Päävalikkoon')
                pygame.display.flip()
                if poistu.active:
                    self.whiteout()
                    return
        
    def loppu(self, pisteet = 0) -> bool:
        # Tehdään endscreenin tausta ja otsikko
        arial32 = pygame.font.SysFont('Arial', 32)
        arial24 = pygame.font.SysFont('Arial', 24)
        otsikko = arial32.render('Aika loppui!', True, (200, 200, 200))
        pisteet = arial24.render(f'Pisteet: {pisteet}', True, (200, 200, 200))
        
        # Piirretään valikon tausta ja tekstit
        pygame.draw.rect(self.naytto, (8, 8, 50), (20, 20, 600, 440), border_radius = 4)
        otsikko_tausta = pygame.Rect(20, 100, 580, 70)
        pisteet_tausta = pygame.Rect(20, 180, 580, 50)
        pygame.draw.rect(self.naytto, (20, 20, 70), otsikko_tausta,
                        border_top_right_radius = 40,
                        border_bottom_right_radius = 40)
        pygame.draw.rect(self.naytto, (20, 20, 70), pisteet_tausta,
                        border_top_right_radius = 35,
                        border_bottom_right_radius = 35)
        otsikko_rect = otsikko.get_rect(center = otsikko_tausta.center)
        pisteet_rect = otsikko.get_rect(center = pisteet_tausta.center)
        self.naytto.blit(otsikko, otsikko_rect)
        self.naytto.blit(pisteet, pisteet_rect)

        # Tehdään valikon napit
        uusi_peli = Nappi(60, 320, 240, 60, (20, 20, 70))
        poistu = Nappi(320, 320, 240, 60, (20, 20, 70))
        pygame.display.flip()

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    self.whiteout()
                    exit()
                
            # Piirretään ja aktivoidaan päävalikon napit
                uusi_peli.draw(self.naytto, tapahtuma, 'Uusi peli')
                poistu.draw(self.naytto, tapahtuma, 'Palaa päävalikkoon')
                pygame.display.flip()

            pygame.display.flip()
            if poistu.active:
                self.whiteout()
                return True
            if uusi_peli.active:
                self.whiteout()
                return False

    def aikapalkki(self, ajastin) -> None:
        palkki_reuna = pygame.Rect(20, 5, 520, 30)
        palkki_inner = pygame.Rect(23, 8, 514, 24)
        palkki = pygame.Rect(26, 11, ajastin * (508 / 1800), 18)
        pygame.draw.rect(self.naytto, (0, 180, 200), palkki_reuna,
                        border_radius = 15)
        pygame.draw.rect(self.naytto, (40, 40, 40), palkki_inner,
                        border_radius = 12)
        pygame.draw.rect(self.naytto, (0, 180, 200), palkki,
                        border_radius = 9)

    def robon_liike(self, robo: Hahmo, kohde: tuple) -> list:
        liike = []
        kohde_x, kohde_y = kohde
        if robo.rect.x > kohde_x and robo.rect.x > 20:
            liike.append(-1)
        elif robo.rect.x < kohde_x and robo.rect.x < 620 - robo.rect.width:
            liike.append(1)
        else:
            liike.append(0)
        if robo.rect.y > kohde_y and robo.rect.y > 40:
            liike.append(-1)
        elif robo.rect.y < kohde_y and robo.rect.y < 460 - robo.rect.height:
            liike.append(1)
        else:
            liike.append(0)
        return liike

    def moron_liike(self, morko: Hahmo, nopeus: list):
        x = nopeus[0]
        y = nopeus[1]
        if x < 0 and morko.rect.x <= 20 or x > 0 and morko.rect.x + morko.rect.width >= 620:
            x *= -1
        if y < 0 and morko.rect.y <= 40 or y > 0 and morko.rect.y + morko.rect.height >= 460:
            y *= -1
        return [x, y]

    def peli(self) -> None:
        '''Itse peliä pyörittävä looppi'''
        
        # Luodaan hahmot 
        robo = Hahmo(100, 220, 'robo.png')
        morko = Hahmo(500, 220, 'hirvio.png')
        kolikko = Hahmo(0, 0, 'kolikko.png')
        kolikko.kolikko()

        pisteet = 0
        ajastin = 1800
        morossa = False
        kohde = pygame.mouse.get_pos()
        arial18 = pygame.font.SysFont('Arial', 18)

        def morolle_suunta():
            satunnaisluku = random.uniform(1.2, 1.8)
            return [satunnaisluku, 3 - satunnaisluku]
        
        moron_suunta = morolle_suunta()

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    self.whiteout()
                    exit()
                if tapahtuma.type == pygame.MOUSEMOTION:
                    kohde = (tapahtuma.pos[0] - robo.rect.width / 2,
                            tapahtuma.pos[1] - robo.rect.height / 2)
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        if self.pause():    # True keskeyttää pelin, False jatkaa
                            return

            # Hahmojen liikkeen laskeminen
            moron_kerroin = 1 + pisteet / 10
            moron_suunta = self.moron_liike(morko, moron_suunta)
            robo.liiku(self.robon_liike(robo, kohde))
            morko.liiku([float(f'{i * moron_kerroin:.02f}') for i in moron_suunta])

            # Piirretään kaikki näytölle tulevat asiat
            pygame.draw.rect(self.naytto, (0, 50, 100), (20, 40, 600, 420), border_radius = 4)
            pistelaskuri = arial18.render(f'Pisteet: {pisteet}', True, (200, 200, 200))
            pl_tausta = pistelaskuri.get_rect()
            pl_tausta.x, pl_tausta.y = (542, 5)
            pygame.draw.rect(self.naytto, (40, 40, 40), pl_tausta)
            self.naytto.blit(pistelaskuri, (542, 5))
            kolikko.piirra(self.naytto)
            robo.piirra(self.naytto)
            morko.piirra(self.naytto)
            
            # Tarkastetaan robotin osumat
            if robo.rect.colliderect(kolikko.rect):
                ajastin += 300
                if ajastin > 1800:
                    ajastin = 1800
                pisteet += 1
                kolikko.kolikko()
                if pisteet%5 == 0:
                    moron_suunta = morolle_suunta()
            
            if not robo.rect.colliderect(morko.rect):
                morossa = False
            
            if robo.rect.colliderect(morko.rect) and morossa == False:
                morossa = True
                ajastin -= 300
                if ajastin < 0:
                    ajastin = 1

            pygame.display.flip()
            self.kello.tick(60)
            
            # Aikapalkki
            ajastin -= 1
            if ajastin <= 0:
                self.aikapalkki(ajastin)
                time.sleep(0.3)
                self.whiteout()
                lopetus = self.loppu(pisteet)
                if not lopetus:
                    self.peli()
                else:
                    return
            else:
                self.aikapalkki(ajastin)

    def run(self) -> None:
        '''Aloittaa pelin'''

        # Alustetaan pygame pelille
        pygame.init()
        self.naytto.fill((40, 40, 40))
        pygame.display.set_caption('CoinRobot')
        
        # Pelin ja valikoiden ajolooppi
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    self.whiteout()
                    exit()
            
                aloita = self.menu()
                if aloita:
                    self.peli()
                if not aloita:
                    self.ohjeet()

def main() -> None:
    peli = Peli()
    peli.run()

if __name__ == '__main__':
    main()