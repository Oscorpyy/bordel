import copy

import result  # result.py = les réponses de référence (correctes)

STATS = {"ok": 0, "ko": 0, "ref_erreur": 0}


def _executer(fonction, args):
    """Exécute fonction(*args) sur une copie des arguments.

    Retourne (valeur, None) si OK, (None, 'Type: message') si exception.
    """
    try:
        return fonction(*copy.deepcopy(args)), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _texte(valeur, erreur):
    return f"ERREUR {erreur}" if erreur else repr(valeur)


def _normaliser(valeur, normaliser):
    """Applique normaliser avant comparaison, sans jamais planter."""
    if normaliser is None:
        return valeur
    try:
        return normaliser(valeur)
    except Exception:
        return valeur


def run_tests(nom, fonction, cas, normaliser=None):
    """Compare fonction (main.py) à la fonction de même nom dans result.py.

    cas : liste de tuples d'arguments.
    normaliser : optionnel (ex: sorted).
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


def run_class_tests(nom, classe_etudiant, classe_ref, scenarios):
    """Exécute une série de scénarios sur classe_etudiant et classe_ref."""
    total = len(scenarios)
    print(f"\n===== {nom} =====")

    for i, (init_args, operations) in enumerate(scenarios, start=1):
        entete = f"Scénario {i}/{total}"
        try:
            obj_etudiant = classe_etudiant(*copy.deepcopy(init_args))
        except Exception as e:
            STATS["ko"] += 1
            print(
                f"{entete} ❌ Erreur instanciation {nom}(*{init_args!r}) : "
                f"{type(e).__name__}: {e}"
            )
            continue

        try:
            obj_ref = classe_ref(*copy.deepcopy(init_args))
        except Exception as e:
            STATS["ref_erreur"] += 1
            print(f"{entete} ⚠️  Erreur référence instanciation : {e}")
            continue

        echec = False
        for methode, args in operations:
            appel = f".{methode}({', '.join(repr(a) for a in args)})"
            meth_etudiant = getattr(obj_etudiant, methode, None)
            meth_ref = getattr(obj_ref, methode, None)

            if meth_etudiant is None:
                STATS["ko"] += 1
                print(f"{entete} ❌ Méthode manquante {appel}")
                echec = True
                break

            obtenu, err = _executer(meth_etudiant, args)
            attendu, err_ref = _executer(meth_ref, args)

            if err_ref:
                STATS["ref_erreur"] += 1
                print(
                    f"{entete} ⚠️  La référence plante sur {appel} : {err_ref}"
                )
                echec = True
                break

            if err is not None or obtenu != attendu:
                STATS["ko"] += 1
                print(f"{entete} ❌ Échec sur {appel}")
                print(f"    obtenu  : {_texte(obtenu, err)}")
                print(f"    attendu : {attendu!r}")
                echec = True
                break

        if not echec:
            STATS["ok"] += 1
            print(
                f"{entete} ✅ {nom}(*{init_args!r}) -> "
                f"{len(operations)} opération(s) validée(s)"
            )


def afficher_resume():
    print(
        f"\n===== RÉSUMÉ : {STATS['ok']} ✅  |  {STATS['ko']} ❌  |  "
        f"{STATS['ref_erreur']} ⚠️  (référence qui plante) ====="
    )


class Test:
    # =================================================================
    #                     RANK 06 - TESTS
    # =================================================================

    def prefix_dictionary(self) -> None:
        try:
            from main import PrefixDictionary
        except ImportError:
            print("\n===== PrefixDictionary =====")
            print("⚠️  PrefixDictionary non trouvé dans main.py")
            STATS["ko"] += 1
            return

        scenarios = [
            ((), [
                ("insert", ("apple",)),
                ("search", ("apple",)),
                ("search", ("app",)),
                ("starts_with", ("app",)),
                ("insert", ("app",)),
                ("search", ("app",)),
                ("starts_with", ("ban",)),
                ("search", ("ban",)),
            ]),
            ((), [
                ("insert", ("a",)),
                ("starts_with", ("a",)),
                ("search", ("a",)),
                ("starts_with", ("b",)),
                ("search", ("b",)),
            ]),
            ((), [
                ("insert", ("car",)),
                ("insert", ("card",)),
                ("insert", ("care",)),
                ("starts_with", ("car",)),
                ("search", ("card",)),
                ("search", ("care",)),
                ("search", ("cart",)),
                ("starts_with", ("cart",)),
            ]),
        ]
        run_class_tests(
            "PrefixDictionary",
            PrefixDictionary,
            result.PrefixDictionary,
            scenarios,
        )

    def pack_strings(self) -> None:
        try:
            from main import pack, unpack
        except ImportError:
            print("\n===== pack_strings =====")
            print("⚠️  pack ou unpack non trouvé dans main.py")
            STATS["ko"] += 1
            return

        cas = [
            ["hello", "world"],
            [],
            [""],
            ["42", "exam#net", "level:6"],
            ["", "a", "", "b", ""],
            ["multiline\ntext", "special#:#char", "123#456", ""],
            ["alpha", "beta", "gamma", "delta"],
        ]

        print("\n===== pack_strings =====")
        for i, original in enumerate(cas, start=1):
            entete = f"Test {i}/{len(cas)}"
            encoded, err_pack = _executer(pack, (original,))
            if err_pack:
                STATS["ko"] += 1
                print(f"{entete} ❌ pack({original!r}) a levé : {err_pack}")
                continue

            decoded, err_unpack = _executer(unpack, (encoded,))
            if err_unpack:
                STATS["ko"] += 1
                print(f"{entete} ❌ unpack(...) a levé : {err_unpack}")
                continue

            ref_encoded = result.pack(original)
            cross_decoded, err_cross = _executer(unpack, (ref_encoded,))

            if (
                decoded == original
                and err_cross is None
                and cross_decoded == original
            ):
                STATS["ok"] += 1
                print(f"{entete} ✅ unpack(pack({original!r})) == {original!r}")
            else:
                STATS["ko"] += 1
                print(f"{entete} ❌ Échec sur {original!r}")
                print(f"    pack renvoie   : {encoded!r}")
                print(f"    unpack renvoie : {decoded!r}")
                print(f"    attendu        : {original!r}")

    def task_order(self) -> None:
        try:
            from main import task_order
        except ImportError:
            print("\n===== task_order =====")
            print("⚠️  task_order non trouvé dans main.py")
            STATS["ko"] += 1
            return

        run_tests("task_order", task_order, [
            (2, [[1, 0]]),
            (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
            (2, [[0, 1], [1, 0]]),
            (3, []),
            (1, []),
            (4, [[2, 0], [1, 0], [3, 1], [3, 2]]),
            (5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]),
            (3, [[0, 1], [1, 2], [2, 0]]),
        ])

    def redundant_link(self) -> None:
        try:
            from main import redundant_link
        except ImportError:
            print("\n===== redundant_link =====")
            print("⚠️  redundant_link non trouvé dans main.py")
            STATS["ko"] += 1
            return

        run_tests("redundant_link", redundant_link, [
            ([[1, 2], [1, 3], [2, 3]],),
            ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],),
            ([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]],),
            ([[1, 2], [2, 3], [3, 1]],),
        ])

    def trie_autocomplete(self) -> None:
        try:
            from main import trie_autocomplete
        except ImportError:
            print("\n===== trie_autocomplete =====")
            print("⚠️  trie_autocomplete non trouvé dans main.py")
            STATS["ko"] += 1
            return

        run_tests("trie_autocomplete", trie_autocomplete, [
            (["apple", "app", "apricot", "banana"], "app"),
            (["apple", "app", "apricot", "banana"], "ban"),
            (["hello", "world", "help", "heap"], "he"),
            (["test"], "xyz"),
            (["cat", "car", "card", "care"], "car"),
            ([], "test"),
            (["a", "ab", "abc"], ""),
            (["dup", "dup", "dupe"], "dup"),
        ])

    def union_find_system(self) -> None:
        try:
            from main import UnionFind
        except ImportError:
            print("\n===== UnionFind =====")
            print("⚠️  UnionFind non trouvé dans main.py")
            STATS["ko"] += 1
            return

        scenarios = [
            ((5,), [
                ("connected", (0, 1)),
                ("union", (0, 1)),
                ("connected", (0, 1)),
                ("union", (1, 2)),
                ("connected", (0, 2)),
                ("union", (0, 1)),
                ("connected", (3, 4)),
                ("union", (3, 4)),
                ("connected", (0, 4)),
                ("union", (2, 4)),
                ("connected", (0, 3)),
            ]),
            ((3,), [
                ("union", (0, 1)),
                ("union", (1, 2)),
                ("connected", (0, 2)),
            ]),
            ((4,), [
                ("connected", (0, 3)),
                ("union", (0, 1)),
                ("union", (2, 3)),
                ("connected", (1, 2)),
                ("union", (1, 3)),
                ("connected", (0, 2)),
            ]),
        ]
        run_class_tests("UnionFind", UnionFind, result.UnionFind, scenarios)

    def cache_keeper(self) -> None:
        try:
            from main import CacheKeeper
        except ImportError:
            print("\n===== CacheKeeper =====")
            print("⚠️  CacheKeeper non trouvé dans main.py")
            STATS["ko"] += 1
            return

        scenarios = [
            ((2,), [
                ("put", (1, 1)),
                ("put", (2, 2)),
                ("get", (1,)),
                ("put", (3, 3)),
                ("get", (2,)),
                ("put", (4, 4)),
                ("get", (1,)),
                ("get", (3,)),
                ("get", (4,)),
            ]),
            ((1,), [
                ("put", (1, 10)),
                ("get", (1,)),
                ("put", (2, 20)),
                ("get", (1,)),
                ("get", (2,)),
            ]),
            ((3,), [
                ("put", (1, 10)),
                ("put", (2, 20)),
                ("put", (3, 30)),
                ("get", (1,)),
                ("put", (4, 40)),
                ("get", (2,)),
                ("put", (1, 100)),
                ("get", (1,)),
            ]),
        ]
        run_class_tests(
            "CacheKeeper", CacheKeeper, result.CacheKeeper, scenarios
        )

    def min_heap(self) -> None:
        try:
            from main import MinHeap
        except ImportError:
            print("\n===== MinHeap =====")
            print("⚠️  MinHeap non trouvé dans main.py")
            STATS["ko"] += 1
            return

        scenarios = [
            ((), [
                ("push", (5,)),
                ("push", (3,)),
                ("push", (8,)),
                ("peek", ()),
                ("pop", ()),
                ("peek", ()),
                ("size", ()),
                ("pop", ()),
                ("pop", ()),
                ("pop", ()),
                ("peek", ()),
                ("size", ()),
            ]),
            ((), [
                ("push", (10,)),
                ("push", (4,)),
                ("push", (15,)),
                ("push", (1,)),
                ("push", (20,)),
                ("pop", ()),
                ("pop", ()),
                ("pop", ()),
                ("pop", ()),
                ("pop", ()),
            ]),
        ]
        run_class_tests("MinHeap", MinHeap, result.MinHeap, scenarios)

    def bridge_finder(self) -> None:
        try:
            from main import bridge_finder
        except ImportError:
            print("\n===== bridge_finder =====")
            print("⚠️  bridge_finder non trouvé dans main.py")
            STATS["ko"] += 1
            return

        run_tests("bridge_finder", bridge_finder, [
            ({0: [1, 2], 1: [0, 2], 2: [0, 1]},),
            ({0: [1], 1: [0, 2], 2: [1]},),
            ({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]},),
            ({},),
            ({0: [1], 1: [0]},),
            ({0: [1, 2], 1: [0, 2, 3, 4], 2: [0, 1], 3: [1, 4], 4: [1, 3]},),
            ({0: [1], 1: [0, 2], 2: [1, 3], 3: [2]},),
        ], normaliser=sorted)

    def all_rank06(self) -> None:
        """Lance tous les tests du Rank 06."""
        print("***************************************************")
        print("                 TESTS RANK 06                     ")
        print("***************************************************")
        self.prefix_dictionary()
        self.pack_strings()
        self.task_order()
        self.redundant_link()
        self.trie_autocomplete()
        self.union_find_system()
        self.cache_keeper()
        self.min_heap()
        self.bridge_finder()

    # =================================================================
    #                     RANK 05 - TESTS
    # =================================================================

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
            ("aabccccccccccccccccccccccccchgoaaaaaaaaaaaaaaaaaaaaaaaaaaaa",),
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
            ({0: [1], 1: [2], 2: [0]},),
            ({0: [1], 1: [2], 2: []},),
            ({},),
            ({0: [2], 1: [0], 2: [1]},),
            ({0: []},),
            ({0: [0]},),
            ({0: [1], 1: [], 2: [3], 3: [2]},),
            ({0: [1, 2], 1: [3], 2: [3], 3: []},),
        ])

    def py_room_scheduler(self) -> None:
        from main import py_room_scheduler
        run_tests("py_room_scheduler", py_room_scheduler, [
            ([[0, 30], [5, 10], [15, 20]],),
            ([],),
            ([[0, 5]],),
            ([[7, 10], [2, 4]],),
            ([[1, 5], [5, 10]],),
            ([[1, 10], [2, 10], [3, 10]],),
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
              ["1", "0", "1"]],),
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
        ], normaliser=sorted)

    def word_ladder(self) -> None:
        from main import word_ladder
        run_tests("word_ladder", word_ladder, [
            ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
            ("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),
            ("hit", "hot", ["hot"]),
            ("hot", "dog", ["hot", "dog", "dot"]),
            ("hit", "hit", ["hit"]),
            ("hit", "cog", []),
            ("a", "c", ["a", "b", "c"]),
        ])

    def all_rank05(self) -> None:
        """Lance tous les tests du Rank 05."""
        print("***************************************************")
        print("                 TESTS RANK 05                     ")
        print("***************************************************")
        self.compress()
        self.decompress()
        self.generate_spiral()
        self.py_graph_cycle_detector()
        self.py_room_scheduler()
        self.island_matrix_counter()
        self.prism_detector()
        self.word_ladder()


if __name__ == "__main__":
    t = Test()
    t.all_rank06()
    afficher_resume()
