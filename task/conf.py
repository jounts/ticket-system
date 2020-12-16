"""
Configfile for task application
"""

# table
TASK_TABLE_NAME: str = 'tasks'
AUTH_TABLE_NAME: str = 'auth_user'
# fields
TASK_F_ID: str = 'id'
TASK_F_NAME: str = 'name'
TASK_F_LEVEL: str = 'level'
TASK_F_USER: str = 'user_execs'
TASK_F_STATUS: str = 'status'
AUTH_F_USERNAME: str = 'username'
AUTH_F_SKILL: str = 'skill_lvl'
# test user
TEST_KEY: bool = True
NAME: str = 'test_task2'
LEVEL: int = 3
USER: tuple = ['test3','test4',]
STATUS: str = 'free'