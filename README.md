# Movie Matcher

This project is a web application designed to help users discover movies. It consists of a frontend application, a backend API, and a collection of scripts for data management.

## Project Structure

The project is organized into the following main directories:

-   **`/` (root directory):** Contains the main project files, including `.gitignore`, `main.py` for starting the application, and `requirements.txt` for Python dependencies.

-   **`mm_api/`:** This directory holds the backend of the application, which is a Flask-based API. It manages data, user authentication, and movie recommendations. Key subdirectories and files include:
    -   `controllers/`: Contains the logic for handling API requests.
    -   `routes.py`: Defines the API endpoints.
    -   `movies.db`: The SQLite database for storing movie information.

-   **`mm_frontend/`:** This directory contains the frontend of the application, built with React. It provides the user interface for interacting with the Movie Matcher. Key subdirectories and files include:
    -   `src/`: Contains the source code for the React components and screens.
    -   `components/`: Reusable UI components.
    -   `screens/`: Top-level screen components.

-   **`scripts/`:** This directory includes various Python scripts for populating and maintaining the movie database. These scripts are used for tasks such as extracting movie ratings and filling the database with movie data.
