from typing import Tuple, Union

import cv2
import numpy as np
import pytesseract
from PIL import Image


ImageLike = Union[str, np.ndarray, Image.Image]


def _to_bgr(image: ImageLike) -> np.ndarray:
	if isinstance(image, str):
		loaded = cv2.imread(image, cv2.IMREAD_COLOR)
		if loaded is None:
			raise ValueError(f"Impossible de lire l'image: {image}")
		return loaded

	if isinstance(image, Image.Image):
		rgb = np.array(image.convert("RGB"))
		return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

	if isinstance(image, np.ndarray):
		if image.ndim == 2:
			return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
		return image.copy()

	raise TypeError("Type d'image non supporte")


def preprocess_price_image(image: ImageLike, scale: int = 3) -> np.ndarray:
	bgr = _to_bgr(image)
	gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

	h, w = gray.shape
	resized = cv2.resize(
		gray,
		(max(1, w * scale), max(1, h * scale)),
		interpolation=cv2.INTER_CUBIC,
	)

	denoised = cv2.bilateralFilter(resized, d=7, sigmaColor=50, sigmaSpace=50)

	_, binary = cv2.threshold(
		denoised,
		0,
		255,
		cv2.THRESH_BINARY + cv2.THRESH_OTSU,
	)

	kernel = np.ones((2, 2), np.uint8)
	binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

	# Garantit une image strictement noir/blanc (0 ou 255).
	binary = np.where(binary > 127, 255, 0).astype(np.uint8)
	return binary


def save_binary_image(binary: np.ndarray, output_path: str) -> None:
	ok = cv2.imwrite(output_path, binary)
	if not ok:
		raise RuntimeError(f"Impossible d'ecrire l'image: {output_path}")


def extract_price_text(binary_image: np.ndarray) -> str:
	config = "--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789,"
	return pytesseract.image_to_string(binary_image, config=config).strip()


def ensure_tesseract_available() -> Tuple[bool, str]:
	try:
		version = str(pytesseract.get_tesseract_version())
		return True, version
	except Exception as exc:
		return False, str(exc)

