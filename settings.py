from os import environ

class CorsMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        original_path = environ.get('PATH_INFO', '')
        request_method = environ.get('REQUEST_METHOD', '')
        
        # Если это API запрос без завершающего слэша
        if original_path == '/api/sessions' and not original_path.endswith('/'):
            if request_method == 'OPTIONS':
                # Отвечаем на preflight запрос напрямую
                headers = [
                    ('Access-Control-Allow-Origin', 'https://gregory-ch.github.io'),
                    ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                    ('Access-Control-Allow-Headers', 'Content-Type, otree-rest-key'),
                    ('Content-Type', 'text/plain'),
                    ('Content-Length', '0')
                ]
                start_response('200 OK', headers)
                return [b'']
            else:
                # Для других методов делаем явное перенаправ��ение с CORS заголовками
                headers = [
                    ('Location', original_path + '/'),
                    ('Access-Control-Allow-Origin', 'https://gregory-ch.github.io'),
                    ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                    ('Access-Control-Allow-Headers', 'Content-Type, otree-rest-key'),
                    ('Content-Type', 'text/plain'),
                    ('Content-Length', '0')
                ]
                start_response('307 Temporary Redirect', headers)
                return [b'']
        
        # Для всех остальных запросов
        def custom_start_response(status, headers, exc_info=None):
            headers = list(headers)
            headers.append(('Access-Control-Allow-Origin', 'https://gregory-ch.github.io'))
            headers.append(('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'))
            headers.append(('Access-Control-Allow-Headers', 'Content-Type, otree-rest-key'))
            headers.append(('X-Frame-Options', 'ALLOW-FROM https://gregory-ch.github.io'))
            headers.append(('Content-Security-Policy', "frame-ancestors 'self' https://gregory-ch.github.io"))
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)


SESSION_CONFIGS = [
   
    # ),
    dict(
        name='rockpaperscissors',
        display_name="Rock/Paper/Scissors against Robot",
        app_sequence=['rockpaperscissors'],
        num_demo_participants=1,
    ),

    dict(
        name='data_to_dgp',
        display_name="data to DGP demo",
        app_sequence=['data_to_dgp', ],
        num_demo_participants=1,
    ),

    # dict(
    #     name='data_to_dgp_quiz',
    #     display_name="data to DGP task quiz",
    #     app_sequence=['quiz', 'data_to_dgp', 'AOT'],
    #     num_demo_participants=1,
    # ),

    dict(
        name='data_to_dgp_eng',
        display_name="data to DGP ENG",
        app_sequence=['consent', 'quizeng', 'data_to_dgp', "survey_eng"],
        num_demo_participants=2,
    ),

    dict(
        name='AOT',
        display_name="trains with oth",
        app_sequence=['trains',  'MPL', 'bret', 'payment_info'],
        num_demo_participants=1,

    ),

    
    # dict(
    #     name='end_of_experiment',
    #     display_name="show up fee",
    #     app_sequence=['end_of_experiment'],
    #     num_demo_participants=1,

    # ),
    

    # dict(
    #     name='data_to_dgp_new_design',
    #     display_name="data to DGP task new design",
    #     # app_sequence=['data_to_dgp_new', 'AOT'],
    #     app_sequence=[#"quiz",
    #                   "data_to_dgp_new", "survey_eng"],
    #     num_demo_participants=1,
    # ),
    
     dict(
        name='dsst',
        display_name="dsst",
        app_sequence=["dsst_from_scratch"],
        num_demo_participants=1,
    ),

    dict(
        name='data_to_dgp_new_design_inverse',
        display_name="data to DGP Inverse",
        app_sequence=["quiz_inverse_rus", "data_to_dgp_new", "survey_eng"],
        num_demo_participants=1,
    ),
        dict(
        name='cursor2',
        display_name="cursor2",
        app_sequence=["cursor2"],
        num_demo_participants=1,
    ),

    # dict(
    #     name='any_app', 
    #     app_sequence=['any_app',], 
    #     num_demo_participants=1,
    #     # use_browser_bots=True
    # ),
    # dict(
    #     name='tictactoe',
    #     display_name="Tic-Tac-Toe",
    #     app_sequence=['tictactoe'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='strategy_method',
    #     display_name="Strategy Method",
    #     app_sequence=['strategy_method'],
    #     num_demo_participants=2,
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.09, participation_fee=00.00, doc="")

# ISO-639 code
# for example: de, fr, ja, ko,'ru', zh-hans

LANGUAGE_CODE = 'en'
# LANGUAGE_CODE = 'ru'  # "," occures....

# e.g. EUR, GBP, CNY, JPY
# REAL_WORLD_CURRENCY_CODE = 'RUR'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
# ADMIN_PASSWORD = '1325'

DEMO_PAGE_INTRO_HTML = """ """
DEMO_PAGE_TITLE = "Behavecon 2023 Hse "

SECRET_KEY = '4387860144726'

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'corsheaders']

PARTICIPANT_FIELDS = [
    'booking_time',
    'cards',
    'order',
    'reaction_times',
    'read_mind_in_eyes_score',
    'responses',
    'stimuli',
    'svo_angle',
    'svo_category',
    'symbol_sets',
    'tasks',
    'time_left',
]

SESSION_FIELDS = ['finished_p1_list', 'iowa_costs', 'wisconsin', 'intergenerational_history']

MIDDLEWARE = [
    'settings.CorsMiddleware',
]
