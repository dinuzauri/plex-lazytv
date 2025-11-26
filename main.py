import logging
import os
import random

from plexapi.collection import Collection
from plexapi.playlist import Playlist
from plexapi.server import CONFIG, PlexServer
from plexapi.myplex import MyPlexAccount
from plexapi.library import ShowSection

filename = os.path.basename(__file__)
filename = filename.split(".")[0]

logger = logging.getLogger(filename)
logger.setLevel(logging.DEBUG)

error_format = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(message)s")
stream_format = logging.Formatter("%(message)s")

file_handler = logging.FileHandler("{}.log".format(filename))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(error_format)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_format)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Edit server settings here or in the plex api config file
PLEX_URL = ""
PLEX_TOKEN = ""
TAUTULLI_URL = ""
TAUTULLI_APIKEY = ""


# CONSTANTS
# size of the lazy playlist
PLAYLIST_SIZE = 6
# keyword for the name of collection from which the playlist will be populated
LAZY_COLLECTION_PATTERN = "[lazyTV]"

if not PLEX_URL:
    PLEX_URL = CONFIG.data["auth"].get("server_baseurl")
if not PLEX_TOKEN:
    PLEX_TOKEN = CONFIG.data["auth"].get("server_token")
if not TAUTULLI_URL:
    TAUTULLI_URL = CONFIG.data["auth"].get("tautulli_baseurl")
if not TAUTULLI_APIKEY:
    TAUTULLI_APIKEY = CONFIG.data["auth"].get("tautulli_apikey")

plex: PlexServer = PlexServer(PLEX_URL, PLEX_TOKEN)
account: MyPlexAccount = MyPlexAccount()
tv: ShowSection = plex.library.section("TV Shows")


def get_lazy_collections() -> list:
    lazy_collections = []
    server_collections = tv.collections()
    for collection in server_collections:
        if collection.title.startswith(LAZY_COLLECTION_PATTERN):
            lazy_collections.append(collection)
    return lazy_collections


def lazy_playlist_exists(name: str):
    for playlist in plex.playlists():
        if playlist.title == name and playlist.playlistType == "video":
            return True
    return False


def get_rand_tv_ep(collection: Collection, new_playlist: bool = False):
    show = get_rand_show(collection)
    logger.debug(f"{show} picked randomly")
    playlist_episodes = [] if new_playlist else plex.playlist(collection.title).items()
    seasons = show.seasons()
    for season in seasons:
        # check if season is not watched
        if not season.isPlayed:
            episodes = season.episodes()
            for episode in episodes:
                # check if episode is not watched
                if not episode.isPlayed and episode not in playlist_episodes:
                    return episode
    return None


def create_playlist(collection: Collection):
    logger.info("Creating a new playlist")
    Playlist.create(
        server=plex,
        title=collection.title,
        items=get_rand_tv_ep(collection=collection, new_playlist=True),
    )


def get_rand_show(collection):
    shows = collection.items()
    print(f"Available shows:{shows}")
    show = None
    while show is None or show.isPlayed:
        show = random.sample(shows, 1)[0]
    return show


def clean_lazy_playlist(name: str) -> bool:
    lazy_playlist = plex.playlist(name)
    logger.debug(f"Cleaning the playlist {lazy_playlist}")
    episodes = lazy_playlist.items()
    incomplete = len(episodes) < PLAYLIST_SIZE
    logger.debug(f"Playlist contains {len(episodes)} items")
    for episode in episodes:
        if episode.isPlayed:
            lazy_playlist.removeItems(episode)
            logger.info(f"{episode} has been removed from the playlist")
            incomplete = True
    logger.debug(f"Playlist incomplete status: {incomplete}")
    return incomplete


def fill_playlist(collection):
    logger.debug("Attempting to fill in the playlist")
    lazy_playlist = plex.playlist(collection.title)
    lazy_episodes = lazy_playlist.items()
    needed_episodes = PLAYLIST_SIZE - len(lazy_episodes)
    logger.debug(f"{needed_episodes} new episodes are needed")
    playlist_spot = 1
    while playlist_spot <= needed_episodes:
        episode = get_rand_tv_ep(collection)
        if episode:
            lazy_playlist.addItems(episode)
            logger.info(f"{episode} added to the playlist")
            playlist_spot += 1
        else:
            playlist_spot -= 1


if __name__ == "__main__":
    # add a delay to avoid race conditions
    # time.sleep(30)

    lazy_collections: list[Collection] = get_lazy_collections()

    for collection in lazy_collections:
        try:
            logger.info("Lazy TV script started...")
            if lazy_playlist_exists(collection.title):
                logger.info("Lazy playlist detected..")
                any_episodes_were_removed = clean_lazy_playlist(collection.title)
                if any_episodes_were_removed:
                    fill_playlist(collection)
            else:
                logger.info("Lazy playlist not detected..")
                create_playlist(collection)
                fill_playlist(collection)
            logger.info("Lazy TV script stopped")
        except Exception as e:
            logger.exception(e)
