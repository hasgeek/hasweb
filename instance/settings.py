# -*- coding: utf-8 -*-
#: Site title
SITE_TITLE = 'HasGeek'
#: Site id (for network bar)
SITE_ID = 'home'
#: Google Analytics code
GA_CODE = 'UA-19123154-1'
#: Timezone
TIMEZONE = 'Asia/Calcutta'
#: Flat pages
FLATPAGES_AUTO_RELOAD = False
FLATPAGES_EXTENSION = '.md'
#: LastUser server
LASTUSER_SERVER = 'https://auth.hasgeek.com/'
MAIL_FAIL_SILENTLY = False
MAIL_SERVER = 'localhost'
DEFAULT_MAIL_SENDER = ('HasGeek', 'bot@hasgeek.com')
MAIL_DEFAULT_SENDER = DEFAULT_MAIL_SENDER  # For new versions of Flask-Mail
#: Logging: recipients of error emails
ADMINS = []
#: Log file
LOGFILE = 'error.log'
