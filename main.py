import argparse
from pathlib import Path

from modules.calibration import calibrate_columns
from modules.ocr_engine import (
	ensure_tesseract_available,
	preprocess_price_image,
	save_binary_image,
)


def cmd_check_tesseract() -> int:
	ok, details = ensure_tesseract_available()
	if ok:
		print(f"[OK] Tesseract detecte: {details}")
		return 0

	print("[ERREUR] Tesseract non detecte.")
	print(details)
	print(
		"Astuce: installe Tesseract puis configure son chemin dans config.json "
		'(ex: "C:/Program Files/Tesseract-OCR/tesseract.exe").'
	)
	return 1


def cmd_calibrate(args: argparse.Namespace) -> int:
	config_path = Path(args.config).resolve()
	calibrate_columns(config_path)
	return 0


def cmd_preprocess(args: argparse.Namespace) -> int:
	input_path = Path(args.input).resolve()
	output_path = Path(args.output).resolve()

	if not input_path.exists():
		print(f"[ERREUR] Fichier introuvable: {input_path}")
		return 1

	binary = preprocess_price_image(str(input_path), scale=args.scale)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	save_binary_image(binary, str(output_path))
	print(f"[OK] Image binaire ecrite: {output_path}")
	return 0


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="DofusChecker - setup OCR, calibrage souris, preprocessing binaire."
	)
	subparsers = parser.add_subparsers(dest="command", required=True)

	subparsers.add_parser("check-tesseract", help="Verifie que Tesseract OCR est detecte")

	calibrate_parser = subparsers.add_parser(
		"calibrate", help="Affiche la souris en temps reel et enregistre Nom/Prix"
	)
	calibrate_parser.add_argument(
		"--config",
		default="config.json",
		help="Chemin du fichier config JSON (defaut: config.json)",
	)

	preprocess_parser = subparsers.add_parser(
		"preprocess", help="Transforme un screenshot de prix en image binaire"
	)
	preprocess_parser.add_argument("--input", required=True, help="Image source")
	preprocess_parser.add_argument("--output", required=True, help="Image de sortie binaire")
	preprocess_parser.add_argument(
		"--scale",
		type=int,
		default=3,
		help="Facteur d'agrandissement avant binarisation (defaut: 3)",
	)

	return parser


def main() -> int:
	parser = build_parser()
	args = parser.parse_args()

	if args.command == "check-tesseract":
		return cmd_check_tesseract()
	if args.command == "calibrate":
		return cmd_calibrate(args)
	if args.command == "preprocess":
		return cmd_preprocess(args)

	parser.print_help()
	return 1


if __name__ == "__main__":
	raise SystemExit(main())
