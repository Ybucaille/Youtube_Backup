import requests
import json
import os
from pytube import YouTube
import argparse
from tqdm import tqdm

class YouTubeDownloader:
    def __init__(self):
        # Initialiser les variables de classe
        self.api_key = None
        self.args = None

        # Charger la clé API à partir du fichier JSON
        with open('api_key.json', 'r') as f:
            api_key_data = json.load(f)
            self.api_key = api_key_data['api_key']

        # Si la clé API n'est pas définie, quitter le programme
        if not self.api_key:
            print("API key not found")
            exit()

        # Créer un parseur d'arguments
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-start", dest="vid", help="Start the program with an id of a video")
        self.parser.add_argument("-downloadvid", help="Download a specific video, you have to put the index number of the video in the json file and to pass the json file with the --json argument")
        self.parser.add_argument("-json", help="Download a specific video")
        #self.parser.add_argument("-numberofvideos", help="Get the number of videos of a channel")
        self.parser.add_argument("-help", action="help", help="your json file with the video links")


    def main(self):
        # Parser les arguments passés en ligne de commande
        self.args = self.parser.parse_args()  # affecter les arguments à l'attribut args

        # Appeler la fonction appropriée en fonction des arguments passés
        if self.args.vid:
            channel_id = self.get_channel_id(self.args)
            self.get_channel_videos_url(channel_id, f'videos_{self.get_channel_title(channel_id)}.json')
        elif self.args.downloadvid:
            self.download_video(self.args.downloadvid)
        elif self.args.json:
            self.download_all_videos(self.args.json)
        elif self.args.help:
            self.parser.print_help()



    def get_channel_id(self, args):
        url = "https://www.googleapis.com/youtube/v3/videos?id={vid}&key={api_key}&part=snippet".format(
            vid=args.vid, api_key=self.api_key
        )
        d = requests.get(url).json()
        return d['items'][0]['snippet']['channelId']

    def get_channel_title(self, cid):
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={cid}&key={api_key}".format(
            cid=cid, api_key=self.api_key
        )
        d = requests.get(url).json()
        return d['items'][0]['snippet']['channelTitle']

    def get_channel_videos_url(self, channel_id, filename):
        """Fonction qui récupère l'URL de toutes les vidéos de la chaîne YouTube avec l'ID de la chaîne spécifié, en utilisant la pagination, et stocke les résultats dans un fichier JSON"""
        # Construire l'URL de l'API YouTube
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "type": "video",
            "maxResults": 50,  # Récupérer un maximum de 50 résultats à chaque fois
            "order": "date",  # Récupérer les vidéos les plus récentes en premier
            "key": self.api_key
        }
        video_urls = []

        params["pageToken"] = ""  # Définir le paramètre "pageToken" à la valeur par défaut

        # Récupérer le nombre total de vidéos de la chaîne YouTube
        channel_videos_count = int(self.get_channel_videos_count(channel_id))
        # Indiquer s'il y a une page suivante de résultats
        has_next_page = True
        # Effectuer une requête à l'API tant que toutes les vidéos n'ont pas été récupérées
        while len(video_urls) < channel_videos_count and has_next_page:
            # Effectuer une requête GET à l'API
            response = requests.get(url, params=params)
            # Vérifier si la requête a réussi
            if response.status_code != 200:
                # Afficher les informations de débogage de l'erreur
                print(f'La requête a échoué avec le code de statut {response.status_code}')
                return None
            # Récupérer les données de la réponse
            data = response.json()
            # Vérifier si les données contiennent la clé attendue
            if "items" not in data:
                print("La réponse ne contient pas les données attendues")
                return None
            # Récupérer les URL des vidéos
            for item in data["items"]:
                video_id = item["id"]["videoId"]
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                video_urls.append(video_url)
            # Vérifier si il y a une page suivante de résultats
            if "nextPageToken" in data:
                data["pageToken"] = data["nextPageToken"]
            else:
                break
            
            # Mettre à jour le paramètre pageToken pour récupérer la prochaine page de résultats
            params["pageToken"] = data["nextPageToken"]
        # On récupère le path du dossier courant
        path = os.getcwd()
        # on vérifie si le dossier videos existe déjà dans le dossier courant
        if not os.path.exists(os.path.join(path, 'jsons')):
            #créer un dossier videos dans le dossier courant
            path = os.path.join(path, 'jsons')
            os.mkdir(path)
        else:
            path = os.path.join(path, 'videos')
        # Stocker les résultats dans un fichier JSON
        path = os.getcwd()
        filename = '\\jsons\\videos_{}.json'.format(self.get_channel_title(channel_id))
        filepath = path + filename
        with open(filepath, 'w') as f:
            json.dump(video_urls, f)

        return video_urls


    def get_channel_videos_count(self, channel_id):
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "statistics",
            "id": channel_id,
            "key":self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:  # Check if the request was successful
            print(f'Request failed with status code {response.status_code}')
            return None
        data = response.json()
        if "items" not in data:  # Check if the data contains the expected key
            print('Response does not contain expected data')
            return None
        return data["items"][0]["statistics"]["videoCount"]


    def download_video(self, url):
        """Fonction qui télécharge une vidéo YouTube à partir de son URL et la stocke dans le dossier spécifié"""
        try:
            #on récupère l'url de la vidéo à partir d'un fichier json
            with open(self.args.json) as f:
                data = json.load(f)
                url = data[int(self.args.downloadvid)]
            # Créer un objet YouTube
            yt = YouTube(url)
            # Récupérer la vidéo la plus haute résolution
            video = yt.streams.get_highest_resolution()
            # On récupère le path du dossier courant
            path = os.getcwd()
            # on vérifie si le dossier videos existe déjà dans le dossier courant
            if not os.path.exists(os.path.join(path, 'videos')):
                #créer un dossier videos dans le dossier courant
                path = os.path.join(path, 'videos')
                os.mkdir(path)
            else:
                path = os.path.join(path, 'videos')
            # Envoyer une requête GET pour télécharger la vidéo
            response = requests.get(video.url, stream=True)
            # Ouvrir le fichier en mode écriture binaire
            with open(os.path.join(path, video.title + '.mp4'), 'wb') as f:
                # Télécharger la vidéo en chunks
                with tqdm(total=int(response.headers.get('Content-Length', 0)), unit='B', unit_scale=True, desc=f'Downloading {video.title}') as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        # Écrire le chunk dans le fichier
                        f.write(chunk)
                        # Mettre à jour la barre de progression
                        pbar.update(len(chunk))
            print(f'"la vidéo : {video.title}" a été téléchargé avec succès')
        except Exception as e:
            print(f'"{url}" n\'a pas pu être téléchargé')
            print(e)

    def download_all_videos(self, videos_file):
        with open(videos_file, 'r') as file:
            videos_data = json.load(file)
            for url in videos_data:
                try:
                    # Créer un objet YouTube
                    yt = YouTube(url)
                    # Récupérer la vidéo la plus haute résolution
                    video = yt.streams.get_highest_resolution()
                    # On récupère le path du dossier courant
                    path = os.getcwd()
                    # on vérifie si le dossier videos existe déjà dans le dossier courant
                    if not os.path.exists(os.path.join(path, 'videos')):
                        #créer un dossier videos dans le dossier courant
                        path = os.path.join(path, 'videos')
                        os.mkdir(path)
                    else:
                        path = os.path.join(path, 'videos')
                    # Envoyer une requête GET pour télécharger la vidéo
                    response = requests.get(video.url, stream=True)
                    # Ouvrir le fichier en mode écriture binaire
                    with open(os.path.join(path, video.title + '.mp4'), 'wb') as f:
                        # Télécharger la vidéo en chunks
                        with tqdm(total=int(response.headers.get('Content-Length', 0)), unit='B', unit_scale=True, desc=f'Downloading {video.title}') as pbar:
                            for chunk in response.iter_content(chunk_size=1024):
                                # Écrire le chunk dans le fichier
                                f.write(chunk)
                                # Mettre à jour la barre de progression
                                pbar.update(len(chunk))
                    print(f'"la vidéo : {video.title}" a été téléchargé avec succès')
                except Exception as e:
                    print(f'"{url}" n\'a pas pu être téléchargé')
                    print(e)