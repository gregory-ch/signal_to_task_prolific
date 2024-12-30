# from os import environ
# import sys
# import traceback
# from starlette.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware
# from starlette.applications import Starlette

# # Основные настройки oTree
# EXTENSION_APPS = ['otree']

# # CORS middleware настройки
# MIDDLEWARE = [
#     Middleware(
#         CORSMiddleware,
#         allow_origins=['*'],
#         allow_methods=['*'],
#         allow_headers=['*'],
#         allow_credentials=False,
#         max_age=1728000
#     )
# ]

SESSION_CONFIGS = [
   
    # ),
    # dict(
    #     name='rockpaperscissors',
    #     display_name="Rock/Paper/Scissors against Robot",
    #     app_sequence=['rockpaperscissors'],
    #     num_demo_participants=1,
    # ),

    # dict(
    #     name='data_to_dgp',
    #     display_name="data to DGP demo",
    #     app_sequence=['data_to_dgp', ],
    #     num_demo_participants=1,
    # ),

    # dict(
    #     name='data_to_dgp_quiz',
    #     display_name="data to DGP task quiz",
    #     app_sequence=['quiz', 'data_to_dgp', 'AOT'],
    #     num_demo_participants=1,
    # ),

    # dict(
    #     name='data_to_dgp_eng',
    #     display_name="data to DGP ENG",
    #     app_sequence=['consent', 'quizeng', 'data_to_dgp', "survey_eng"],
    #     num_demo_participants=2,
    # ),

    # dict(
    #     name='AOT',
    #     display_name="trains with oth",
    #     app_sequence=['trains',  'MPL', 'bret', 'payment_info'],
    #     num_demo_participants=1,

    # ),

    
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

    # dict(
    #     name='data_to_dgp_new_design_inverse',
    #     display_name="data to DGP Inverse",
    #     app_sequence=["quiz_inverse_rus", "data_to_dgp_new", "survey_eng"],
    #     num_demo_participants=1,
    # ),
        dict(
        name='prolific_study',
        display_name="prolific",
        app_sequence=["consent", "intro", "dsst_from_scratch",  "cursor2", "dsst_from_scratch2", 'end'],
        context="prolific",
        num_demo_participants=1,
    ),
        dict(
        name='cursor2',
        display_name="cursor2",
        app_sequence=["cursor2"],
        num_demo_participants=1,
    ),
    #   dict(
    #     name='go_no_go',
    #     display_name='Attention test (Go/No-Go)',
    #     app_sequence=['go_no_go'],
    #     num_demo_participants=1,
    # ),

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
    # dict(
    #     name='econ101',
    #     display_name='Econ 101 class',
    #     participant_label_file='_rooms/econ101.txt',
    # ),
    dict(
        name='prolific',
        display_name='prolific_study',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

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

# Временно закомментируем middleware для теста
# MIDDLEWARE = [
#     'settings.CorsMiddleware'
# ] 
 # dict(
    #     name='intergenerational',
    #     app_sequence=['intergenerational'],
    #     display_name="""
    #     Intergenerational/evolutionary game, passing along donations to future players, 
    #     in a chain.""",
    #     num_demo_participants=6,
    # ),
    # dict(
    #     name='scheduling',
    #     display_name="Scheduling players to arrive at the same time",
    #     num_demo_participants=12,
    #     app_sequence=['scheduling_part0', 'scheduling_part1'],
    # ),
    # dict(
    #     name='supergames_indefinite',
    #     display_name="Supergames of an indefinitely repeated prisoner's dilemma",
    #     num_demo_participants=2,
    #     app_sequence=['supergames_indefinite'],
    # ),
    # dict(
    #     name='wait_page_from_scratch',
    #     display_name="Wait page implemented from scratch, using live pages.",
    #     num_demo_participants=6,
    #     app_sequence=['wait_page_from_scratch'],
    # ),
    # dict(
    #     name='fast_consensus',
    #     display_name="Fast consensus: Reach a consensus with your group before your payoffs shrink to 0.",
    #     num_demo_participants=3,
    #     app_sequence=['fast_consensus'],
    # ),
    # dict(
    #     name='bots_vs_humans',
    #     display_name="Bots playing against a human participant",
    #     num_demo_participants=1,
    #     app_sequence=['bots_vs_humans'],
    # ),
    # dict(
    #     name='crazy_eights',
    #     display_name="Card game (crazy eights)",
    #     app_sequence=['crazy_eights'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='word_search',
    #     display_name="Word search game (multiplayer)",
    #     app_sequence=['word_search'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='punishment',
    #     display_name="Public goods with punishemnt",
    #     app_sequence=['punishment'],
    #     num_demo_participants=4,
    # ),
    # dict(
    #     name='continuous_time_slider',
    #     display_name="Continuous-time public goods game with slider",
    #     app_sequence=['continuous_time_slider'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='asynchronous',
    #     app_sequence=['asynchronous'],
    #     display_name="Asynchronous 2-player game (no waiting for another player)",
    #     num_demo_participants=6,
    # ),
    # dict(
    #     name='wisconsin',
    #     display_name="Wisconsin Card Sorting Test",
    #     app_sequence=['wisconsin'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='iowa_gambling',
    #     display_name="Iowa Gambling Task",
    #     app_sequence=['iowa_gambling'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='twitter',
    #     app_sequence=['twitter'],
    #     display_name="Mini-Twitter",
    #     num_demo_participants=6,
    # ),
    # dict(
    #     name='svo',
    #     display_name="Social Value Orientation Measure (SVO)",
    #     app_sequence=['svo'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='image_annotation',
    #     display_name="Image annotation",
    #     app_sequence=['image_annotation'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='image_rating',
    #     display_name="Image rating",
    #     app_sequence=['image_rating'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='live_coordination',
    #     display_name="Live coordination (voting with chat/negotiation)",
    #     app_sequence=['live_coordination'],
    #     num_demo_participants=6,
    # ),
    # dict(
    #     name='shop',
    #     display_name="Shopping app (online grocery store)",
    #     app_sequence=['shop'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='double_auction',
    #     display_name="Double auction market",
    #     app_sequence=['double_auction'],
    #     num_demo_participants=4,
    # ),
    # dict(name='dollar_auction', app_sequence=['dollar_auction'], num_demo_participants=3),
    # dict(
    #     name='ebay',
    #     display_name="eBay style auction",
    #     app_sequence=['ebay'],
    #     num_demo_participants=3,
    # ),
    # dict(name='stroop', app_sequence=['stroop'], num_demo_participants=1),
    # dict(
    #     name='go_no_go',
    #     display_name='Attention test (Go/No-Go)',
    #     app_sequence=['go_no_go'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='choice_list',
    #     display_name='Choice list (Holt/Laury, equivalence test, etc)',
    #     app_sequence=['choice_list'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='live_bargaining',
    #     display_name="Live bargaining between 2 players",
    #     app_sequence=['live_bargaining'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='randomize_stimuli',
    #     display_name='Demo of different stimulus randomizations',
    #     app_sequence=['randomize_stimuli'],
    #     num_demo_participants=5,
    # ),
    # dict(
    #     name='bigfive',
    #     display_name='Big 5 personality test',
    #     app_sequence=['bigfive'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='panas',
    #     display_name='PANAS (positive and negative affect schedule)',
    #     app_sequence=['panas'],
    #     num_demo_participants=1,
    # ),
    # dict(
    #     name='nim',
    #     display_name="Race game / Nim (take turns adding numbers to reach a target)",
    #     app_sequence=['nim'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='read_mind_in_eyes',
    #     display_name="Reading the Mind in the Eyes Test (Baron-Cohen et al. 2001)",
    #     app_sequence=['read_mind_in_eyes'],
    #     num_demo_participants=1,