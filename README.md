# Backend - CMS (ClinicAI)

Backend for ClinicAI, the Clinical Management System.

## Description
Backend for ClinicAI, the Clinical Management System. Holds database models, urls and APIs.

 The backend is **hosted live** at "http://backend-cms3.eba-fdjnmcbd.ap-southeast-1.elasticbeanstalk.com/api/docs/" ⚠️
### Technologies used:
- Python >= 3.8.0
- Django >= 3.2.4
- Django Rest Framework >= 3.12.4
- Django Environ >= 0.9.0
- Psycopg2 >= 2.8.6

## Visuals (*TODO*)
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
1. Clone project using HTTPS
2. Create a virtual environment in the root and activate it
    ```bash
    python -m venv .venv
    .venv\scripts\activate
    ```
3. Upgrade pip to latest version
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Read the `engine.md` file in `/voice_recognition/engine/`. Follow instructions to download the .pbmm and .scorer files
6. Create .env file in `/backend_cms` (ask @ashr0008 for contents of .env file). The project cannot be served locally unless this .env file is present. 
7. Use the same migration files available in the repo. Don't run make migrations!
8. Migrate database with latest changes (from migration files). You can check the database at this point.
    ```bash
    python manage.py migrate
    ```
9. Start the server
    ```bash
    python manage.py runserver
    ```



## Usage
Localhost backend server will be live at http://127.0.0.1:8000/

All api endpoints are at `api/`

API documentation is at `/api/docs`

Query Params for the Appointment API:
- `api/appointment/appointments?status=unattended` -> returns all unattended appointments
- `api/appointment/appointments?status=attended` -> returns all attended appointments
- `api/appointment/appointments` -> returns all appointments (attended + unattended)

Voice recognition api is at `api/stt`. Must include the following in the POST request header:

`Content-Disposition: attachment; filename="speech.wav"`

When debugging the frontend mobile application, execute the following command to allow communication between the locally hosted Django server with other devices within the same network (LAN).
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

## Authors and acknowledgment
- Abhishek Shrestha
- Isaac Lee Kian Min
- Lee Zi Yan

## Project status

There will be **no more updates** to this repo in the future. All project requirements have been met. 

Status: Complete ✅
