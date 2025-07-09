```python

import requests
import subprocess
import time
import git
import os
import sys

# !!! ВАЖНО: ЗАМЕНИТЕ ЭТИ ЗНАЧЕНИЯ НА СВОИ !!!
GITHUB_TOKEN = "github_pat"  # Ваш персональный токен доступа GitHub (с правом repo)
REPO_OWNER = "REPO_OWNER"      # Ваше имя пользователя на GitHub
REPO_NAME = "Jarvis"          # Название вашего репозитория Jarvis
BRANCH_NAME = "main"              # Название основной ветки (может быть "master")
REPO_PATH = "/Users/Users/pythonProject"

def check_for_updates():
    """Проверяет наличие новых коммитов в удаленном репозитории GitHub."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = 'https://github.com/prem1umservice/Jarvis/tree/main'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Вызывает исключение для HTTP ошибок (4xx или 5xx)
        data = response.json()
        latest_commit_sha = data['sha']
        return latest_commit_sha
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при проверке обновлений: {e}")
        return None

def pull_latest_code():
    """Получает последние изменения из удаленного репозитория."""
    try:
        repo = git.Repo(REPO_PATH)
        origin = repo.remote(name='origin')
        pull_info = origin.pull()
        if pull_info and not pull_info[0].flags & git.remote.common.FetchInfo.NEW_HEAD:
            print("Локальный репозиторий уже обновлен.")
            return False
        elif pull_info and pull_info[0].flags & git.remote.common.FetchInfo.NEW_HEAD:
            print("Получены последние изменения из репозитория.")
            return True
        else:
            print("Не удалось получить обновления (возможно, нет изменений).")
            return False
    except git.InvalidGitRepositoryError:
        print(f"Неверный путь к репозиторию: {REPO_PATH}. Убедитесь, что это правильный путь к клонированному репозиторию.")
        return False
    except Exception as e:
        print(f"Ошибка при выполнении git pull: {e}")
        return False

def restart_jarvis():
    """Перезапускает основной скрипт Jarvis."""
    print("Перезапускаю Джарвис...")
    # !!! ВАЖНО: Укажите здесь команду для запуска вашего основного скрипта Jarvis !!!
    # Предполагается, что ваш основной скрипт называется, например, 'jarvis.py'
    try:
        subprocess.Popen(['python', 'jarvis.py'])  # Запускаем новый процесс
        print("Джарвис перезапущен.")
        sys.exit(0) # Завершаем текущий скрипт обновления
    except FileNotFoundError:
        print("Ошибка: Файл 'jarvis.py' не найден. Убедитесь, что основной скрипт находится в той же директории или укажите правильный путь.")
    except Exception as e:
        print(f"Ошибка при перезапуске Джарвиса: {e}")

if __name__ == "__main__":
    # Убедимся, что путь к репозиторию существует
    if not os.path.isdir(REPO_PATH):
        print(f"Ошибка: Указанный путь к репозиторию не существует: {REPO_PATH}")
        sys.exit(1)

    try:
        # Попытаемся инициализировать репозиторий, если его еще нет
        repo = git.Repo(REPO_PATH)
    except git.InvalidGitRepositoryError:
        print(f"Репозиторий по пути {REPO_PATH} не является корректным Git-репозиторием. Пожалуйста, клонируйте репозиторий вручную.")
        sys.exit(1)

    last_known_commit = None
    print("Скрипт слежения за обновлениями запущен.")
    while True:
        latest_commit = check_for_updates()
        if latest_commit and latest_commit != last_known_commit:
            print(f"Обнаружено новое обновление: {latest_commit}")
            if pull_latest_code():
                restart_jarvis()
            last_known_commit = latest_commit
        elif latest_commit:
            print("Нет новых обновлений.")
        else:
            print("Не удалось проверить обновления. Повторная попытка через 60 секунд.")

        time.sleep(60) # Проверять обновления раз в минуту
```
