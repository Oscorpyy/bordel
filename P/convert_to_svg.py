#!/usr/bin/env python3
"""
Convertisseur d'images matricielles vers SVG.
Usage :
  python3 convert_to_svg.py <chemin_source> <chemin_destination.svg> [options]

Exemple :
  python3 convert_to_svg.py ~/Downloads/image.jpeg frontend/public/favicon.svg
"""

import sys
import os
import base64
import argparse
from pathlib import Path

# Formats d'images matricielles supportés
SUPPORTED_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff", ".tif", ".ppm", ".pgm"
)


def embed_image_to_svg(input_path: Path, output_path: Path) -> None:
    """Encapsule l'image en Base64 dans une balise <image> SVG."""
    from PIL import Image

    with Image.open(input_path) as img:
        width, height = img.size
        fmt = (img.format or "PNG").lower()
        if fmt in ("jpeg", "jpg"):
            mime_type = "image/jpeg"
        elif fmt == "png":
            mime_type = "image/png"
        elif fmt == "webp":
            mime_type = "image/webp"
        elif fmt == "gif":
            mime_type = "image/gif"
        else:
            mime_type = "image/png"

    with open(input_path, "rb") as f:
        encoded_data = base64.b64encode(f.read()).decode("ascii")

    svg_content = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
        f'  <image width="{width}" height="{height}" '
        f'href="data:{mime_type};base64,{encoded_data}"/>\n'
        f'</svg>\n'
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)


def vectorize_image_to_svg(input_path: Path, output_path: Path) -> None:
    """Vectorise véritablement l'image en chemins géométriques SVG via vtracer."""
    try:
        import vtracer
    except ImportError:
        sys.stderr.write(
            "❌ Erreur : Le module 'vtracer' est manquant pour la vectorisation.\n"
            "Installez-le avec : pip install vtracer\n"
            "Ou utilisez le mode encapsulation : --mode embed\n"
        )
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    vtracer.convert_image_to_svg_py(
        image_path=str(input_path),
        out_path=str(output_path),
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=4,
        color_precision=6,
        layer_difference=16,
        corner_threshold=60,
        length_threshold=4.0,
        max_iterations=10,
        splice_threshold=45,
        path_precision=2,
    )


def convert_pair(src_raw: str, dst_raw: str, mode: str = "vector") -> bool:
    """Traite une paire (source, destination). Retourne True si succès, False sinon."""
    src_path = Path(os.path.expanduser(src_raw))
    dst_path = Path(os.path.expanduser(dst_raw))

    # 1. Vérification de l'existence du fichier source
    if not src_path.is_file():
        print(f"❌ Erreur : Le fichier source '{src_raw}' est introuvable.", file=sys.stderr)
        print("⏩ Fichier ignoré.\n", file=sys.stderr)
        return False

    # 2. Vérification de l'extension du fichier source
    suffix = src_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        formats_list = ", ".join(SUPPORTED_EXTENSIONS)
        ext_display = suffix if suffix else "(aucune extension)"
        print(
            f"❌ Erreur : Format non supporté pour '{src_path.name}' [{ext_display}].",
            file=sys.stderr,
        )
        print(f"ℹ️  Formats d'images pris en charge : {formats_list}", file=sys.stderr)
        print("⏩ Fichier ignoré.\n", file=sys.stderr)
        return False

    # 3. Préparation du chemin de destination
    if dst_path.is_dir() or dst_raw.endswith(("/", "\\")):
        dst_path = dst_path / f"{src_path.stem}.svg"
    elif dst_path.suffix.lower() != ".svg":
        dst_path = dst_path.with_suffix(".svg")

    print(f"🔄 Conversion : '{src_raw}' ➔ '{dst_path}' (mode: {mode})...")

    # 4. Conversion selon le mode choisi
    try:
        if mode == "embed":
            embed_image_to_svg(src_path, dst_path)
        else:
            vectorize_image_to_svg(src_path, dst_path)

        size_kb = dst_path.stat().st_size / 1024
        print(f"✅ Succès ! Fichier SVG créé : {dst_path} ({size_kb:.1f} Ko)\n")
        return True
    except Exception as e:
        print(f"❌ Erreur pendant la conversion : {e}", file=sys.stderr)
        print("⏩ Fichier ignoré.\n", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convertit des images (.png, .jpg, .jpeg, etc.) en .svg.",
        usage="%(prog)s <chemin_source> <chemin_destination.svg> [options]",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Paire(s) de chemins : <source> <destination.svg>",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["vector", "embed"],
        default="vector",
        help="Mode de conversion : 'vector' (courbes vectorielles SVG) ou 'embed' (encapsulation base64).",
    )

    args = parser.parse_args()

    # Vérification des arguments positionnels
    if not args.files or len(args.files) % 2 != 0:
        formats_list = ", ".join(SUPPORTED_EXTENSIONS)
        print("❌ Erreur : Vous devez fournir des paires de chemins <source> <destination>.\n", file=sys.stderr)
        print("Exemple d'utilisation :", file=sys.stderr)
        print("  python3 convert_to_svg.py ~/Downloads/image.jpeg frontend/public/favicon.svg\n", file=sys.stderr)
        print(f"ℹ️  Formats sources acceptés : {formats_list}\n", file=sys.stderr)
        sys.exit(1)

    # Découpage des arguments par paires (src, dst)
    pairs = [(args.files[i], args.files[i + 1]) for i in range(0, len(args.files), 2)]

    success_count = 0
    for src, dst in pairs:
        if convert_pair(src, dst, mode=args.mode):
            success_count += 1

    total = len(pairs)
    if total > 1:
        print(f"🏁 Bilan : {success_count}/{total} fichier(s) converti(s).")

    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
