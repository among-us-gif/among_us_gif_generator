import argparse
import os

from gifgen import generator


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--message',
        help='Message after ejection.\nNOTE: overrides role option',
    )
    parser.add_argument(
        '--name',
        default='I',
        help='Name of the person or thing being ejected',
    )
    parser.add_argument(
        '--role',
        choices=('impostor', 'crewmate', 'unknown'),
        default='unknown',
        help='Role to be displayed for the ejection.\n'
             'NOTE: overridden by the --message option',
    )
    parser.add_argument(
        '--color',
        choices=generator.all_colors,
        help='Crewmate Color, exclude for a random color.',
    )
    parser.add_argument(
        '--skin',
        choices=generator.all_skins,
        default='rand',
        help='Crewmate Skin, exclude for a random skin.',
    )
    args = parser.parse_args()

    if args.message:
        gif_path = generator.generate_ejection_custom_message(
            color=args.color,
            skn=args.skin,
            text=args.message,
            path=os.getcwd(),
            watermark=False,
        )
    else:
        if args.role == 'impostor':
            impostor = True
        elif args.role == 'crewmate':
            impostor = False
        else:
            impostor = None
        gif_path = generator.generate_ejection_message(
            color=args.color,
            skn=args.skin,
            person=args.name,
            impostor=impostor,
            path=os.getcwd(),
            watermark=False,
        )
    print(f'Generated your gif at {gif_path}')


if __name__ == '__main__':
    raise SystemExit(main())
