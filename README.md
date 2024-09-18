
# Инструкция по запуску Telegram бота на VPS

## 1. Подготовка VPS

1. **Подключитесь к VPS**:
   Используйте SSH для подключения к вашему серверу. Команда:
   ```
   ssh username@your_vps_ip
   ```

2. **Обновите систему**:
   ```
   sudo apt update
   sudo apt upgrade
   ```

3. **Установите необходимые пакеты**:

   - Python и pip:
     ```
     sudo apt install python3 python3-pip
     ```

   - Установите `venv` для создания виртуального окружения (рекомендуется):
     ```
     sudo apt install python3-venv
     ```

## 2. Настройка окружения проекта

1. **Создайте директорию для проекта**:
   ```
   mkdir ~/my_telegram_bot
   cd ~/my_telegram_bot
   ```

2. **Создайте виртуальное окружение**:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Создайте файл `requirements.txt`** и добавьте зависимости:
   ```
   openai
   pyTelegramBotAPI
   python-dotenv
   ```

4. **Установите зависимости**:
   ```
   pip install -r requirements.txt
   ```

5. **Создайте файл `.env`** для хранения ключей:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

6. **Перенесите ваш скрипт бота** (например, `bot.py`) в директорию проекта.

## 3. Запуск бота

1. **Запустите скрипт бота**:
   ```
   python bot.py
   ```

## 4. Настройка автоматического запуска

1. **Создайте файл службы**:
   ```
   sudo nano /etc/systemd/system/telegram_bot.service
   ```

2. **Добавьте следующее содержимое**:
   ```
   [Unit]
   Description=Telegram ChatGPT Bot
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/home/your_username/my_telegram_bot
   ExecStart=/home/your_username/my_telegram_bot/venv/bin/python /home/your_username/my_telegram_bot/bot.py
   Restart=always
   Environment="PATH=/home/your_username/my_telegram_bot/venv/bin"
   Environment="OPENAI_API_KEY=your_openai_api_key"
   Environment="TELEGRAM_BOT_TOKEN=your_telegram_bot_token"

   [Install]
   WantedBy=multi-user.target
   ```

   Замените `your_username`, `your_openai_api_key` и `your_telegram_bot_token` на ваши значения.

3. **Перезагрузите `systemd` и запустите службу**:
   ```
   sudo systemctl daemon-reload
   sudo systemctl start telegram_bot.service
   sudo systemctl enable telegram_bot.service
   ```

4. **Проверьте статус службы**:
   ```
   sudo systemctl status telegram_bot.service
   ```

Ваш бот будет автоматически запускаться при перезагрузке сервера.
Просмотреть логи можно командой:
```
journalctl -u telegram_bot.service
```

