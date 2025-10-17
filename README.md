# Movie Matcher

This project is a web application designed to help users discover movies. It consists of a frontend application, a backend API, and a collection of scripts for data management.

## Project Structure

The project is organized into the following main directories:

-   **`mm_api/`:** This directory holds the backend of the application, which is a Flask-based API. It manages data, user authentication, and movie recommendations. Key subdirectories and files include:
    -   `controllers/`: Contains the logic for handling API requests.
    -   `routes.py`: Defines the API endpoints.
    -   `movies.db`: The SQLite database for storing movie information.

-   **`mm_frontend/`:** This directory contains the frontend of the application, built with React. It provides the user interface for interacting with the Movie Matcher. Key subdirectories and files include:
    -   `components/`: Reusable UI components such as auth-forms, and movie detail cards.
    -   `screens/`: Top-level screen components such as a swipable list of movie cards.

-   **`scripts/`:** This directory includes various Python scripts for populating and maintaining the movie database. These scripts are used for tasks such as extracting movie ratings and filling the database with movie data.

## Recommendation Algorithms
 1. `User Recommendations`: This is a content-based system. It recommends movies to a user by finding movies that are similar to ones they've
  already liked. The similarity is calculated based on the movie's plot description, genres, director, and actors.

2. `Group Recommendations`: This builds on the user recommendations. For a group, it creates a shared "stack" of movies. This stack is filled
  with movies that are similar to what the group members have collectively liked, plus some random movies to introduce variety. Each member of
  the group can then see and rate movies from this shared stack.
