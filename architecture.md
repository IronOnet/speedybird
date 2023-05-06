# Architecture Notes 

=> Speedybird is a microbloging web app similar to twitter 

## Features: 
    - Read tweets from the newsfeed
    - Comment on tweets 
    - Post tweets 
    - A tweet can contain media content 
    - A tweet can contain external links 
    - A tweet can contain #tags 
    - A user can follow other users 
    - A user can be followed by other users 


## System API 

- /api/v1/tweets/{:me}/ 
    - GET: 
      - return a list of tweets made by the current users 

    - POST: 
      - create a new tweet by the current user

- /api/v1/tweets/ 
  - GET: 
    - return a list of all the tweets made

- api/v1/tweet/{id}/ 
  - GET 
    - return a single tweet by it's ID 

  - DELETE 
    - delete a tweet by its ID

- /api/v1/feed/{:me}/ 
  - GET: 
    - return a list of tweets sorted in reversed chronological order 