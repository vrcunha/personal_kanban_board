import json
import string
from datetime import datetime
from random import choice

def make_uuid():
    chars = string.digits+string.ascii_letters+string.punctuation
    uuid = [choice(chars) for i in range(5)]
    return ''.join(uuid)

def load_states():
    try:
        with open('task_state.json') as f:
            task_state = json.load(f)
    except FileNotFoundError:
        with open('task_state.json', 'w') as f:
            pass
    
def save_task_status():
    task_state = {
        'todo': todo,
        'in_progress': in_progress,
        'done': done
        }
    
    with open('task_state.json', 'w') as f:
        json.dump(task_state, f, ensure_ascii=False, indent=4)

load_states()

# todo = dict()
# in_progress = dict()
# done = dict()

# while True:
#     task = input('Insira uma tarefa: ')
#     if len(task) == 0:
#         break
#     todo[make_uuid()] = {
#         'task': task, 
#         'metadata': {
#             'creation_time': datetime.now().timestamp(),
#             'modification_time': datetime.now().timestamp(),
#             'finalization_time': None
#             }
#         }


# save_task_status()