import pygame
import sys
import math
import random


pygame.init()
clock = pygame.time.Clock()
# Postavljanje veličine prozora i naslov igre
win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("UDG Runner")


# Create the white transparent curtain
curtain = pygame.Surface((win_width, win_height), pygame.SRCALPHA)
curtain.fill((173, 216, 230, 24)) #24 predstavlja transparentnost svijetlo plave zavjese

# Postavljanje pozadine
bg = pygame.image.load("images\\background.jpg")
bg = pygame.transform.scale(bg, (win_width, win_height)) 
bg = bg.convert()
bg.set_alpha(200)

icon = pygame.image.load('images\\runner.ico')
pygame.display.set_icon(icon)

pygame.mixer.music.load('music\\11HimnaUDG.mp3')
pygame.mixer.music.play(-1) 

tinted_bg = pygame.Surface((win_width, win_height))
tinted_bg.fill((255, 255, 255))
tinted_bg.set_alpha(120)
tinted_bg.blit(bg, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
bg = tinted_bg


# Postavljanje podova
floor = pygame.image.load("images\\pod.png")
floor_width = floor.get_width() # Širina poda
floor_height = floor.get_height() # Visina poda
floor_x1 = 0 # X pozicija prvog poda
floor_x2 = floor_width # X pozicija drugog poda (odmah do prvog)
floor_y = win_height - floor_height + 100 # Y pozicija oba poda
floor_speed = 4 # Brzina kojom se pod pomjera udesno


# Prebojavanje podova u sivu boju
gray = (84, 84, 84)
floor = floor.convert_alpha() # Dodavanje alpha kanala
floor.fill(gray, special_flags=pygame.BLEND_RGBA_MULT) # Prebojavanje površine sivom bojom


# Učitavanje slika za trčanje
run_imgs = [
    pygame.image.load("images\\Run1.png"),
    pygame.image.load("images\\Run2.png"),
    pygame.image.load("images\\Run3.png")
]
# Indeks trenutne slike za trčanje
current_run_img = 0
# Brojač za promjenu slika
img_counter = 0

# Kreiranje glavnog karaktera
runner = pygame.image.load("images\\Run1.png")
runner_width = runner.get_width()
runner_height = runner.get_height()+75
runner_x = 50
runner_y = floor_y - runner_height


runner_rect = pygame.Rect(runner_x+50, runner_y-50, runner_width-10, runner_height-16)

#PREPREKA
bus = pygame.image.load('images\\bus1.png')

bus_width = bus.get_width() /2 
bus_height = (bus.get_height()+75) /2
bus_x = 400   
bus_y = floor_y - bus_height+450
bus = pygame.transform.scale(bus, (int(bus_width * 0.5), int(bus_height * 0.5)))
bus_speed = 6
bus_spawned = False
bus_spawn_point = 1000

powerup_img= pygame.image.load("images\\dojc.png")
powerup_img = pygame.image.load("images\\dojc.png").convert_alpha()
powerup_img = pygame.transform.scale(powerup_img, (50, 50))



powerup_x = random.randint(0, win_width - 50)
powerup_y = random.randint(0, win_height - 50)

powerup_rect = pygame.Rect(powerup_x+35, powerup_y+25, 50, 30)

powerup_on_screen = False



bus_rect= pygame.Rect(bus_x, bus_y, bus_width/8, bus_height/8)
    

bus_rect= pygame.Rect(bus_x, bus_y, bus_width/8, bus_height/8)





# Draw the runner on the screen
pygame.draw.rect(win, (255, 0, 0), runner_rect)

# Draw the runner on the screen
pygame.draw.rect(win, (255, 0, 0), bus_rect)


frame = 0  # trenutni frejm trkača
frame_rate = 50  # promjena frejma svakih 50 milisekundi
last_update = pygame.time.get_ticks()  # vrijeme od posljednjeg ažuriranja


# Postavite brzinu i ubrzanje trkača
runner_speed = 5
runner_acceleration = 0.45 
runner_max_speed = 10
runner_jump_speed = -11.8
runner_is_jumping = False

jump = False


# citaj highscore iz fajla
with open('highscore.txt', 'r') as f:
    high_score = float(f.read())


# definisanje end game screena
def end_screen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # izadji iz igre ako se klikne X
            game_over = True
    # Kreiraj font objekt
    font = pygame.font.SysFont('comicsans', 70)
    font2 = pygame.font.SysFont('comicsans', 40)

    
    # Kreiraj tekstualni objekat za gejm over
    game_over_text = font.render('Izgubio si!', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(win_width//2, win_height//2 - 150))

    # Create text object for score
    score_text = font2.render(f'Rezultat: {int(score)}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(win_width//2, win_height//2 - 50))

    high_score_text = font2.render("Rekord: " + str(int(high_score)), True, (255, 255, 255))

    

    # Kreiraj tekstualni objekat i uputstva za restartovanje igre
    restart_text = font2.render('Pritisni SPACE da probas opet.', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(win_width//2, win_height//2 + 150))

    background = pygame.Surface(win.get_size())
    background.fill((17, 23, 71))

    # Prikazi end game screen
    win.blit(background, (0, 0))
    win.blit(game_over_text, game_over_rect)
    win.blit(score_text, score_rect)
    win.blit(restart_text, restart_rect)
    win.blit(high_score_text, (win_width/2 - high_score_text.get_width()/2, 300))


    pygame.display.update()

game_over=False
# Glavna petlja igre
run = True
# Starting screen
show_start_screen = True
while show_start_screen:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_start_screen = False
                start_time = pygame.time.get_ticks()

    # Crtaj startni ekran
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont("comicsans", 50, True)
    # Inicijalna pozicija i amplitutda "wobble-a"
    x = 400
    y = 250
    amplitude = 10


    

    text = font.render("Pritisni SPACE da pocnes!", 1, pygame.Color("Orange"))

    # Dobij dimenzije tekstualnog objekta
    text_rect = text.get_rect()

    # Crtaj outline teksta
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
     outline_rect = text_rect.move(dx, dy)

    y += amplitude * math.sin(pygame.time.get_ticks() / 100)

    # Crtanje i renderoavnje teksta
    text_rect = text.get_rect(center=(x, y))
    pygame.draw.rect(win, (0, 0, 0), text_rect.inflate(2, 1)) 
    win.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)



score = 0  


while run:
    
 if game_over == False:
    # Obrada događaja
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            run = False

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key==pygame.K_SPACE) and not runner_is_jumping:
                # Zapocni skok
                runner_speed = runner_jump_speed
                runner_is_jumping = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if powerup_rect.collidepoint(event.pos):
                score+=1
                


    # Azuriranje pozicije trkača
    runner_y += runner_speed
    # Updateovanje skora




    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if the mouse click is within the powerup's bounding box
        if powerup_rect.collidepoint(event.pos):
            score+=0.000000000000000000000000000000000005
            powerup_x = random.randint(0,  600)
            powerup_y = random.randint(0,  400)
            powerup_rect = pygame.Rect(powerup_x, powerup_y, 40, 40)

    

    # apdejtovanje highscore-a
    if score > high_score:
        high_score = score
        with open('highscore.txt', 'w') as f:
            f.write(str(high_score))
    

    font = pygame.font.SysFont("comicsans", 30, True)




    # apdejtuj brzinu trkača (ako je u skoku)
    if runner_is_jumping:
        runner_speed += runner_acceleration
        if runner_speed > runner_max_speed:
            runner_speed = runner_max_speed

    # Ako je trkač iznad poda, vrati ga na pod
    if runner_y > floor_y - runner_height:
        runner_y = floor_y - runner_height
        runner_is_jumping = False
        runner_speed = 0


    # apdejtovanje pozicije busa
    if bus_x*3 > -bus_width:
        bus_x -= bus_speed

    # ako se bus nije spawnovao, nasumice odredi vrijeme za sledeci bus
    if not bus_spawned:
        bus_delay = 2350 # time delay in milliseconds
        bus_spawn_time = pygame.time.get_ticks() + bus_delay
        bus_spawned = True

    # ako je vrijeme da se spawnuje drugi bus, resetuj vrijeme i kreiraj objekat busa bus
    if pygame.time.get_ticks() >= bus_spawn_time:
        bus_x = bus_spawn_point
        bus_y = floor_y - bus_height + 100
        bus_rect = pygame.Rect(bus_x+10, bus_y, bus_width*0.5-5, bus_height*0.5)
        bus_spawned = False


    # Kretanje busa ka runneru
    bus_rect.x -= bus_speed 
      
    if runner_rect.colliderect(bus_rect):
     game_over=True

     if runner_rect.colliderect(bus_rect):
      powerup_on_screen=False

    # Ažuriranje igre
    floor_x1 -= floor_speed # Pomjeranje prvog poda udesno
    floor_x2 -= floor_speed # Pomjeranje drugog poda udesno
    if floor_x1 < -floor_width: # Ako se prvi pod potpuno pomakne izvan prozora, vraćamo ga na početnu poziciju
        floor_x1 = floor_x2 + floor_width
    if floor_x2 < -floor_width: # Ako se drugi pod potpuno pomakne izvan prozora, vraćamo ga na početnu poziciju
        floor_x2 = floor_x1 + floor_width

    
    img_counter += 1
    if img_counter == 10:
        current_run_img += 1
        if current_run_img > 2:
            current_run_img = 0
        img_counter = 0

    if pygame.time.get_ticks() - last_update > frame_rate:
        last_update = pygame.time.get_ticks()
        frame += 1
        if frame >= len(run_imgs): 
            frame = 0
    # Učitavanje trenutne slike za trčanje

    runner = pygame.transform.scale(run_imgs[current_run_img], (175, 175))
    # Move the runner
  
    runner_rect.y = runner_y

    # Crtež na ekranu

    win.blit(bg, (0, 0)) # Crtanje pozadine na (0, 0) poziciju u prozoru
    win.blit(curtain, (0, 0))
    win.blit(floor, (floor_x1, floor_y)) # Crtanje prvog poda na njegovoj poziciji
    win.blit(floor, (floor_x2, floor_y))
    win.blit(bus,(bus_x, bus_y))
    win.blit(runner, (runner_x, runner_y))
    score_text = font.render(f'Score: {int(score)}', True, pygame.Color("Orange"))
    high_score_text = font.render(f'Rekord: {high_score}', True, pygame.Color("Orange"))
    win.blit(score_text, (10, 10))
    win.blit(powerup_img, (powerup_x, powerup_y))



        
        
        

    ''' BLITOVI ZA RECTOVE!
    pygame.draw.rect(win, (255,0,0), bus_rect)
    pygame.draw.rect(win, (255,0,0), runner_rect)
    pygame.draw.rect(win, (255,0,0), powerup_rect)

'''

    pygame.display.update()
    pygame.time.delay(10)
 else:

    end_screen()
        
        # Cekaj igraca da restartuje igru
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Resetovanje varijabli i igrice
            game_over = False
            start_time = pygame.time.get_ticks()
            runner_y = floor_y - runner_height
            bus_x = win_width + bus_width
            score = 0
            break

# Zatvaranje igre i pygame
pygame.quit()
sys.exit()

