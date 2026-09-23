from typing import Optional
import sys
import tty
import termios


class TerminalMenu:
    """Gère un menu interactif dans le terminal."""
    def __init__(self, options: list[str]):
        self.options = options
        self.selected_index = 0

    def get_key(self) -> str:
        """Lit une touche du clavier sans attendre Entrée."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                sys.stdin.read(1)  # skip '['
                ch = sys.stdin.read(1)
                if ch == 'A':
                    return 'UP'
                if ch == 'B':
                    return 'DOWN'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def show(self) -> Optional[int]:
        """Affiche le menu et retourne l'index choisi ou None si annulé."""
        print("\nSelect Contact Type (Use Arrows + Enter):")
        sys.stdout.write("\033[?25l")

        try:
            while True:
                for i, option in enumerate(self.options):
                    prefix = "> " if i == self.selected_index else "  "
                    # \033[K efface la fin de ligne
                    print(f"\r{prefix}{option}\033[K")

                key = self.get_key()

                if key == 'UP':
                    self.selected_index = (self.selected_index - 1) % len(
                        self.options)
                elif key == 'DOWN':
                    self.selected_index = (self.selected_index + 1) % len(
                        self.options)
                elif key == '\r':
                    return self.selected_index
                elif key == 'c' or key == 'q':
                    return None

                sys.stdout.write(f"\033[{len(self.options)}A")
        finally:
            # Rétablir le curseur
            sys.stdout.write("\033[?25h")
