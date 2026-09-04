Created a folder to for mini project with the name miniprojectmyname
create the following files inside it
    client.py
        -- wrote the main code inside this file 
    .env    
        -- placed the bearer token here
    .gitignore
        -- placed the .env file inside it to not to track the .env file by git
    requirements.txt 
        -- placed the requests dependency inside it and for version I ran the command pip show requests reports

To get the post by id I have placed the id inside the base url as end-point as mentioned in API Guide GET api/v1/posts/{id} — get one post

To update the post I followed with PUT / PATCH /api/v1/posts/{id} — update a post as mentioned in API guide

For Delete feature I followed DELETE /api/v1/posts/{id} — delete a post

For every feature implementation I ran git commit 

## AI Usage 
Used claude code to handle the exception handling as I'm not able to figure where to use it whether inside each method of during the implementation. hence generated the exception handling using claude code