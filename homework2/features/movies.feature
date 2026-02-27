Feature: Movie Listings
    As a user
    I want to view available movies
    So that I can decide what to book

    Scenario: view all movies
        Given the database has movies
        when I request the movie Listings
        Then I should recieve a 200 status code
        and the response I should contian movie titles
        