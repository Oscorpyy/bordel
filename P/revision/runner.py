import copy
import sys
from typing import Any

from test import Test, afficher_resume


# =====================================================================
#             CAS DE TEST RAPIDES (MODIFIABLES PAR DÉFAUT)
# =====================================================================
CAS_RAPIDES: dict[str, Any] = {
    # --- RANK 06 ---
    "pack": (["hello", "world"],),
    "unpack": ("5#hello5#world",),
    "task_order": (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
    "redundant_link": ([[1, 2], [1, 3], [2, 3]],),
    "trie_autocomplete": (["apple", "app", "apricot", "banana"], "app"),
    "bridge_finder": ({0: [1, 2], 1: [0, 2], 2: [0, 1]},),
}

# =====================================================================
#                      LISTE DES EXERCICES
# =====================================================================
LISTE_EXERCICES = [
    # --- RANK 06 ---
    {"type": "class", "nom": "PrefixDictionary", "test_methode": "prefix_dictionary"},
    {"type": "pack_strings", "nom": "pack_strings", "test_methode": "pack_strings"},
    {"type": "func", "nom": "task_order", "test_methode": "task_order"},
    {"type": "func", "nom": "redundant_link", "test_methode": "redundant_link"},
    {"type": "func", "nom": "trie_autocomplete", "test_methode": "trie_autocomplete"},
    {"type": "class", "nom": "UnionFind", "test_methode": "union_find_system"},
    {"type": "class", "nom": "CacheKeeper", "test_methode": "cache_keeper"},
    {"type": "class", "nom": "MinHeap", "test_methode": "min_heap"},
    {"type": "func", "nom": "bridge_finder", "test_methode": "bridge_finder"},
]


def _executer_test_rapide_fonction(nom: str, func: Any, cas_override: Any = None) -> None:
    cas = cas_override if cas_override is not None else CAS_RAPIDES.get(nom)
    if cas is None:
        return
    args = cas if isinstance(cas, (tuple, list)) else (cas,)
    appel_str = f"{nom}({', '.join(repr(a) for a in args)})"
    try:
        res = func(*copy.deepcopy(args))
        print(f"👉 Test rapide modifiable : {appel_str}")
        print(f"   Résultat obtenu : {res!r}")
    except Exception as e:
        print(f"👉 Test rapide modifiable : {appel_str}")
        print(f"   ❌ Erreur : {type(e).__name__}: {e}")


def _executer_test_rapide_classe(nom: str, cls: Any) -> None:
    try:
        if nom == "PrefixDictionary":
            obj = cls()
            obj.insert("apple")
            res_search = obj.search("apple")
            res_prefix = obj.starts_with("app")
            print("👉 Test rapide modifiable : PrefixDictionary")
            print(f"   insert('apple') -> search('apple'): {res_search!r}, starts_with('app'): {res_prefix!r}")
        elif nom == "UnionFind":
            obj = cls(3)
            obj.union(0, 1)
            res = obj.connected(0, 1)
            print("👉 Test rapide modifiable : UnionFind(3)")
            print(f"   union(0, 1) -> connected(0, 1): {res!r}")
        elif nom == "CacheKeeper":
            obj = cls(2)
            obj.put(1, 42)
            res = obj.get(1)
            print("👉 Test rapide modifiable : CacheKeeper(2)")
            print(f"   put(1, 42) -> get(1): {res!r}")
        elif nom == "MinHeap":
            obj = cls()
            obj.push(5)
            obj.push(2)
            res = obj.peek()
            print("👉 Test rapide modifiable : MinHeap")
            print(f"   push(5), push(2) -> peek(): {res!r}")
    except Exception as e:
        print(f"👉 Test rapide modifiable : {nom} -> ❌ Erreur : {type(e).__name__}: {e}")


def lancer_tests(exo_seul: str | None = None, cas_perso: Any = None) -> None:
    """Détecte les exercices définis dans main.py et lance leurs tests.

    :param exo_seul: Nom d'un exercice précis si tu ne veux tester que celui-là.
    :param cas_perso: Tuple d'arguments personnalisés pour le test rapide.
    """
    # Récupération du module principal
    main_mod = sys.modules.get("main") or sys.modules.get("__main__")
    if main_mod is not None:
        sys.modules.setdefault("main", main_mod)

    t = Test()
    nb_trouves = 0

    print("=" * 65)
    print("🚀 DÉTECTION ET EXÉCUTION AUTOMATIQUE DES TESTS")
    print("=" * 65)

    for exo in LISTE_EXERCICES:
        nom = exo["nom"]
        genre = exo["type"]
        methode_test = exo["test_methode"]

        # Filtre optionnel si un seul exercice est demandé
        if exo_seul and nom != exo_seul and exo_seul not in (nom, methode_test):
            continue

        if genre == "func":
            if hasattr(main_mod, nom) and callable(getattr(main_mod, nom)):
                nb_trouves += 1
                func = getattr(main_mod, nom)
                print(f"\n--- [Exercice détecté : {nom}] ---")
                _executer_test_rapide_fonction(nom, func, cas_override=cas_perso)
                getattr(t, methode_test)()

        elif genre == "class":
            if hasattr(main_mod, nom) and isinstance(getattr(main_mod, nom), type):
                nb_trouves += 1
                cls = getattr(main_mod, nom)
                print(f"\n--- [Classe détectée : {nom}] ---")
                _executer_test_rapide_classe(nom, cls)
                getattr(t, methode_test)()

        elif genre == "pack_strings":
            pack_present = hasattr(main_mod, "pack") and callable(getattr(main_mod, "pack"))
            unpack_present = hasattr(main_mod, "unpack") and callable(getattr(main_mod, "unpack"))

            if pack_present or unpack_present:
                nb_trouves += 1
                print(f"\n--- [Exercice détecté : pack_strings] ---")
                if pack_present:
                    _executer_test_rapide_fonction("pack", getattr(main_mod, "pack"))
                if unpack_present:
                    _executer_test_rapide_fonction("unpack", getattr(main_mod, "unpack"))

                if pack_present and unpack_present:
                    t.pack_strings()
                else:
                    manquant = "unpack" if pack_present else "pack"
                    print(f"ℹ️ Implémente aussi '{manquant}' pour lancer la suite complète de tests pack_strings.")

    if nb_trouves > 0:
        afficher_resume()
    else:
        if exo_seul:
            print(f"\n⚠️ L'exercice '{exo_seul}' n'a pas été trouvé dans main.py.")
        else:
            print("\nℹ️ Aucun exercice détecté dans main.py pour le moment.")
            print("👉 Code une fonction (ex: def decompress(s): ...) et relance !")
