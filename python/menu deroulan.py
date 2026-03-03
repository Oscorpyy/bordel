from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator
import sys
import tty
import termios


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    # 3. Business logic validator
    @model_validator(mode='after')
    def check_contact_rules(self) -> 'AlienContact':
        # Rule: ID must start with "AC"
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        # Rule: Physical contact requires verification
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        # Rule: Telepathy requires at least 3 witnesses
        if self.contact_type == ContactType.TELEPATHIC and \
           self.witness_count < 3:
            raise ValueError("Telepathic contact requires at "
                             "least 3 witnesses")

        # Rule: Strong signal (> 7) requires a message
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) must include a message")

        return self


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
            # Gestion des séquences d'échappement (flèches)
            if ch == '\x1b':
                sys.stdin.read(1)  # skip '['
                ch = sys.stdin.read(1)
                if ch == 'A': return 'UP'
                if ch == 'B': return 'DOWN'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def show(self) -> Optional[int]:
        """Affiche le menu et retourne l'index choisi ou None si annulé."""
        print("\nSelect Contact Type (Use Arrows + Enter):")
        # Masquer le curseur
        sys.stdout.write("\033[?25l")
        
        try:
            while True:
                # Réaffiche les options
                for i, option in enumerate(self.options):
                    prefix = "> " if i == self.selected_index else "  "
                    # \033[K efface la fin de ligne
                    print(f"\r{prefix}{option}\033[K")
                
                key = self.get_key()
                
                if key == 'UP':
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif key == 'DOWN':
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif key == '\r':  # Touche Entrée
                    return self.selected_index
                elif key == 'c' or key == 'q': # Cancel
                    return None
                
                # Remonte le curseur pour réécrire par dessus au prochain tour
                sys.stdout.write(f"\033[{len(self.options)}A")
        finally:
            # Rétablir le curseur
            sys.stdout.write("\033[?25h")


def select_contact_type() -> Optional[ContactType]:
    options = [t.value for t in ContactType] + ["Cancel"]
    menu = TerminalMenu(options)
    index = menu.show()
    
    if index is not None and index < len(ContactType):
        return list(ContactType)[index]
    return None


def main() -> None:
    """Demonstration of data validation."""
    print("Alien Contact Validation")
    print("=" * 30)
    try:
        # On demande le type de contact
        selected_type = select_contact_type()
        if selected_type is None:
            print("Operation cancelled.")
            return

        valid_log = AlienContact(
            contact_id=input("Enter Contact ID: ") or "AC_ALPHA_9",
            timestamp=input("Enter Timestamp (YYYY-MM-DDTHH:MM:SS): ")
            or "2024-05-12T22:10:00",  # type: ignore
            location=input("Enter Location: ") or "Désert d'Atacama",
            contact_type=selected_type,
            signal_strength=float(input("Enter Signal Strength (0-10): ")
                                  or 8.5),
            duration_minutes=int(input("Enter Duration (min): ") or 15),
            witness_count=int(input("Enter Witness Count: ") or 2),
            message_received="Signal pulsé détecté"
        )
        print("Contact successfully recorded:")
        print(f"ID: {valid_log.contact_id}")
        print(f"Time: {valid_log.timestamp.replace(microsecond=0)}")
        print(f"Location: {valid_log.location}")
        print(f"Type: {valid_log.contact_type.value}")
        print(f"Strength: {valid_log.signal_strength}")
        print(f"Duration: {valid_log.duration_minutes} min")
        print(f"Witnesses: {valid_log.witness_count}")
        print(f"Message: {valid_log.message_received}")

    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except ValueError as e:
        print(f"Invalid Input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("")
    print("=" * 30)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id=input("Enter Contact ID: ") or "BETA_1",
            timestamp=datetime.now(),
            location=input("Enter Location: ") or "Paris",
            contact_type=ContactType.PHYSICAL,
            signal_strength=float(input("Enter Signal Strength: ") or 2.0),
            duration_minutes=int(input("Enter Duration: ") or 5),
            witness_count=int(input("Enter Witness Count: ") or 1),
            message_received=None
        )
    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except ValueError as e:
        print(f"Invalid Input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
