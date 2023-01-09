from libs.youtube_backup import YouTubeDownloader
import sys

if __name__ == "__main__":
    # Créer un objet de la classe YouTubeDownloader
    yt = YouTubeDownloader()
    # Appelle la fonction main de l'objet yt en passant les arguments de la ligne de commande
    args = yt.parser.parse_args(sys.argv[1:])
    yt.main()