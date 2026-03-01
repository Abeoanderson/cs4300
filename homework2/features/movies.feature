Feature: Movie Listings
    As a user
    I want to view available movies
     So that I can decide what to book

     Scenario: view all movies
        Given the database has movies
        When I request the movie list                    
        Then I should receive a 200 status code          
        And the response should contain movie titles     