"""
Модуль распределения задач.

модуль распределения обращается к таблице task2user - ищет задачу со статусом free.
в результате работы модуля задаче сопоставляется единственный пользователь,
модуль меняет статус на inwork и заменяет список возможных пользователей на единственного.
клиент выполнив задачу меняет статус на done
"""

cursor_task = 1 # курсор на task2user
cursor_user = 2 # курсор на БД юхеров (или альтернативный список юзеров онлайн)


def get_task_from_database(cursor_task):
    """
    Получение задачи из task2user со статусом 'free'
    :param cursor_task: курсор на task2user
    :return: нераспределенная задача
            (id_task - id задачи,
            name_task - имя задачи,
            user_task - назначенный для решения пользователь (name_user, None),
            status_task - статус задачи (free, in_work, done))
    """
    cursor_task.execute('SELECT * FROM task2user LIMIT 1'
                        'WHERE status_task=free')

    tasks = cursor_task.fetchall()
    return tasks


def get_list_free_users_online(cursor_user):
    """
    Получение списка юзеров онлайн из ...
    :param cursor_user: курсор на ...
    :return: список юзеров онлайн
            (session_id - id юзера (если есть id - юзер online),
            status_user - статус юзера (free, working))
    """
    cursor_user.execute('SELECT * FROM ...'
                        'WHERE session_id IS NOT NULL'
                        'AND status_user=free')

    users_online = cursor_user.fetchall()
    return users_online


def update_task(task_id, task_status):
    """
    Обновление статуса задачи в task2user
    :param task_id: id назначенной задачи
    :param task_status: статус задачи (in_work, done)
    """
    cursor_task.execute('UPDATE task2user'
                        'SET status_task=?'
                        'WHERE id_task=?', (task_status, task_id, ))
    cursor_task.commit()


def distribution_task(possible_users_list):
    """
    Сопоставление задачи конкретному пользователю
    :param possible_users_list: список возможных пользователей для решения задачи
    :return: задача ставится в очередь при успешном назначении юзера, иначе - 0
    """
    task = get_task_from_database(cursor_task)
    users_online = get_list_free_users_online(cursor_user)
    for user in users_online:
        if user in possible_users_list:
            task.user_task = user
            task.status_task = 'in_work'
            user.status_user = 'working'
            possible_users_list = user # обновить список возможных пользователей
            update_task('in_work', task.id_task)
            # ф-я отправки task в rabbit
            return task
        else:
            print('Нет свободных юзеров для решения задачи.')
    return 0
