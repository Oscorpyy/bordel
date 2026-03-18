import sys

try:
    from maze_generator import MazeGenerator
except ImportError:
    print("Erreur: Le module 'maze_generator' n'est pas installé.")
    print("Veuillez installer le .whl dans votre environnement en utilisant :")
    print("pip install /home/opernod/42/ama/mazegen-1.0.0-py3-none-any.whl")
    sys.exit(1)


def main():
    print("=== Test du module indépendant MazeGenerator ===")

    # Instanciation de la classe
    generator = MazeGenerator()

    width = 100
    height = 100
    print(f"Génération d'un labyrinthe test de taille {width}x{height}...")

    # Génération du labyrinthe
    generator.generate(width, height, entry=(0, 0),
                       exit_pos=(width-1, height-1))

    # Test de récupération de solution si la méthode est exposée
    solution = generator.get_solution()

    print("Labyrinthe généré avec succès !")
    if solution:
        print(f"Solution trouvée. Longueur : {len(solution)} cases.")
    else:
        print("Aucun chemin trouvé ou algorithme non exécuté.")


if __name__ == "__main__":
    main()
