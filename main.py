import pygame
import time
import random

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
colors = {
    'color1': (217, 237, 146), 'color2': (181, 228, 140), 'color3': (153, 217, 140),
    'color4': (118, 200, 147), 'color5': (82, 182, 154), 'color6': (52, 160, 164),
    'color7': (22, 138, 173), 'color8': (227, 80, 83), 'color9': (208, 34, 36),
    'color10': (24, 78, 119), 'color11': (189, 31, 33), 'color12': (221, 44, 47),
    'color13': (82, 182, 154)
}

# Dimensions de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Morse Memory")

# Chargement de l'image
lebron = pygame.image.load("C:/Users/Darius/Desktop/lebron-james-jeune-nba.png")
lebron1 = pygame.transform.scale(lebron, (80, 50))

# Chemin de la police personnalisée
font_path = "C:/Users/VotreNomUtilisateur/Desktop/Holen Vintage.otf"
font_large = pygame.font.SysFont(font_path, 130)
font_small = pygame.font.SysFont(font_path, 50)

# Horloge et FPS
clock = pygame.time.Clock()

# Dictionnaire pour le code Morse
morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..'
}

# Fonction pour afficher le texte centré horizontalement
def display_text_centered(text, font, color, y_position):
    rendered_text = font.render(text, True, color)
    text_width = rendered_text.get_width()
    x_pos = (screen.get_width() - text_width) // 2
    screen.blit(rendered_text, (x_pos, y_position))

# Fonction pour afficher le texte en haut à gauche
def display_text_top_left(text, font, color, x_position, y_position):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x_position, y_position))

# Fonction pour dessiner la barre de progression
def draw_progress_bar(progress, y_position):
    pygame.draw.rect(screen, colors['color4'], (200, y_position, 400, 30))  # Barre vide
    pygame.draw.rect(screen, colors['color5'], (200, y_position, int(400 * progress), 30))  # Barre pleine

# Fonction pour vérifier la réponse
def check_answer(player_input, correct_morse):
    return player_input == correct_morse

# Fonction pour afficher l'écran d'accueil
def show_welcome_screen():
    while True:
        screen.fill(colors['color3'])
        display_text_centered("Remember the translation of the alphabet", font_small, colors['color10'], 100)
        display_text_centered("letter displayed in Morse code for the", font_small, colors['color10'], 150)
        display_text_centered("allotted time, and reproduce it", font_small, colors['color10'], 200)
        display_text_centered("Ready ?", pygame.font.Font(None, 65), colors['color8'], 300)
        display_text_centered("PRESS SPACE TO START", pygame.font.Font(None, 80), colors['color9'], 425)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Retourner pour commencer le jeu

# Fonction principale du jeu
def main_game(score):
    current_letter = random.choice(list(morse_dict.keys()))
    correct_morse = morse_dict[current_letter]
    player_input = ""
    progress = 0
    is_space_pressed = False
    start_time = None

    display_time = 3  # Temps d'affichage de la lettre
    start_display_time = time.time()

    # Affichage initial avec le compte à rebours
    while time.time() - start_display_time < display_time:
        screen.fill(colors['color3'])
        display_text_centered(f"{current_letter}", font_large, colors['color10'], 100)
        display_text_centered(f"Translation :", pygame.font.Font(None, 50), colors['color10'], 250)
        display_text_centered(f"{correct_morse}", pygame.font.Font(None, 100), colors['color10'], 330)
        remaining_time = int(display_time - (time.time() - start_display_time))
        display_text_centered(f"Time Left : {remaining_time+1}s", font_small, colors['color12'], 475)
        display_text_top_left(f"Score: {score}", pygame.font.Font(None, 70), colors['color10'], 20, 20)
        
        # Affichage de l'image à la position désirée
        screen.blit(lebron1, (205, 12))
        
        pygame.display.update()
        clock.tick(60)

    # Phase où le joueur doit entrer sa réponse
    while True:
        screen.fill(colors['color3'])
        display_text_centered(f"{current_letter}", font_large, colors['color10'], 100)
        display_text_centered(f"Translate with spacebar", font_small, colors['color10'], 300)
        display_text_centered(f"Your guess: {player_input}", font_small, colors['color10'], 375)
        draw_progress_bar(progress, 450)
        display_text_top_left(f"Score: {score}", pygame.font.Font(None, 70), colors['color10'], 20, 20)

        # Affichage de l'image dans cette phase du jeu
        screen.blit(lebron1, (205, 12))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_space_pressed = True
                if start_time is None:
                    start_time = time.time()

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if is_space_pressed:
                    press_duration = time.time() - start_time
                    start_time = None
                    is_space_pressed = False
                    player_input += "-" if press_duration >= 0.5 else "."
                    progress = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                player_input = player_input[:-1]
                progress = 0

        if is_space_pressed:
            press_duration = time.time() - start_time
            progress = min(press_duration / 0.5, 1)

        if len(player_input) == len(correct_morse):
            if check_answer(player_input, correct_morse):
                score += 3
                display_text_centered("Perfect ! You won 3 ", font_small, (0, 255, 0), 525)
                screen.blit(lebron1, (550, 510))
            else:
                score = score-1
                display_text_centered("Wrong ! You lost 1 ", font_small, (255, 0, 0), 525)
                screen.blit(lebron1, (535, 510))

            pygame.display.update()
            time.sleep(2)

            player_input = ""
            current_letter = random.choice(list(morse_dict.keys()))
            correct_morse = morse_dict[current_letter]
            start_display_time = time.time()
            break

        pygame.display.update()
        clock.tick(60)

    return score  # Retourner le score mis à jour

# Boucle principale du jeu
score = 0
show_welcome_screen()  # Afficher l'écran d'accueil avant de commencer le jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    score = main_game(score)

pygame.quit()