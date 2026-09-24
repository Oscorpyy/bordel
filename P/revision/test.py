import copy

import result  # result.py = les réponses de référence (correctes)

STATS = {"ok": 0, "ko": 0, "ref_erreur": 0}


def _executer(fonction, args):
    """Exécute fonction(*args) sur une copie des arguments.
    Retourne (valeur, None) si tout va bien, (None, "Type: message") si exception."""
    try:
        return fonction(*copy.deepcopy(args)), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _texte(valeur, erreur):
    return f"ERREUR {erreur}" if erreur else repr(valeur)


def _normaliser(valeur, normaliser):
    """Applique `normaliser` (ex: sorted) avant comparaison, sans jamais planter."""
    if normaliser is None:
        return valeur
    try:
        return normaliser(valeur)
    except Exception:
        return valeur


def run_tests(nom, fonction, cas, normaliser=None):
    """Compare `fonction` (main.py) à la fonction du même nom dans result.py.

    `cas` : liste de tuples d'arguments (un tuple par test).
    `normaliser` : optionnel, appliqué aux deux résultats avant comparaison
                   (ex: sorted quand l'ordre de la liste n'a pas d'importance).

    Affiche pour chaque test : numéro, statut, arguments, résultat.
    Une exception n'arrête pas les autres tests.
    """
    reference = getattr(result, nom)
    total = len(cas)
    print(f"\n===== {nom} =====")

    for i, args in enumerate(cas, start=1):
        arguments = ", ".join(repr(a) for a in args)
        appel = f"{nom}({arguments})"
        entete = f"Test {i}/{total}"

        obtenu, err = _executer(fonction, args)
        attendu, err_ref = _executer(reference, args)

        if err_ref:
            # La référence elle-même plante : impossible de comparer.
            STATS["ref_erreur"] += 1
            print(f"{entete} ⚠️  {appel}")
            print(f"    la référence plante : {err_ref}")
            print(f"    ton main renvoie    : {_texte(obtenu, err)}")
            continue

        identique = err is None and (
            _normaliser(obtenu, normaliser) == _normaliser(attendu, normaliser)
        )

        if identique:
            STATS["ok"] += 1
            print(f"{entete} ✅ {appel} -> {obtenu!r}")
        else:
            STATS["ko"] += 1
            print(f"{entete} ❌ {appel}")
            print(f"    obtenu  : {_texte(obtenu, err)}")
            print(f"    attendu : {attendu!r}")


def afficher_resume():
    print(
        f"\n===== RÉSUMÉ : {STATS['ok']} ✅  |  {STATS['ko']} ❌  |  "
        f"{STATS['ref_erreur']} ⚠️  (référence qui plante) ====="
    )


class Test:
    def compress(self) -> None:
        from main import compress
        run_tests("compress", compress, [
            ("aabcccccaaa",),
            ("",),
            ("a",),
            ("abc",),
            ("aabbcc",),
            ("aaaaaaaaaaaa",),
            ("aabccccccccccccccccccccccccchgoaaa",),
        ])

    def decompress(self) -> None:
        from main import decompress
        run_tests("decompress", decompress, [
            ("a2bc5a3",),
            ("",),
            ("a",),
            ("abc",),
            ("a9a3",),
            ("a2bc9c9c7hgoa3",),
        ])

    def generate_spiral(self) -> None:
        from main import generate_spiral
        run_tests("generate_spiral", generate_spiral, [
            (0,),
            (1,),
            (2,),
            (3,),
            (4,),
            (5,),
            (10,),
        ])

    def py_graph_cycle_detector(self) -> None:
        from main import py_graph_cycle_detector
        run_tests("py_graph_cycle_detector", py_graph_cycle_detector, [
            ({0: [1], 1: [2], 2: [0]},),                # cycle 0->1->2->0
            ({0: [1], 1: [2], 2: []},),                 # chaîne sans cycle
            ({},),                                      # graphe vide
            ({0: [2], 1: [0], 2: [1]},),                # cycle 0->2->1->0
            ({0: []},),                                 # un seul noeud
            ({0: [0]},),                                # boucle sur lui-même
            ({0: [1], 1: [], 2: [3], 3: [2]},),         # 2 composantes, cycle dans la 2e
            ({0: [1, 2], 1: [3], 2: [3], 3: []},),      # losange sans cycle
        ])

    def py_room_scheduler(self) -> None:
        from main import py_room_scheduler
        run_tests("py_room_scheduler", py_room_scheduler, [
            ([[0, 30], [5, 10], [15, 20]],),
            ([],),
            ([[0, 5]],),
            ([[7, 10], [2, 4]],),
            ([[1, 5], [5, 10]],),                       # réunions qui se touchent
            ([[1, 10], [2, 10], [3, 10]],),             # toutes en même temps
        ])

    def island_matrix_counter(self) -> None:
        from main import island_matrix_counter
        run_tests("island_matrix_counter", island_matrix_counter, [
            ([["1", "1", "1", "1", "0"],
              ["1", "1", "1", "0", "0"],
              ["1", "1", "1", "1", "0"],
              ["0", "0", "0", "0", "0"]],),
            ([["1", "1", "0", "0", "0"],
              ["1", "1", "0", "0", "0"],
              ["0", "0", "1", "0", "0"],
              ["0", "0", "0", "1", "1"]],),
            ([],),
            ([["1"]],),
            ([["0"]],),
            ([["1", "0", "1"],
              ["0", "1", "0"],
              ["1", "0", "1"]],),                       # damier : diagonales != connectées
        ])

    def prism_detector(self) -> None:
        from main import prism_detector
        run_tests("prism_detector", prism_detector, [
            (["CAT", "A..", "T.."], "CAT"),
            ([], "CAT"),
            (["CAT", "A..", "T.."], "DOG"),
            (["CAT"], "CAT"),
            (["C..", "A..", "T.."], "CAT"),
            (["CAT", "A..", "T.."], ""),
        ], normaliser=sorted)                           # l'ordre des résultats n'a pas d'importance

    def word_ladder(self) -> None:
        from main import word_ladder
        run_tests("word_ladder", word_ladder, [
            ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
            ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),   # "cog" absent
            ("hit", "hot", ["hot"]),
            ("hot", "dog", ["hot", "dog", "dot"]),
            ("hit", "hit", ["hit"]),
            ("hit", "cog", []),
            ("a", "c", ["a", "b", "c"]),
        ])


if __name__ == "__main__":
    t = Test()
    t.compress()
    t.decompress()
    t.generate_spiral()
    t.py_graph_cycle_detector()
    t.py_room_scheduler()
    t.island_matrix_counter()
    t.prism_detector()
    t.word_ladder()
    afficher_resume()