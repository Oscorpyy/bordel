def caesarCipher(string, pas):
    minuscule = "abcdefghijklmnopqrstuvwxyz"
    majuscule = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    for i in string:
        if i in minuscule:
            result += minuscule[(minuscule.index(i) + pas) % 26]
        elif i in majuscule:
            result += majuscule[(majuscule.index(i) + pas) % 26]
        else:
            result += i
    return result


if __name__ == "__main__":
    print(caesarCipher("Hello, World!", 3))   # Output: "Khoor, Zruog!"
    print(caesarCipher("Python 3.8", 5))      # Output: "Udymts 3.8"
    print(caesarCipher("Caesar Cipher", -2))  # Output: "Aycqyp Agncp"


def convert_base(base_from, base_to, number):
    # Vérification des contraintes de base
    if not (2 <= base_from <= 36 and 2 <= base_to <= 36):
        return "error"

    # Les caractères utilisés pour les bases > 10
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Étape 1 : Convertir le nombre (string) en base 10 (entier)
    # Python gère nativement jusqu'à la base 36 avec int()
    try:
        decimal_number = int(str(number), base_from)
    except ValueError:
        return "error"

    # Cas particulier pour le chiffre 0
    if decimal_number == 0:
        return "0"

    # Étape 2 : Convertir de la base 10 vers la base cible (base_to)
    result = ""
    while decimal_number > 0:
        reste = decimal_number % base_to
        result = digits[reste] + result  # On ajoute le nouveau chiffre
        decimal_number = decimal_number // base_to
    return result
