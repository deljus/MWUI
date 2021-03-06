# -*- coding: utf-8 -*-
#
#  Copyright 2015-2018 Ramil Nugmanov <stsouko@live.ru>
#  Copyright 2015 Oleg Varlamov <ovarlamo@gmail.com>
#  This file is part of MWUI.
#
#  MWUI is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
from pathlib import Path
from sys import stderr
from traceback import format_exc

VIEW_ENABLE = True
UPLOAD_PATH = 'upload'
IMAGES_PATH = 'upload/images'
MAX_UPLOAD_SIZE = 16 * 1024 * 1024
RESIZE_URL = '/static/images'
PORTAL_NON_ROOT = None
SECRET_KEY = 'development key'
YANDEX_METRIKA = None
DEBUG = False
SWAGGER = False

LAB_NAME = 'Kazan Chemoinformatics and Molecular Modeling Laboratory'
LAB_SHORT = 'CIMM'

BLOG_POSTS_PER_PAGE = 10

SCOPUS_ENABLE = False
SCOPUS_API_KEY = None
SCOPUS_TTL = 86400 * 7
SCOPUS_SUBJECT_LIST = '1600'

SMTP_HOST = None
SMTP_PORT = None
SMTP_LOGIN = None
SMTP_PASSWORD = None
SMTP_MAIL = None

MAIL_INKEY = None
MAIL_SIGNER = None

DB_USER = None
DB_PASS = None
DB_HOST = None
DB_PORT = 5432
DB_NAME = None
DB_MAIN = None
DB_PRED = None
DB_SCOPUS = None

JOBS_ENABLE = False
CGRDB_ENABLE = False
JOBMONITOR_URL = '127.0.0.1:8111'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_TTL = 86400
REDIS_JOB_TIMEOUT = 3600
REDIS_MAIL = 'mail'
REDIS_SCOPUS = 'scopus'

RESULTS_PER_PAGE = 50

VK_ENABLE = False
VK_CONFIRM_TOKEN = None
VK_SECRET = None
VK_AUTHOR = 1

config_list = ('UPLOAD_PATH', 'PORTAL_NON_ROOT', 'SECRET_KEY', 'RESIZE_URL', 'MAX_UPLOAD_SIZE', 'IMAGES_PATH',
               'DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME', 'DB_MAIN', 'DB_PRED', 'YANDEX_METRIKA', 'SWAGGER',
               'REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD', 'REDIS_TTL', 'REDIS_JOB_TIMEOUT', 'REDIS_MAIL',
               'LAB_NAME', 'LAB_SHORT', 'BLOG_POSTS_PER_PAGE', 'SCOPUS_API_KEY', 'SCOPUS_TTL', 'RESULTS_PER_PAGE',
               'SMTP_HOST', 'SMTP_PORT', 'SMTP_LOGIN', 'SMTP_PASSWORD', 'SMTP_MAIL', 'MAIL_INKEY', 'MAIL_SIGNER',
               'SCOPUS_SUBJECT_LIST', 'DB_SCOPUS', 'REDIS_SCOPUS', 'DB_PORT', 'VK_CONFIRM_TOKEN', 'VK_SECRET',
               'VK_AUTHOR', 'VK_ENABLE', 'CGRDB_ENABLE', 'JOBS_ENABLE', 'SCOPUS_ENABLE', 'VIEW_ENABLE',
               'JOBMONITOR_URL')

config_load_list = ['DEBUG']
config_load_list.extend(config_list)

config_dirs = [x / '.MWUI.ini' for x in (Path(__file__).parent, Path.home(), Path('/etc'))]

if not any(x.exists() for x in config_dirs):
    with config_dirs[1].open('w') as f:
        f.write('\n'.join('%s = %s' % (x, y or '') for x, y in globals().items() if x in config_list))

with next(x for x in config_dirs if x.exists()).open() as f:
    for n, line in enumerate(f, start=1):
        try:
            line = line.strip()
            if line and not line.startswith('#'):
                k, v = line.split('=')
                k = k.rstrip()
                v = v.lstrip()
                if k in config_load_list:
                    globals()[k] = int(v) if v.isdigit() else v == 'True' if v in ('True', 'False', '') else v
        except ValueError:
            print('line %d\n\n%s\n consist errors: %s' % (n, line, format_exc()), file=stderr)

IMAGES_ROOT = Path(IMAGES_PATH)
UPLOAD_ROOT = Path(UPLOAD_PATH)
SCOPUS_SUBJECT = [int(x) for x in SCOPUS_SUBJECT_LIST.split(',')]

if CGRDB_ENABLE and not JOBS_ENABLE:
    JOBS_ENABLE = True

if SCOPUS_ENABLE and not VIEW_ENABLE:
    SCOPUS_ENABLE = False

if VK_ENABLE and not VIEW_ENABLE:
    VK_ENABLE = False
