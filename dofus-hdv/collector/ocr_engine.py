import cv2
import pytesseract

# Config Tesseract pour ne lire que des chiffres (pour la zone prix)
CONF_DIGITS = r"--oem 3 --psm 6 outputbase digits"


def image_to_text(img_np, is_price=False):
    # Pretraitement: Gris -> Inversion (Noir sur Blanc)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    config = CONF_DIGITS if is_price else ""
    text = pytesseract.image_to_string(thresh, config=config)
    return text.strip()
