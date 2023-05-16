def demander_str(message) -> str:
    """
Demande d'entrer une chaine de caractère
    """
    while True:
        entree_utilisteur = input(message).strip()
        if entree_utilisteur:
            return entree_utilisteur
        print("Vous n'avez rien entré")


def demande_number(message, interval: tuple[int | float, int | float] = (-float('Infinity'), float('Infinity')), must_be_int = False) -> int|float:
    while True:
        number = demander_str(message)
        try:
            number = int(number)
            if must_be_int:
                print("Vous n'avez pas entré un nombre entié!")
                continue
        except ValueError:
            try:
                number = float(number)
            except ValueError:
                print("Vous n'avez pas entré un nombre!")
                continue
        if interval[0] <= number <= interval[1]:
            return number
        else:
            print(f"Vous n'avez pas entré un nombre entre {interval[0]} et {interval[1]}!")


def get_from_option(message: str, options: set[str]):
    user_input = ''
    while user_input not in options:
        print(
            f'Je ne comprend répondez en choisissant parmis ces options: f{", ".join(options)}')
        user_input = demander_str(message).lower()
    return user_input


def demander(message: str) -> bool:
    """Fonction demandant au joueur / à la joueuse si il/elle souhaite faire l'action demandé.
    Le joueur/La joueuse doit pouvoir répondre par oui (ou o) ou par non (ou n),
    et la fonction doit être dumbproof.
    """
    return get_from_option(message + " (o/n)", set('o', 'n', 'oui', 'non', 'yes', 'no', 'y')) in set('o', 'oui', 'yes', 'y')


def ask_view_score():
    if demander('Voulez vous regarder le classement ?'):
        print(read_save().affiche_score())


def same_gamer(name, score, same_name_gamer):
    """
    Fonction appelé lorsque deux noms sont identiques,
    elle revoie le nom de la partie avec le meilleur score si l'utillisateur nous confirme avoir déjà joué,
    sinon elle demande un nouveau nom à l'utilisateur
"""
    if same_name_gamer['want_to_replay']:
        return name, score
    if demander('Avez vous déjà joué avec ce nom ?'):
        if same_name_gamer['score'] < score:
            return name, score
        else:
            return name, same_name_gamer['score']
    return demander_str('Votre nom à déjà été enregistré:\nVotre noveau nom est: '), score


def demande_inscription(time_score: int, gamer: str) -> None:
    if demander('Voulez vous sauvegarder votre partie ?'):
        sauve_score(gamer, time_score, same_gamer)


class sauve_score:

    def __init__(self, nom_j: str, score_j: int, same_name_gamer) -> None:
        self.nom_j, self.score_j = nom_j, score_j
        self.same_name_gamer = same_name_gamer
        self.hight_score = []
        self._read_previous_save()
        self._write_score()

    def _read_previous_save(self) -> None:
        """
    Lit les score déjà enregistré en modifiant {self.hight_score}
    """
        self.hight_score = read_save().get_score()
        self._same_gamer()
        self._add_new_player()

    def _same_gamer(self) -> None:
        """
    Vérifit si le nom du joueur à déjà été enregitré, dans ce cas il enclanche la callback {self.same_name_gamer},
    qui définit le comprtement associé
    """
        for gamer in self.hight_score:
            if gamer['nom'] == self.nom_j:
                self.hight_score.remove(gamer)
                self.nom_j, self.score_j = self.same_name_gamer(
                    self.nom_j, self.score_j, gamer)

    def _add_new_player(self) -> None:
        """
    Ajoute le nouveau à sa place dans le classement 
    """
        for i, gamer in enumerate(self.hight_score):
            if self.score_j >= gamer['score']:
                self.hight_score.insert(
                    i, {"nom": self.nom_j, "score": self.score_j})
                return
        self.hight_score.append({"nom": self.nom_j, "score": self.score_j})

    def _write_score(self) -> None:
        """"
    écrit le score du joueur dans le fichier HighScore.txt
    """
        with open("HighScore.txt", "w", encoding="utf8") as file:
            for s in self.hight_score:
                if s is not None:
                    file.write(f"{s['nom']} / {s['score']}")
                else:
                    file.write("Inconnu / 0\n")


class read_save:
    def get_score(self):
        """ Fonction récupérant les HighScore sauvegardés depuis un fichier HishScore.txt"""
        try:
            with open('HighScore.txt', "r", encoding="utf-8") as file:
                lines = file.readlines()
                hight_score = [None]*len(lines)
                for i, line in enumerate(lines):
                    nom, score, replay = line.split(" / ")
                    replay = replay.replace('\n', '')
                    try:
                        hight_score[i] = {"nom": nom, "score": int(score)}
                    except ValueError:
                        hight_score[i] = {"nom": nom, "score": 0}
                return hight_score
        except FileNotFoundError:
            return []

    def affiche_score(self) -> str:
        """Renvoie une chaine de caractères des HighScore correctement formatée pour la console"""
        return "".join(f"{index + 1} {' ' if index != 9 else ''}{d['nom']:>14} : {d['score']:>11} €\n" for index, d in enumerate(self.get_score()[:10]))
