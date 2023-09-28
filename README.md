# Capstone Project Proposal - Sky Time

## Title: Sky Time
The website is hosted at [Sky Time Website](https://sky-time.onrender.com)

## Goal of the Website
The main goal of this application is to provide users with information about the Sun and Moon at the requested time, including sunrise, sunset, day length, moonrise, and moonset.

## Demographic of Users
This website targets anyone who wants to plan their activities, such as fishing, weight loss (moon diet), photography during the "golden hour," hiking, or simply enjoying a specific sunrise or sunset.

## Data to be Used
The Astronomy API from https://ipgeolocation.io/documentation/astronomy-api.html will be used to retrieve the location-based rise and set times for both the Sun and Moon.

## Approach to Creating the Project
### Database Schema
A database schema to store user information, location information, and other necessary data.
https://dbdiagram.io/d/644b8383dca9fb07c431cd24

### Possible Issues
The API data may not always be accurate due to atmospheric conditions, precision of location data, or different time zones. Additionally, if the API's external data sources have issues, it will affect the API itself.

### Sensitive Information to Secure
Users' passwords will be hashed using a secure hashing algorithm when they create or update their accounts.

## Features
The website implements the following features:
1. **User Authentication**: Users can sign up and log in to access personalized features.
2. **Location Search**: Users can search for specific locations to retrieve astronomical data.
3. **Location Saving**: Users can save their preferred locations for quick access to data.
4. **View Favorites**: Users can view their last 5 different searches.

## User Flow
The standard user flow on the website is as follows:
1. **Homepage**: Users arrive at the homepage.
2. **Sign Up/Log In**: Users can sign up or log in to access personalized features.
3. **Location Search**: Users can search for a location to get Sun and Moon data.
4. **View Favorites**: Users can view their last 5 different searches.
5. **Log Out**: Users can log out to end their session.

## Technology Stack
The website is built using:
- Flask (Python web framework)
- PostgreSQL (Database)
- HTML, CSS, JavaScript (Front-end)


