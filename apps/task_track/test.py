
import task_tracker


def test_statboard():
    task_tracker.listStatTaskBoard('jap')
    task_tracker.listStatTaskBoard('nback')
    task_tracker.listStatTaskBoard('backe')


def test_listtasks():
    task_tracker.listTasks()


def test_entertask():
    task_tracker.enterTask('automatically_entered_test_task',
                           1.234,
                           'No comment is a kind of comment.')

if __name__ == '__main__':
    test_entertask()
    test_listtasks()
    test_statboard()
