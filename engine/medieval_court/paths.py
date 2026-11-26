from pathlib import Path

# Racine du package medieval_court
PACKAGE_DIR = Path(__file__).resolve().parent

# Ressources graphiques
SHADERS_DIR = PACKAGE_DIR / "shaders"

# Autres ressources (pour plus tard)
ASSETS_DIR = PACKAGE_DIR / "assets"
TEXTURES_DIR = ASSETS_DIR / "textures"
FONTS_DIR = ASSETS_DIR / "fonts"