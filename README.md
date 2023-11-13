# Guider

## Installation

Guider is created entirely using Django and it comes as a batteries included package. In essence, you need only this repo to get setup and running. Guider uses Postgres as it's primary database, but don't  worry you don't have to install and configure postgres as there is a docker-compose included that will take care of setting up the DB with required users and other configs.

### Steps

1) Clone this repo
    ```bash
    git clone https://github.com/rohittp0/guider.git
    ```
2) Create a venv and activate it
    - Linux / MacOs
    ```bash
   python3 -m venv venv
   ./venv/bin/activate
   ```
   - Windows
   ```
   python3 -m venv venv
   venv\Scripts\activate
   ```
3) Install dependencies
    ```bash
   pip install -r requirements.txt
    ```
4) Rename the .env.example to .env and edit the values in it
5) Set up the database
    ```bash
   docker-compose up -d
    ```
6) Apply migrations
    ```bash
   python manage.py migrate
   ```
7) Enable sign in with Google ( Optional )
    ```bash
    python manage.py createsocial
    ```
8) Create an admin user account
    ```bash
   python manage.py createsuperuser
   ```
   
That's it, now you should be able to start Guider by running,
```bash
python manage.py runserver
```

Open http://localhost:8000 in your browser

## Questions and Feedback
If you are facing any problem feel free to open an issue or mail me a stack overflow question with `guider` as the tag. All pull requests are always welcome.

## Contact Me

**Mail me @**  [tprohit9@gmail.com](mailto:tprohit9@gmail.com)

**Catch me on**  [Stackoverflow](https://stackoverflow.com/users/10182024/rohi)

**Check out my YouTube**  [Channel](https://www.youtube.com/channel/UCVRdZwluF8jYXSIaHBqK73w)

**Follow me on**  [Instagram](https://www.instagram.com/rohit_pnr/)
