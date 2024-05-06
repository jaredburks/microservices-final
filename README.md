# microservices-final

App description:
This app (app.py) is an image dataset genertor. It was created to facilitate making datasets for computer vision models.
Users name the dataset directory and 2 subdirectories within it. This allows users to specifiy labels for classification. 
Other features include account registration, login, signing out, and an admin endpoint that displays usage statistics.
Dataset names have a "_dataset" suffix when they are downloaded.
NOTE: This app is intended for images to be uploaded but there is currently not limit on the file type used.

Installation:
This app's dependencies are listed in the requirements.txt.
Locust is not necessary and is only used for load testing.
After cloning this repo, run the app by using the flask run command.
This app was developed using WSL. 

Documentation:
Endpoint:
'/' - Where users can register for an account, login, enter names for a dataset and 2 subdirectories, select photos to upload via 2 "Choose Files" buttons.
'/upload' - Not accessible in browser. Only used for dataset generation logic.
'/register' - Sign up for an account by providing a username and password. NOTE: Cannot register duplicate usernames. 
'/login' - Input username and password for signing in registered users.
'/logout' - Logs out current user.
'/admin' - Provides usage statistics (current user logged in, requested endpoint, method, timestamp, and http reponse status code) for each endpoint. Only accessed via logged in users.

All fields in the html forms must be filled out or you will be prompted with an error or alert. 
The database only save account information after registering a username and password.
Datasets are sent directly to the client after clicking "Upload Files" as an archived folder (e.g., images_dataset.zip).
NOTE: zipped files are saved to the root directory of the project as well as sent as an attachment to be downloaded.

Use case:
Create a dataset with structured subdirectories containing images as input for computer vision models (e.g., image classification).
As the app is currently, users can utilize this app as a general file organizer since there is not restriction on file types (MIMETYPE). 
