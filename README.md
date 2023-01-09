# Youtube_Backup

YoutubeDownloader is a python script that allows you to make backups of your YouTube channel.

## Startup

Install packages with pip:

```bash
pip install -r requirements.txt
```

Get you're Google API key and put it in the file `config.json` instead of `YOUR_API_KEY`:

https://console.cloud.google.com/

## Example

examples of some usage: 

```
python main.py [-start VIDEOID]
python main.py [-downloadvid indexOfTheVideoInTheJsonFile] [-json JSONFILE]
python main.py [-help]
python main.py [-download_all_videos] [-json JSONFILE]
```