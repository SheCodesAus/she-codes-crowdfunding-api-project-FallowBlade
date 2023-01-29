# Rejuvinature

Crowdfunding project for community-conscious individuals looking to rejuvinate unloved public open greenspace.
​
## Features
​
### User Accounts
​
- [X] Username
- [X] Email Address
- [X] Password
​
### Project
​
- [X] Create a project
  - [X] Title
  - [X] Owner (a user)
  - [X] Description
  - [X] Image
  - [X] Target Amount to Fundraise
  - [X] Open/Close (Accepting new supporters)
  - [X] When was the project created
- [X] Ability to pledge to a project
  - [X] An amount
  - [X] The project the pledge is for
  - [X] The supporter
  - [X] Whether the pledge is anonymous
  - [X] A comment to go with the pledge
  
### Implement suitable update delete
​
**Note: Not all of these may be required for your project, if you have not included one of these please justify why.**
​
- Project
  - [X] Create
  - [X] Retrieve
  - [X] Update
  - [X] Destroy

- Pledge
  - [X] Create
  - [X] Retrieve
  - [X] Update
  - [X] Destroy - I wanted to try and set this to be only the Project Owner could delete a pledge linked to a project, but ran into issues trying to get this to work :(

- User
  - [X] Create
  - [X] Retrieve
  - [X] Update
  - [ ] Destroy - did not include as did not want user to be able to delete (would need to manage cascades/data retention and ran out of time to consider how to account for this).
​
### Implement suitable permissions
​
**Note: Not all of these may be required for your project, if you have not included one of these please justify why.**
​
- Project
  - [X] Limit who can create - only users can create a project
  - [ ] Limit who can retrieve - no necessary, as want everyone to be able to view the projects.
  - [X] Limit who can update 
  - [X] Limit who can delete 
- Pledge
  - [X] Limit who can create - implemented anonymous and non-anonymous create option
  - [X] Limit who can retrieve - anyone can get the pledge lists
  - [X] Limit who can update - only supporters can update
  - [ ] Limit who can delete - wanted to limit this to project owners, but unable to figure out how to create. Currently delete for all users.
- User
  - [X] Limit who can retrieve
  - [X] Limit who can update
  - [] Limit who can delete - did not implement this. Unsure of data and security protocol for deletion of a users (i.e. what happens to their committed pledges, projects, etc.? Should I have them cascade, or should I set them to be full)
​
### Implement relevant status codes
​
- [X] Get returns 200
- [X] Create returns 201
- [X] Not found returns 404
​
### Handle failed requests gracefully 
​
- [X] 404 response returns JSON rather than text
​
### Use token authentication
​
- [X] impliment /api-token-auth/
​
## Additional features
​
- [X] SearchAPI Feature
​
Apply this API & View to search for a project based on the project title or description. Functions as a GET, which calls a query that you are setting the parameter for. For example, mine is set to "title" and "search" within all projects, so when you type your keyword/value, it will only search those fields for a corresponding word. Note I have not set a contains, onlycontains, etc. rule for this feature, so it has limitations in that it is broad-based search of strings.
​
- [X] Filter by owner or is_open fields

This feature sits within the ProjectList view. It allows us to filter projects based on whether or not a project is open or closed.
​
- [X] Category Feature
​
This feature creates project categories with a name, unique ID and slug(URL-friendly name convention for calling at later stage).

- [X] Ben's Bonus Totals Feature
​
This feature creates an aggregate sum of all pledges against a project, and returns a total of those against an individual project.

- [X] Pagination Feature 

Not sure if this counts as a feature, but i've added a pagination rule where if the count of projects in project list view is >5, then a new page for viewing the next 5 projects is generated.
​
​
### External libraries used
​
- [X] django-filter
​
​
## Part A Submission
​
- [ ] A link to the deployed project. 
- [ ] A screenshot of Insomnia, demonstrating a successful GET method for any endpoint.
- [X] A screenshot of Insomnia, demonstrating a successful POST method for any endpoint.
- [X] A screenshot of Insomnia, demonstrating a token being returned. see 
- [ ] Your refined API specification and Database Schema. - Link here: 
​
### Step by step instructions for how to register a new user and create a new project (i.e. endpoints and body data).
​
1. Create User
​
```shell
curl --request POST \
  --url http://wild-glade-7116/users/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": <insertusername>
	"email": <insertemail>
	"password": <insertpassword>
}
```
​
2. Sign in User
​
```shell
curl --request POST \
  --url http://127.0.0.1:8000/api-token-auth/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "testuser",
	"password": "not-my-password"
}'
```
​
3. Create Project
​
```shell
curl --request POST \
  --url http://127.0.0.1:8000/projects/ \
  --header 'Authorization: Token 5b8c82ec35c8e8cb1fac24f8eb6d480a367f322a' \
  --header 'Content-Type: application/json' \
  --data '{
	"title": "Donate a cat",
	"description": "Please help, we need a cat for she codes plus, our class lacks meows.",
	"goal": 1,
	"image": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Dollar_bill_and_small_change.jpg",
	"is_open": true,
	"date_created": "2023-01-28T05:53:46.113Z"
}

