import pygame
import time
import random
import csv

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

# Polices de caractères
font_large = pygame.font.Font(None, 70)
font_small = pygame.font.Font(None, 50)

# Horloge et FPS
clock = pygame.time.Clock()

# Dictionnaire pour le code Morse
morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..'
}

# Fonctions utilitaires
def display_text_centered(text, font, color, y_position):
    rendered_text = font.render(text, True, color)
    text_width = rendered_text.get_width()
    x_pos = (screen.get_width() - text_width) // 2
    screen.blit(rendered_text, (x_pos, y_position))

def display_text_top_left(text, font, color, x_position, y_position):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x_position, y_position))

def draw_progress_bar(progress, y_position):
    pygame.draw.rect(screen, colors['color4'], (200, y_position, 400, 30))
    pygame.draw.rect(screen, colors['color5'], (200, y_position, int(400 * progress), 30))

def check_answer(player_input, correct_morse):
    return player_input == correct_morse

def adjust_lebron_position(score):
    return 205 if score < 10 else 231

# Gestion des joueurs
def load_player_data():
    players = {}
    try:
        with open('player_scores.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    players[row[0]] = int(row[1])
    except FileNotFoundError:
        pass
    return players

def save_player_data(players):
    with open('player_scores.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for player, best_score in players.items():
            writer.writerow([player, best_score])

# Fonction pour afficher la page des stats
def show_stats_page(players):
    while True:
        screen.fill(colors['color3'])
        display_text_centered("Stats", font_large, colors['color10'], 100)
        y_position = 200
        for player, best_score in players.items():
            display_text_top_left(f"{player}: {best_score} points", pygame.font.Font(None, 50), colors['color10'], 100, y_position)
            y_position += 60
        display_text_centered("Press M to go back", font_small, colors['color10'], 400)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Retourner au menu
                    show_start_page()
                    return
                
# Fonction pour afficher la page des niveaux débloqués
def show_levels_page():
    while True:
        screen.fill(colors['color3'])
        display_text_centered("Niveaux Débloqués", font_large, colors['color10'], 100)
        display_text_centered("Your unlocked levels will appear here.", font_small, colors['color10'], 250)
        display_text_centered("Press M to go back", font_small, colors['color10'], 400)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Vérifie si la souris est sur le bouton Play
                    show_start_page()  # Affiche la page d'explication
                    return

# Pages du jeu
def show_start_page():
    play_button_rect = pygame.Rect(300, 310, 200, 50)
    stats_button_rect = pygame.Rect(300, 370, 200, 50)
    levels_button_rect = pygame.Rect(225, 430, 350, 50)

    players = load_player_data()

    while True:
        screen.fill(colors['color3'])
        display_text_centered("Welcome to Morse Memory!", font_large, colors['color10'], 100)
        display_text_centered("Click Play to Start", font_small, colors['color10'], 215)

        pygame.draw.rect(screen, colors['color9'], play_button_rect)
        pygame.draw.rect(screen, colors['color9'], stats_button_rect)
        pygame.draw.rect(screen, colors['color9'], levels_button_rect)

        display_text_centered("Play", font_small, colors['color1'], 318)
        display_text_centered("Stats", font_small, colors['color1'], 380)
        display_text_centered("Niveaux Débloqués", font_small, colors['color1'], 440)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    player_name = show_name_input_page()
                    return player_name, players
                if stats_button_rect.collidepoint(event.pos):
                    show_stats_page(players)
                if levels_button_rect.collidepoint(event.pos):
                    show_levels_page()

def show_name_input_page():
    player_name = ""
    font = pygame.font.Font(None, 50)
    input_box = pygame.Rect(200, 250, 400, 50)
    active = False
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    while True:
        screen.fill(colors['color3'])
        display_text_centered("Enter your name", font, colors['color10'], 100)
        pygame.draw.rect(screen, color, input_box, 2)
        display_text_centered(player_name, font, colors['color10'], 260)
        display_text_centered("Press Enter to continue", font, colors['color10'], 350)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and player_name:
                        return player_name
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

# Fonction principale du jeu
def main_game(score, player_name, players):
    current_letter = random.choice(list(morse_dict.keys()))
    correct_morse = morse_dict[current_letter]
    player_input = ""
    progress = 0
    is_space_pressed = False
    start_time = None

    display_time = 3  # Temps d'affichage de la lettre
    start_display_time = time.time()

    # Phase d'affichage de la lettre
    while time.time() - start_display_time < display_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                action = pause_game()
                if action == "main_menu":
                    return score, players  # Retourner uniquement score et players

        screen.fill(colors['color3'])
        display_text_centered(f"{current_letter}", font_large, colors['color10'], 100)
        display_text_centered(f"Translation :", pygame.font.Font(None, 50), colors['color10'], 250)
        display_text_centered(f"{correct_morse}", pygame.font.Font(None, 100), colors['color10'], 330)
        remaining_time = int(display_time - (time.time() - start_display_time))
        display_text_centered(f"Time Left : {remaining_time+1}s", font_small, colors['color12'], 475)
        display_text_top_left(f"Score: {score}", pygame.font.Font(None, 70), colors['color10'], 20, 20)
        screen.blit(lebron1, (adjust_lebron_position(score), 12))
        pygame.display.update()
        clock.tick(60)

    # Phase d'entrée du joueur
    while True:
        screen.fill(colors['color3'])
        display_text_centered(f"{current_letter}", font_large, colors['color10'], 100)
        display_text_centered(f"Translate with spacebar", font_small, colors['color10'], 300)
        display_text_centered(f"Your guess: {player_input}", font_small, colors['color10'], 375)
        draw_progress_bar(progress, 450)
        display_text_top_left(f"Score: {score}", pygame.font.Font(None, 70), colors['color10'], 20, 20)
        screen.blit(lebron1, (adjust_lebron_position(score), 12))

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                action = pause_game()
                if action == "main_menu":
                    return score, players  # Retourner uniquement score et players

        if is_space_pressed:
            press_duration = time.time() - start_time
            progress = min(press_duration / 0.5, 1)

        if len(player_input) == len(correct_morse):
            screen.fill(colors['color3'])
            display_text_centered(f"{current_letter}", font_large, colors['color10'], 100)
            display_text_centered(f"Translate with spacebar", font_small, colors['color10'], 300)
            display_text_centered(f"Your guess: {player_input}", font_small, colors['color10'], 375)
            draw_progress_bar(progress, 450)
            display_text_top_left(f"Score: {score}", pygame.font.Font(None, 70), colors['color10'], 20, 20)
            screen.blit(lebron1, (adjust_lebron_position(score), 12))
            pygame.display.update()

            if check_answer(player_input, correct_morse):
                score += 3
                display_text_centered("Perfect! You won 3 points", font_small, (128, 185, 24), 525)
            else:
                # Mettre à jour le best_score avant de réinitialiser
                if player_name in players:
                    if score > players[player_name]:  # Vérifier si le score actuel dépasse le best_score
                        players[player_name] = score
                else:
                    players[player_name] = score  # Nouveau joueur avec son best_score initial

                score = 0  # Réinitialiser le score en cas d'erreur
                display_text_centered("Wrong! Score reset to 0", font_small, colors['color9'], 525)

            pygame.display.update()
            time.sleep(2)

            # Mise à jour du meilleur score pour le joueur
            if player_name in players:
                if score > players[player_name]:  # Si le score du joueur est meilleur que le précédent
                    players[player_name] = score
            else:
                players[player_name] = score  # Nouveau joueur avec son score

            player_input = ""
            current_letter = random.choice(list(morse_dict.keys()))
            correct_morse = morse_dict[current_letter]
            start_display_time = time.time()
            break

        pygame.display.update()
        clock.tick(60)

    return score, players  # Retourne uniquement score et players

# Boucle principale
players = load_player_data()
while True:
    player_name, players = show_start_page()
    score = 0
    while True:
        score, players = main_game(score, player_name, players)
        if score == "menu":
            break