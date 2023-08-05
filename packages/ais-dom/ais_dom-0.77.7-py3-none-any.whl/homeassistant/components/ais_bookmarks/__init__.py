"""Component to manage a shopping list."""
import asyncio
import logging
import uuid
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.helpers import intent
from homeassistant.util.json import load_json, save_json
import homeassistant.ais_dom.ais_global as ais_global

DOMAIN = 'ais_bookmarks'
DEPENDENCIES = ['http']
_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema({DOMAIN: {}}, extra=vol.ALLOW_EXTRA)
INTENT_ADD_FAVORITE = 'AisBookmarksAddFavorite'
INTENT_LAST_BOOKMARKS = 'AisBookmarksLastBookmarks'
PERSISTENCE_BOOKMARKS = '.ais_bookmarks.json'
PERSISTENCE_FAVORITES = '.ais_favorites.json'

SERVICE_ADD_BOOKMARK = 'add_bookmark'
SERVICE_ADD_FAVORITE = 'add_favorite'
SERVICE_GET_BOOKMARKS = 'get_bookmarks'
SERVICE_GET_FAVORITES = 'get_favorites'
SERVICE_PLAY_BOOKMARK = 'play_bookmark'
SERVICE_PLAY_FAVORITE = 'play_favorite'

@asyncio.coroutine
def async_setup(hass, config):
    """Initialize the ais bookmarks list."""
    @asyncio.coroutine
    def add_bookmark_service(call):
        """Add an current played item to bookmark"""
        d = hass.data[DOMAIN]
        attr = call.data.get("attr")
        if attr is not None:
            d.async_add(attr, True)

    @asyncio.coroutine
    def add_favorite_service(call):
        """Add an current played item to favorite."""
        d = hass.data[DOMAIN]
        attr = call.data.get("attr")
        if attr is not None:
            d.async_add(attr, False)

    @asyncio.coroutine
    def get_bookmarks_service(call):
        """Return the list of bookmarks to app LOV"""
        d = hass.data[DOMAIN]
        lv_options = [ais_global.G_EMPTY_OPTION]
        for item in d.bookmarks:
            lv_options.append(item['source'] + '; ' + item['name'])
        #     + '; ' + item['media_duration']
        hass.async_add_job(
            hass.services.async_call(
                'input_select', 'set_options', {
                    "entity_id": "input_select.ais_bookmark_last_played",
                    "options": lv_options})
        )

    @asyncio.coroutine
    def get_favorites_service(call):
        """Return the list of favorites to app LOV"""
        data = hass.data[DOMAIN]
        lv_options = [ais_global.G_EMPTY_OPTION]
        for item in data.favorites:
            lv_options.append(item['source'] + '; ' + item['name'])
        hass.async_add_job(
            hass.services.async_call(
                'input_select', 'set_options', {
                    "entity_id": "input_select.ais_bookmark_favorites",
                    "options": lv_options})
        )

    @asyncio.coroutine
    def play_bookmark_service(call):
        """Play selected bookmark"""
        bookmark = call.data.get("bookmark")
        d = hass.data[DOMAIN]
        name = bookmark.split(';', 1)[1].strip()
        source = bookmark.split(';', 1)[0].strip()
        item = next((itm for itm in d.bookmarks if (itm['name'] == name and itm['source'] == source)), None)
        if item is not None:
            hass.async_add_job(
                hass.services.async_call(
                    'media_player',
                    'play_media', {
                        "entity_id": "media_player.wbudowany_glosnik",
                        "media_content_type": "audio/mp4",
                        "media_content_id": item['media_content_id']
                    })
            )

    @asyncio.coroutine
    def play_favorite_service(call):
        """Play selected favorite"""
        favorite = call.data.get("favorite")
        d = hass.data[DOMAIN]
        name = favorite.split(';', 1)[1].strip()
        source = favorite.split(';', 1)[0].strip()
        item = next((itm for itm in d.favorites if (itm['name'] == name and itm['source'] == source)), None)
        if item is not None:
            hass.async_add_job(
                hass.services.async_call(
                    'media_player',
                    'play_media', {
                        "entity_id": "media_player.wbudowany_glosnik",
                        "media_content_type": "audio/mp4",
                        "media_content_id": item['media_content_id']
                    })
            )

    data = hass.data[DOMAIN] = BookmarksData(hass)
    intent.async_register(hass, AddFavoriteIntent())
    intent.async_register(hass, ListTopBookmarkIntent())
    hass.services.async_register(
        DOMAIN, SERVICE_ADD_BOOKMARK, add_bookmark_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_ADD_FAVORITE, add_favorite_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_GET_BOOKMARKS, get_bookmarks_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_GET_FAVORITES, get_favorites_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_PLAY_BOOKMARK, play_bookmark_service
    )
    hass.services.async_register(
        DOMAIN, SERVICE_PLAY_FAVORITE, play_favorite_service
    )

    hass.components.conversation.async_register(INTENT_ADD_FAVORITE, [
        'Dodaj do ulubionych',
        'Do ulubionych',
        'Lubię to',
    ])
    hass.components.conversation.async_register(INTENT_LAST_BOOKMARKS, [
        'Jakie mam zakładki'
    ])

    yield from data.async_load()
    return True


class BookmarksData:
    """Class to hold bookmarks list data."""

    def __init__(self, hass):
        """Initialize the bookmarks list."""
        self.hass = hass
        self.bookmarks = []
        self.favorites = []

    @callback
    def async_add(self, attributes, bookmark):
        """Add a item."""
        name = attributes.get("media_title")
        source = attributes.get("source")
        media_position = attributes.get("media_position", None)
        media_content_id = attributes.get("media_content_id")

        if name is None or source is None or media_content_id is None:
            _LOGGER.warning("can't add the bookmark, no full info provided: " + str(attributes))
            return

        if bookmark:
            # check if the audio is on bookmark list
            item = next((itm for itm in self.bookmarks if (itm['name'] == name and itm['source'] == source)), None)
            if item is not None:
                # move the bookmark
                item['media_position'] = media_position
                self.async_update(item['id'], item)
            item = {
                'name': name,
                'id': uuid.uuid4().hex,
                'source': source,
                'media_position': media_position,
                'media_content_id': media_content_id
            }
            self.bookmarks.append(item)
            self.hass.async_add_job(self.save)
            return item
        else:
            # check if the audio is on bookmark list
            item = next((itm for itm in self.favorites if (itm['name'] == name and itm['source'] == source)), None)

            if item is not None:
                message = '{}, {} jest już w ulubionych.'.format(source, name)
                self.hass.async_add_job(
                    self.hass.services.async_call(
                        'ais_ai_service', 'say_it',
                        {"text": message})
                )
                return
            item = {
                'name': name,
                'id': uuid.uuid4().hex,
                'source': source,
                'media_content_id': media_content_id
            }
            self.favorites.append(item)
            self.hass.async_add_job(self.save)
            return item

    @callback
    def async_update(self, item_id, info):
        """Update a bookmarks list item."""
        item = next((itm for itm in self.bookmarks if itm['id'] == item_id), None)

        if item is None:
            raise KeyError

        item.update(info)
        self.hass.async_add_job(self.save)
        return item

    @callback
    def async_clear_completed(self):
        """Clear completed bookmarks."""
        self.bookmarks = [itm for itm in self.bookmarks if not itm['complete']]
        self.hass.async_add_job(self.save)

    @asyncio.coroutine
    def async_load(self):
        """Load bookmarks."""
        def load():
            """Load the bookmarks synchronously."""
            try:
                self.bookmarks = load_json(self.hass.config.path(PERSISTENCE_BOOKMARKS), default=[])
                self.favorites = load_json(self.hass.config.path(PERSISTENCE_FAVORITES), default=[])
            except Exception as e:
                _LOGGER.error("Can't load bookmarks data: " + str(e))
        yield from self.hass.async_add_job(load)

    def save(self):
        """Save the bookmarks and favorites."""
        save_json(self.hass.config.path(PERSISTENCE_BOOKMARKS), self.bookmarks)
        save_json(self.hass.config.path(PERSISTENCE_FAVORITES), self.favorites)
        # LV list
        self.hass.async_add_job(self.hass.services.async_call(DOMAIN, SERVICE_GET_BOOKMARKS))
        self.hass.async_add_job(self.hass.services.async_call(DOMAIN, SERVICE_GET_FAVORITES))


class AddFavoriteIntent(intent.IntentHandler):
    """Handle AddItem intents."""
    intent_type = INTENT_ADD_FAVORITE

    @asyncio.coroutine
    def async_handle(self, intent_obj):
        """Handle the intent."""
        hass = intent_obj.hass
        state = hass.states.get('media_player.wbudowany_glosnik')
        name = state.attributes.get("media_title")
        source = state.attributes.get("source")
        media_content_id = state.attributes.get("media_content_id")
        # check if all fields are provided
        if name is None or source is None or media_content_id is None:
            answer = "Nie można dodać do ulubionych - brak informacji o odtwarzanym audio."
        else:
            answer = "Dobrze zapamiętam - dodaje {} do Twoich ulubionych".format(name)
            hass.data[DOMAIN].async_add(state.attributes, False)
        response = intent_obj.create_response()
        response.async_set_speech(answer)
        yield from hass.services.async_call(
            'ais_ai_service', 'say_it', {"text": answer})

        return response


class ListTopBookmarkIntent(intent.IntentHandler):
    """Handle ListTopBookmarkIntent intents."""

    intent_type = INTENT_LAST_BOOKMARKS

    @asyncio.coroutine
    def async_handle(self, intent_obj):
        """Handle the intent."""
        hass = intent_obj.hass
        bookmarks = intent_obj.hass.data[DOMAIN].bookmarks[-5:]
        response = intent_obj.create_response()

        if not bookmarks:
            answer = "Nie ma żadnych zakładek"

        else:
            answer = "Oto ostatnie zakładki {} na twojej liście: {}".format(
                        min(len(bookmarks), 5),
                        ', '.join(itm['name'] for itm in reversed(bookmarks)))

        response.async_set_speech(answer)
        yield from hass.services.async_call(
            'ais_ai_service', 'say_it', {"text": answer})
        return response
