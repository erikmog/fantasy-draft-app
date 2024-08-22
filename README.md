# Fantasy Draft App

Welcome to the Fantasy Draft App, a Flask-based web application designed to help you with your fantasy football draft. This app provides features such as player filtering, favorites marking, and more.

## Features

- **Player Filtering:** Filter players by various attributes.
- **Favorites:** Mark players as favorites and view them in a separate table.
- **Fantasy Football Calculator API Integration:** Display data from Fantasy Football Calculator.
- **Web Scraping:** Scrape rookie details and display them on a separate page.
- **Modern Design:** Custom styling and design using Flask templates and CSS.

## Installation

To get started with the project, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/fantasy-draft-app.git
    cd fantasy-draft-app
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root of the project and add the necessary environment variables:

    ```bash
    FLASK_APP=app.py
    FLASK_ENV=development
    ```

5. **Run the application:**

    ```bash
    flask run
    ```

6. **Access the app:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

- Use the home page to browse players and apply filters.
- Mark players as favorites by clicking the star icon.
- Access the rookie details on the "Rookies" page.
- View ADP data fetched from Fantasy Football Calculator.

## Technologies Used

- **Flask**: The web framework used.
- **SQLite**: Database for storing player data.
- **HTML/CSS**: For the front-end design.
- **JavaScript**: For interactive elements.
- **Python**: The programming language used for back-end logic.
- **Terraform**: Used for deploying the app to Azure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Fantasy Football Calculator for the API.
- DraftSharks for rookie data scraping.

