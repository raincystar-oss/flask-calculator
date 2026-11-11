# Калькулятор на Flask и Docker

Приложение состоит из Flask API и отдельного веб-интерфейса на Nginx. В Docker Compose Nginx пересылает запросы `/api/` к сервису `backend` по внутренней сети. Flask доступен на порту 5000, интерфейс — на 18085.

## Подготовка

1. Установите и запустите Docker Desktop. Дождитесь, пока движок запустится (Engine running); выберите Linux containers, если требуется.
2. Откройте PowerShell в папке `flask-calculator`. Например, в Проводнике откройте эту папку, введите `powershell` в адресной строке и нажмите Enter.
3. Проверьте `docker --version` и `docker info`. Вторая команда должна показать сведения о сервере Docker без ошибки.

## Вариант 1. Только Flask, как в задании

```powershell
docker build -t my-flask-app .
docker run -d --name flask-calculator -p 5000:5000 my-flask-app
docker ps
```

Откройте http://localhost:5000/ и http://localhost:5000/info — вы увидите ответы JSON. Для сложения откройте http://localhost:5000/calc/12/3?operation=%2B (знак `+` в URL записывается как `%2B`). Например, результат будет `15.0`. Также доступны действия `-`, `*`, `/` в параметре `operation`; без параметра выполняется сложение. При делении на ноль сервер вернёт ошибку.

Перед запуском Compose остановите и удалите одиночный контейнер, чтобы освободить порт 5000:

```powershell
docker stop flask-calculator
docker rm flask-calculator
```

## Вариант 2. Flask и веб-интерфейс через Compose

Из той же папки выполните:

```powershell
docker compose up -d --build
docker compose ps
```

Откройте http://localhost:18085, введите два числа, выберите действие и нажмите «Посчитать». Проверьте, например, что 12 / 3 даёт 4, а деление на 0 показывает ошибку. Сам API также доступен по адресу http://localhost:5000/info.

В браузере запрос идёт на `/api/calc/...` к Nginx, а Nginx передаёт его на `backend:5000/calc/...` внутри сети Compose. Адрес `backend` работает внутри этой сети, а не в браузере на компьютере.

Для просмотра журналов и остановки:

```powershell
docker compose logs
docker compose down
```

Если порт 5000 или 18085 занят, остановите использующее его приложение либо измените левую часть соответствующего сопоставления `ports` в `docker-compose.yml` и используйте новый порт в браузере. Если контейнер не запустился, проверьте `docker compose logs` и состояние Docker Desktop. Для повторной сборки после изменения файлов снова выполните `docker compose up -d --build`.

Для сдачи можно заархивировать папку `flask-calculator` или сделать скриншоты страницы калькулятора и работающих контейнеров в Docker Desktop.
