# Plex Lazy TV

You have a tremendous number of shows in your library and can't decide what episode to watch next?
I got you!
The Plex Lazy TV script is a script that will generate and maintain for you a smart playlist shuffled in the right way so as you can watch the next unwatched episode of a show.

## How does it work?

Say that you are watching Friends and you are at episode: S01E06 and in the same time you are watching The Office and you are at S03E04 and of course, in the same time you are at S04E04 of Samurai Jack. This script will shuffle your watched shows and create a random playlist but in the right order. Something like this:

- Samurai Jack S04E04
- Samurai Jack S04E05
- The Office S03E06
- Friends S03E04
- Samurai Jack S04E06
- The Office S03E07

Each time you watch something from the playlist, the script will take it out of the playlist and replace it with the next unwatched episode of your watched shows. It's like watching TV but you always get the next unwatched episode, not a random one from the end of the season or a something that you already watched.

The script is monitoring any TV Shows collection that starts with `[lazyTV]` so if you want all your shows to be considered when creating a playlist, add them to a Collection with a name that starts with `[lazyTV]`. If you want only your Anime or only your sitcoms you can create collection for those only. A collection that starts with `[lazyTV]` will have a smart playlist of shuffled unwatched episodes in the right order.

## Setup

### What you need?

1. A Plex server
2. [Tautulli](https://tautulli.com/) - the script is triggered through tautulli as tautulli monitors the watched state of your media.
3. Your plex server [token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)
4. Your tautulli api key

### Actual setup

Once you have tautulli set-up and running it means that your system is capable to run this script (you have the right python version and the plexapi package is also installed)

1. Clone this repo somewhere Tautulli can access it.
2. Copy the `config_model.ini` file rename it to `config.ini` and fill in the required keys.
3. Go to your tautulli instance and inside settings add a new notification agent.
4. For script folder choose the folder that contains the script.
5. Script file will be the `main.py` file.
6. In triggers select `Watched` this will trigger the script when an episode is marked as watched by Plex.
7. _Optionally_ you can set a condition for actions only made by your user to trigger the script (if you have multiple users that are using the server).
8. Click on `Save`
9. Either watch something or use the _Test Notifications_ section to Test the script, which will manually trigger the script and run it without watching anything.

## Questions or comments?

Open an Issue.
