import random
from colorama import Fore
import save_score


class Cell:
    def __init__(self):
        """ construit et initialise un objet de classe Cell possédant tro#is attributs :
- value, qui prend les valeurs  :
    * -1 si la cellule possède une bombe ;
    * sinon un entier de 0 à 8 représentant le nombre de bombes dans les cases vosines.
- flag, un booléen représentant le fait qu'une cellule possède un drapeau ou non ;
- covered : un booléen représentant une case couverte ou découverte.
        """
        self.value = 0
        self.flag = False
        self.covered = True

def timing():
    import time
    first_time = time.time()
    final_time = time.time()
    def dif_time():
        final_time = time.time()
        dif_time_s = final_time - first_time
        formated_time = f'{dif_time_s//60}min {round(dif_time_s%60, 2)}s'
        return formated_time
    def score_time():
        return round(final_time - first_time, 2)
    return dif_time, score_time

def init_grid(taille: int):
    """ Crée et renvoie une grille carré de dimension taille*taille
    dont chaque cellule est un objet de classe Cell, et renvoie cette grille sous la forme d'une liste de listes."""
    return [[Cell() for _ in range(taille)] for _ in range(taille)]


def compute_cell(grid: list[list[Cell]], x: int, y: int):
    """ Fonction mettant à jour et renvoyant la valeur d'une cellule ne comportant pas de bombes en fonction
du nombre de cases voisines comportant des bombes
Exemples sur la grille | 0 | -1 | -1 |
                       | 0 |  0 |  0 |
                       | 0 |  0 | -1 |
>>> grid = init_grid(3)
>>> grid[0][1].value = -1
>>> grid[0][2].value = -1
>>> grid[2][2].value = -1 
>>> compute_cell(grid, 1, 1)
3
>>> compute_cell(grid, 1, 0)
1
>>> compute_cell(grid, 0, 0)
1
>>> compute_cell(grid, 2, 0)
0
>>> compute_cell(grid, 1, 2)
3
>>> compute_cell(grid, 2, 2)
-1
    """
    size = len(grid)
    if grid[x][y].value == -1:
        return -1
    count = 0
    for right_or_left in range(max(0, x-1), min(x+2, size)):
        for up_or_down in range(max(0, y-1), min(y+2, size)):
            if grid[right_or_left][up_or_down].value == -1:
                count += 1
    grid[x][y].value = count
    return count


def make_grid(grid: list[list[Cell]], nb_bombes: int):
    """ fonction créant une grille avec nb_bombes bombes dissimulées et placées aléatoirement, et mettant à jour les valeurs de toutes les cases
Non testable avec doctest.
Attention, on ne doit pas placer une bombe sur une case déjà occupée par une autre bombe.
Cette fonction ne renvoie rien, puisqu'elle modifie la grille existante (mutabilité des listes en Python). 
    """
    max_i_lines_cols = len(grid) - 1
    for _ in range(nb_bombes):
        bomb = True
        while (bomb):
            i_x, i_y = random.randint(
                0, max_i_lines_cols), random.randint(0, max_i_lines_cols)
            bomb = grid[i_x][i_y].value == -1
            grid[i_x][i_y].value = -1
    for x in range(taille):
        for y in range(taille):
            compute_cell(grid, x, y)


def affichegrid(grid: list[list[Cell]], time, colors=False, detonate=False):
    """ fonction traçant la grille dans la console
Si l'argument colors est True, alors certaines cases sont colorées :
- en vert lorsque le joueur agagné, on représente les bombes ;
- en rouge : lorsque le joueur a perdu, non seukement on représente les bombes mais aussi les drapeaux mal placés.
L'argument detonate permet de savoir si le joueur a perdu.
Non testatble dans doctest.
La fonction ne renvoie rien, et ne modifie pas la grille. Elle ne fait qu'afficher.
    """

    grid_len = len(grid)
    to_print = f"Timer : {time()}\n   "
    for i in range(grid_len):
        to_print = to_print + "     " + str(i)
    print(to_print)

    for line in range(grid_len):
        to_print = "     "
        if line == 0:
            for col in range(grid_len):
                to_print = to_print + "______"
            print(to_print)

        to_print = "     "
        for col in range(grid_len):
            to_print = to_print + "|     "
        print(to_print + "|")

        to_print = "  " + chr(line + ord('A')) + "  "
        for col in range(grid_len):
            cell_char = ""
            if detonate and colors and grid[line][col].value == -1:
                cell_char = Fore.RED + "◕" + Fore.WHITE
            elif detonate and colors and grid[line][col].flag and grid[line][col].value != -1:
                cell_char = Fore.RED + "f" + Fore.WHITE
            elif colors and grid[line][col].flag:
                cell_char = Fore.GREEN + "◕" + Fore.WHITE
            elif grid[line][col].flag:
                cell_char = "f"
            elif grid[line][col].covered:
                cell_char = "◘"
            elif grid[line][col].value == 0:
                cell_char = " "
            else:
                cell_char = str(grid[line][col].value)
            to_print = to_print + "|  " + cell_char + "  "
        print(to_print + "|")

        to_print = "     "
        for col in range(grid_len):
            to_print = to_print + "|_____"
        print(to_print + '|')
    print()


def ask_position(grid: list[list[Cell]]):
    """ Fonction dumbProof demandant au joueur une position sous la forme suivante :
soit du type A3, B4, C0, etc... où la lettre représente l'indice de ligne (A=0, B=1, ...), et le chiffre l'indice de colonne.
    Une telle saisie découvre la case à laquelle elle fait référence.
soit du type fA5, fB6, etc... (donc comme ci-dessus, mais précédé d'un f) : place un drapeau sur la case correspondante.

La fonction renvoie un tuple de la forme (flag, x, y) où :
- flag est un booléen (drapeau ou non) ;
- x est un entier représentant l'indice de la ligne visée ;
- y est un entier représentant l'indice de la colonne visée;


Ainsi sur une grille de taille 5:
    - une saiie de type F3 ou B7 est invalide et doit être recommencée, tout comme une saisie de type 0B
    - la saisie fB3 renvoie le tuple (True, 1, 3)
    - la saisie E0 renvoie le tuple (False, 4, 0)

Non testable par doctest
"""
    size = len(grid)
    while True:
        position = input("Entrez une position: ")
        if len(position) < 2 or len(position) > 3:
            print("Saisie invalide. Réessayez.")
            continue
        flag = False
        if position[0] == 'f':
            flag = True
            position = position[1:]
        if not position[0].isalpha() or not position[1].isdigit():
            print("Saisie invalide. Réessayez.")
            continue
        letter_val = ord(position[0].upper()) - ord('A')
        num_val = int(position[1])
        if letter_val < 0 or letter_val >= size or num_val < 0 or num_val >= size:
            print("Saisie invalide. Réessayez.")
            continue
        return (flag, letter_val, num_val)


def propagate(grid: list[list[Cell]], x: int, y: int):
    """ fonction propageant la découverte de cellules de proche en proche selon les règles classiques du démineur,
en partant d'une cellule dont les coordonnées x et y sont données, x étant l'indice de ligne, et y l'indice de colonne.
L'algorithme est le suivant :
1) On utilise deux listes, to_uncover qui contiendra la liste des coordonnées des cellules à découvrir, et to_compute
qui contiendra la liste des cellules sur lesquels on va travailler. Ces deux listes sont initialisées avec un élément,
le tuple (x,y)
2) tant que la liste to_compute n'est pas vide :
    a) retirer le dernier élément de to_compute, et garder les coordonnées obtenues
    b) si la cellule ayant ces coordonnées possède une valeur égale à 0, alors ajouter chacune de ses
        voisines à la fois à la liste to_compute et à la liste to_uncover
3) Parcourir la liste to_uncover et découvrir toutes les cellules correspondantes.
"""
    size = len(grid)
    to_uncover = [(x, y)]
    to_compute = [(x, y)]
    while to_compute:
        x, y = to_compute.pop()
        grid[x][y].covered = False
        if grid[x][y].value == 0:
            for adjacent_x in range(max(0, x - 1), min(size, x + 2)):
                for adjacent_y in range(max(0, y - 1), min(size, y + 2)):
                    if (adjacent_x, adjacent_y) not in to_uncover:
                        to_uncover.append((adjacent_x, adjacent_y))
                        to_compute.append((adjacent_x, adjacent_y))


def apply_position(grid: list[list[Cell]], flag: bool, x: int, y: int):
    """ fonction modifiant la grille selon la saisie proposée, et renvoyant True si la position est valide
(placement de drapeau ou case pouvant être découverte (= sans bombe)) et False si la position est celle d'une bombe.
Dans le cas où la case ne possède pas de bombe, fait appel à la fonction propagate pour découvrir toutes les cellules nécessaires"""
    if flag:
        grid[x][y].flag = not grid[x][y].flag
        return True
    if grid[x][y].value == 0:
        propagate(grid, x, y)
        return True
    return False


def count_uncovered(grid: list[list[Cell]]):
    """ fonction comptant le nombre de caese découvertes sur le plateau de jeu"""
    return sum(sum(item.covered for item in line) for line in grid)


def count_flagged(grid: list[list[Cell]]):
    """ fonction comptant le nombre de cases comportat un drapeau"""
    return sum(sum(item.flag for item in line) for line in grid)


def main_console(taille: int, difficulte=1):
    """ Fonction principale, lançant une partie de démineur avec la taille donnée, et un nombre de bombe correspondant
à taille + difficulte.
En fin de partie, montre au joueur si il a perdu la position de toutes les bombes."""
    grid = init_grid(taille)
    message_level = "Choisissez votre niveau de difficulté ! (débutant/initié/moyen/dificile/expert) \nSeuls les joueurs du niveau expert peuvent enregitrerleur score"
    level = save_score.get_from_option(message_level, set('débutant', 'initié', 'moyen', 'dificile', 'expert'))
    level_table = {
        "débutant": -4,
        "initié": -2,
        "moyen": 0,
        "difficile": 2,
        "expert": 4
    }

    nb_bombs = taille + taille//level_table[level]
    make_grid(grid, nb_bombs)
    winner = False
    time, final_time = timing()
    while True:
        affichegrid(grid, time,False, False)
        if not apply_position(grid, *ask_position(grid)):
            print(Fore.RED + "\n\t\tLOOSER\n" + Fore.WHITE)
            break
        if count_flagged(grid) == nb_bombs:
            winner = True
            print(Fore.GREEN + "\n\t\tWINNER\n" + Fore.WHITE)
            break
    affichegrid(grid, time, True, not winner)
    if winner and level == "expert":
        nom = save_score.demander_str('Quel est votre prénom ? ')
        save_score.demande_inscription(final_time(), nom)
    save_score.ask_view_score()


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    taille = 6
    main_console(taille)
