from otree.api import *
try:
    import pylink
except ImportError:
    print("Error: pylink not found. Make sure EyeLink SDK is installed and PYTHONPATH is set correctly")
    # Можно добавить fallback режим или вызвать исключение
    raise

doc = """
Go/No-go
"""


class C(BaseConstants):
    NAME_IN_URL = 'go_no_go'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    RED_IMAGES = [0, 4, 8, 17]
    NUM_IMAGES = 10  # actually there are 20 images but we just show 10 for brevity
    NUM_TRIALS = NUM_IMAGES // 2  # количество пар изображений
    
    # Eye-link settings
    EYELINK_IP = '10.1.1.7'
    EYELINK_PORT = 50589  # Добавляем порт
    DUMMY_MODE = False  # Set True for testing without actual eye tracker

# Глобальная переменная для хранения соединения с eye tracker
el_tracker = None

def initialize_eyelink():
    global el_tracker
    if el_tracker is None:
        try:
            print("Available pylink attributes:", dir(pylink))
            print(f"Attempting to connect to EyeLink at {C.EYELINK_IP}:{C.EYELINK_PORT}")
            
            if C.DUMMY_MODE:
                el_tracker = pylink.TCPLink(None, C.EYELINK_PORT)
            else:
                el_tracker = pylink.TCPLink(C.EYELINK_IP, C.EYELINK_PORT)
            
            # Пробуем получить информацию о соединении
            try:
                print("Connection info:", el_tracker.getsockname())
                print("Peer info:", el_tracker.getpeername())
            except:
                print("Could not get connection details")
                
            print("Successfully connected to EyeLink")
            return True
        except Exception as e:
            print(f"Error connecting to EyeLink: {type(e).__name__} - {str(e)}")
            print("Available pylink attributes:", dir(pylink))
            return False

def send_to_eye_link(message):
    global el_tracker
    print(f"Attempting to send message to EyeLink: {message}")
    try:
        if el_tracker is None:
            if not initialize_eyelink():
                print("Failed to initialize EyeLink connection")
                return
                
        # Используем правильный метод sendMessage
        el_tracker.sendMessage(message)
        print(f"Successfully sent message to EyeLink")
    except Exception as e:
        print(f"Error sending message to EyeLink: {type(e).__name__} - {str(e)}")


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    # Инициализируем соединение с EyeLink
    if subsession.round_number == 1:  # только в первом раунде
        initialize_eyelink()
        
    for p in subsession.get_players():
        participant = p.participant
        image_pairs = generate_ordering()
        for left_id, right_id in image_pairs:
            left_is_red = left_id in C.RED_IMAGES
            right_is_red = right_id in C.RED_IMAGES
            Trial.create(
                player=p,
                left_image_id=left_id,
                right_image_id=right_id,
                left_is_red=left_is_red,
                right_is_red=right_is_red
            )
        participant.reaction_times = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_completed = models.IntegerField(initial=0)
    num_errors = models.IntegerField(initial=0)
    avg_reaction_ms = models.FloatField()


def get_current_trial(player: Player):
    return Trial.filter(player=player, is_error=None)[0]


def is_finished(player: Player):
    return player.num_completed >= C.NUM_TRIALS


class Trial(ExtraModel):
    player = models.Link(Player)
    reaction_ms = models.IntegerField()
    left_image_id = models.IntegerField()
    right_image_id = models.IntegerField()
    left_is_red = models.BooleanField()
    right_is_red = models.BooleanField()
    is_error = models.BooleanField()
    pressed = models.BooleanField()


def generate_ordering():
    import random
    numbers = list(range(C.NUM_IMAGES))
    random.shuffle(numbers)
    # Убедимся, что у нас четное количество изображений
    if len(numbers) % 2 != 0:
        numbers = numbers[:-1]
    # Генерируем пары изображений
    pairs = []
    for i in range(0, len(numbers), 2):
        pairs.append((numbers[i], numbers[i+1]))
    return pairs


# PAGES
class Introduction(Page):
    pass


class Task(Page):
    @staticmethod
    def live_method(player: Player, data):
        print(f"Received data in live_method: {data}")  # Отладочное сообщение
        
        # Если получили пустое сообщение при инициализации
        if not data:
            trials = Trial.filter(player=player, is_error=None)
            if not trials:
                print("No trials available at initialization")
                return {player.id_in_group: dict(is_finished=True)}
                
            trial = trials[0]
            print(f"Initializing first trial: left={trial.left_image_id}, right={trial.right_image_id}")
            return {
                player.id_in_group: dict(
                    left_image_id=trial.left_image_id,
                    right_image_id=trial.right_image_id,
                    feedback='',
                    trialId=trial.id
                )
            }

        # Обработка сообщений для eye-link
        if data.get('type') == 'eye_link':
            print(f"Received eye-link message from frontend: {data}")
            send_to_eye_link(data['message'])
            return

        # Обработка обновлений триала
        if data.get('type') == 'trial_update':
            print(f"Received trial update: {data}")
            participant = player.participant
            if 'pressed' in data:
                trials = Trial.filter(player=player, is_error=None)
                if not trials:
                    print("No more trials available")
                    return {player.id_in_group: dict(is_finished=True)}
                    
                trial = trials[0]
                if (data['left_image_id'] != trial.left_image_id or 
                    data['right_image_id'] != trial.right_image_id):
                    print(f"Trial ID mismatch. Expected: {trial.left_image_id},{trial.right_image_id}, Got: {data['left_image_id']},{data['right_image_id']}")
                    return
                    
                has_green = (not trial.left_is_red) or (not trial.right_is_red)
                trial.is_error = has_green != data['pressed']
                
                if trial.is_error:
                    feedback = '✗'
                    player.num_errors += 1
                    print(f"Error recorded. Total errors: {player.num_errors}")
                else:
                    feedback = '✓'
                    if has_green:
                        trial.reaction_ms = data['answered_timestamp'] - data['displayed_timestamp']
                        participant.reaction_times.append(trial.reaction_ms)
                        print(f"Correct response. Reaction time: {trial.reaction_ms}ms")
                player.num_completed += 1
                print(f"Completed trials: {player.num_completed}/{C.NUM_TRIALS}")
                
                if is_finished(player):
                    print("All trials completed")
                    return {player.id_in_group: dict(is_finished=True)}
                    
                # Получаем следующий триал сразу после обработки текущего
                next_trials = Trial.filter(player=player, is_error=None)
                if not next_trials:
                    print("No more trials available")
                    return {player.id_in_group: dict(is_finished=True)}
                
                next_trial = next_trials[0]
                print(f"Sending next trial with feedback: left={next_trial.left_image_id}, right={next_trial.right_image_id}")
                return {
                    player.id_in_group: dict(
                        left_image_id=next_trial.left_image_id,
                        right_image_id=next_trial.right_image_id,
                        feedback=feedback,
                        trialId=next_trial.id
                    )
                }

            # Если pressed=false (таймаут)
            trials = Trial.filter(player=player, is_error=None)
            if not trials:
                print("No more trials available")
                return {player.id_in_group: dict(is_finished=True)}
            
            trial = trials[0]
            print(f"Sending next trial after timeout: left={trial.left_image_id}, right={trial.right_image_id}")
            return {
                player.id_in_group: dict(
                    left_image_id=trial.left_image_id,
                    right_image_id=trial.right_image_id,
                    feedback='',
                    trialId=trial.id
                )
            }

    @staticmethod
    def vars_for_template(player: Player):
        image_paths = [
            'go_no_go/{}.png'.format(image_id) for image_id in range(C.NUM_IMAGES)
        ]

        return dict(image_paths=image_paths)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import statistics

        # if the participant never pressed, this list will be empty
        if participant.reaction_times:
            avg_reaction = statistics.mean(participant.reaction_times)
            player.avg_reaction_ms = int(avg_reaction)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(avg_reaction_ms=player.field_maybe_none('avg_reaction_ms'))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        global el_tracker
        if player.round_number == C.NUM_ROUNDS:  # только в последнем раунде
            if el_tracker is not None:
                try:
                    el_tracker.close()
                    print("EyeLink connection closed")
                except:
                    print("Error closing EyeLink connection")
                finally:
                    el_tracker = None


page_sequence = [Introduction, Task, Results]
