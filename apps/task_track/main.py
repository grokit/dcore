"""
# TODO

- Would be cool if generated plots with matplotlib, could make it my browser's mainpage :).

- design task_tracker.listStatTaskBoard('exer') should not be here
     should be in something like: 'local_tasks_config.py', with default as nothing.

- Would be nice if could set a targer (e.g: 3x a week or x hours) -- not all tasks require same commitment.

"""

_meta_shell_command = 'tasktrack'

import task_tracker
import time

if __name__ == '__main__':

    print('Enter in Pomodoro units')

    # task_tracker.listTasks()

    # task_tracker.listStatTaskBoard('nback')
    # task_tracker.listStatTaskBoard('jap')
    # task_tracker.listStatTaskBoard('book')
    # task_tracker.listStatTaskBoard('3tgf')
    # task_tracker.listStatTaskBoard('read')
    # task_tracker.listStatTaskBoard('social')
    # task_tracker.listStatTaskBoard('low_coffee')
    # task_tracker.listStatTaskBoard('floss')
    # task_tracker.listStatTaskBoard('knee')
    # task_tracker.listStatTaskBoard('focus_n_low_stress')
    # task_tracker.listStatTaskBoard('exer')
    task_tracker.listStatTaskBoard('medi')
    task_tracker.listStatTaskBoard('cs')
    task_tracker.listStatTaskBoard('math')

    task_tracker.enterTask()
    print("All done, keep up the good work! :)")
    time.sleep(1)
