import sys
import getpass
from pathlib import Path
from pykeepass import PyKeePass

# Assuming you have a logger setup
# import logging
# logger = logging.getLogger(__name__)


class Credentials:
    """ Simple class for storing credentials """
    def __init__(self):
        self.aliexpress = type('Aliexpress', (), {})()
        self.openai = type('Openai', (), {})()
        self.openai.assistant_id = type('AssistantId', (), {})()
        self.gemini = type('Gemini', (), {})()
        self.discord = type('Discord', (), {})()
        self.telegram = type('Telegram', (), {})()
        self.presta = type('Presta', (), {})()
        self.presta.client = type('PrestaClient', (), {})()
        self.smtp = type('SMTP', (), {})()
        self.facebook = type('Facebook', (), {})()
        self.presta_translations = type('PrestaTranslations', (), {})()
        self.gapi = type('GAPI', (), {})()


class Config:
    """ Simple class for storing configuration data."""
    def __init__(self):
        self.secrets = Path('secrets') #Path('путь к папке')
        self.credentials = Credentials()
        self.path = type('Path', (), {})()
        self.path.secrets = Path('secrets')



class KeePassLoader:
    """ Loads credentials from KeePass database."""
    def __init__(self):
         self.path = Config().path
         self.credentials = Credentials()


    def _load_credentials(self) -> None:
        """ Loads credentials from KeePass based on configured groups. """

        kp = self._open_kp(3)
        if not kp:
            print("Error :( ")
            ...
            sys.exit(1)

        if not self._load_aliexpress_credentials(kp):
            print('Failed to load Aliexpress credentials')

        if not self._load_openai_credentials(kp):
            print('Failed to load OpenAI credentials')

        if not self._load_gemini_credentials(kp):
            print('Failed to load GoogleAI credentials')

        if not self._load_discord_credentials(kp):
            print('Failed to load Discord credentials')

        if not self._load_telegram_credentials(kp):
            print('Failed to load Telegram credentials')

        if not self._load_prestashop_credentials(kp):
            print('Failed to load prestashop credentials')
            
        if not self._load_smtp_credentials(kp):
            print('Failed to load SMTP credentials')

        if not self._load_facebook_credentials(kp):
            print('Failed to load Facebook credentials')

        if not self._load_presta_translations_credentials(kp):
            print('Failed to load Translations credentials')

        if not self._load_gapi_credentials(kp):
            print('Failed to load GAPI credentials')

    def _open_kp(self, retry: int = 3) -> PyKeePass | None:
        """ Open KeePass database
        Args:
            retry (int): Number of retries
        """
        while retry > 0:
            try:
                password = getpass.getpass(prompt='Enter KeePass master password: ')
                kp = PyKeePass(str(self.path.secrets / 'credentials.kdbx'), password=password)
                return kp
            except Exception as ex:
                print(f"Failed to open KeePass database Exception: {ex}, {retry-1} retries left.")
                ...
                retry -= 1
                if retry < 1:
                    # logger.critical('Failed to open KeePass database after multiple attempts', exc_info=True)
                    ...
                    sys.exit()
        return None

    # Define methods for loading various credentials
    def _load_aliexpress_credentials(self, kp: PyKeePass) -> bool:
        """ Load Aliexpress API credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['suppliers', 'aliexpress', 'api']).entries[0]
            self.credentials.aliexpress.api_key = self._get_entry_value(entry, 'api_key')
            self.credentials.aliexpress.secret = self._get_entry_value(entry, 'secret')
            self.credentials.aliexpress.tracking_id = self._get_entry_value(entry, 'tracking_id')
            self.credentials.aliexpress.email = self._get_entry_value(entry, 'email')
            self.credentials.aliexpress.password = entry.password
            return True
        except Exception as ex:
            print(f"Failed to extract Aliexpress API key from KeePass {ex}" )
            ...
            return False

    def _load_openai_credentials(self, kp: PyKeePass) -> bool:
        """ Load OpenAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            openai_api_keys = kp.find_groups(path=['openai']).entries
            assistants = kp.find_groups(path=['openai','assistants']).entries

            for entry in openai_api_keys:
                setattr(self.credentials.openai, entry.title, self._get_entry_value(entry,'api_key') or self._get_entry_value(entry,'project_api') )
            for assistant in assistants:
                setattr(self.credentials.openai.assistant_id, assistant.title, self._get_entry_value(assistant,'assistant_id'))
            return True
        except Exception as ex:
            print(f"Failed to extract OpenAI credentials from KeePass {ex}" )
            ...
            return False


    def _load_gemini_credentials(self, kp: PyKeePass) -> bool:
        """ Load GoogleAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entries = kp.find_groups(path=['gemini']).entries

            for entry in entries:
                 setattr(self.credentials.gemini, entry.title, self._get_entry_value(entry,'api_key'))

            return True
        except Exception as ex:
            print(f"Failed to extract GoogleAI credentials from KeePass {ex}")
            ...
            return False

    def _load_telegram_credentials(self, kp: PyKeePass) -> bool:
        """Load Telegram credentials from KeePass.

        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entries = kp.find_groups(path=['telegram']).entries
            for entry in entries:
                setattr(self.credentials.telegram, entry.title, self._get_entry_value(entry, 'token'))
            return True
        except Exception as ex:
            print(f"Failed to extract Telegram credentials from KeePass {ex}")
            ...
            return False

    def _load_discord_credentials(self, kp: PyKeePass) -> bool:
        """ Load Discord credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['discord']).entries[0]
            self.credentials.discord.application_id = self._get_entry_value(entry,'application_id')
            self.credentials.discord.public_key = self._get_entry_value(entry,'public_key')
            self.credentials.discord.bot_token = self._get_entry_value(entry,'bot_token')
            return True
        except Exception as ex:
            print(f"Failed to extract Discord credentials from KeePass {ex}")
            ...
            return False

    def _load_prestashop_credentials(self, kp: PyKeePass) -> bool:
         """ Load prestashop credentials from KeePass
         Args:
            kp (PyKeePass): The KeePass database instance.
         Returns:
            bool: True if loading was successful, False otherwise.
         """

         for entry in kp.find_groups(path=['prestashop', 'clients']).entries:
            try:
                setattr(self.credentials.presta.client, entry.title, entry.title)
                current_client = getattr(self.credentials.presta.client, entry.title)

                setattr(current_client, 'api_key', self._get_entry_value(entry,'api_key'))
                setattr(current_client, 'api_domain', self._get_entry_value(entry,'api_domain'))
                setattr(current_client, 'db_server', self._get_entry_value(entry,'db_server'))
                setattr(current_client, 'db_user', self._get_entry_value(entry,'db_user'))
                setattr(current_client, 'db_password', self._get_entry_value(entry,'db_password'))

            except Exception as ex:
                print(f"Failed to extract prestashop credentials from KeePass {ex}")
                ...
                return False

         return True

    def _load_smtp_credentials(self, kp: PyKeePass) -> bool:
        """Load SMTP credentials from KeePass.

        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['smtp']).entries[0]
            self.credentials.smtp.server = self._get_entry_value(entry,'server')
            self.credentials.smtp.port = self._get_entry_value(entry,'port')
            self.credentials.smtp.username = self._get_entry_value(entry,'username')
            self.credentials.smtp.password = entry.password
            return True
        except Exception as ex:
            print(f"Failed to extract SMTP credentials from KeePass {ex}")
            ...
            return False

    def _load_facebook_credentials(self, kp: PyKeePass) -> bool:
        """Load Facebook credentials from KeePass.
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['facebook']).entries[0]
            self.credentials.facebook.app_id = self._get_entry_value(entry,'app_id')
            self.credentials.facebook.app_secret = self._get_entry_value(entry,'app_secret')
            self.credentials.facebook.access_token = self._get_entry_value(entry,'access_token')
            return True
        except Exception as ex:
            print(f"Failed to extract Facebook credentials from KeePass {ex}")
            ...
            return False


    def _load_presta_translations_credentials(self, kp: PyKeePass) -> bool:
        """Load Presta translations credentials from KeePass.

        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['presta_translations']).entries[0]
            self.credentials.presta_translations.project_id = self._get_entry_value(entry,'project_id')
            self.credentials.presta_translations.api_key = self._get_entry_value(entry,'api_key')
            return True
        except Exception as ex:
            print(f"Failed to extract Translations credentials from KeePass {ex}")
            ...
            return False

    def _load_gapi_credentials(self, kp: PyKeePass) -> bool:
        """ Load GAPI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
             entry = kp.find_groups(path=['google']).entries[0]
             self.credentials.gapi.api_key = self._get_entry_value(entry,'api_key')
             return True
        except Exception as ex:
             print(f"Failed to extract GAPI credentials from KeePass {ex}")
             ...
             return False
    
    def _get_entry_value(self, entry, key):
         """ Helper method to safely get custom property value """
         return entry.custom_properties.get(key, None)


if __name__ == '__main__':
    loader = KeePassLoader()
    loader._load_credentials()

    # Example of accessing credentials
    print("Aliexpress API Key:", loader.credentials.aliexpress.api_key)
    print("OpenAI API Keys:")
    for key, value in vars(loader.credentials.openai).items():
      if key != 'assistant_id':
        print(f"  {key}: {value}")
    print("OpenAI Assistant IDs:")
    for key, value in vars(loader.credentials.openai.assistant_id).items():
        print(f" {key}: {value}")
    print("Gemini API Keys:")
    for key, value in vars(loader.credentials.gemini).items():
      print(f"  {key}: {value}")
    print("Telegram Tokens:")
    for key, value in vars(loader.credentials.telegram).items():
       print(f" {key}: {value}")
    print("Discord Application ID:", loader.credentials.discord.application_id)
    print("Prestashop clients:", [client for client in vars(loader.credentials.presta.client).keys()])
    for client_name, client_data in vars(loader.credentials.presta.client).items():
        print(f"  {client_name} api_key:", client_data.api_key)
    print("SMTP Server:", loader.credentials.smtp.server)
    print("Facebook App ID:", loader.credentials.facebook.app_id)
    print("Presta Translations Project ID:", loader.credentials.presta_translations.project_id)
    print("GAPI Api Key:", loader.credentials.gapi.api_key)