
# MediaUploadX
MediaUploadX is a web application that empowers users to upload and share their media content, including videos and photos, in a seamless and user-friendly manner. The platform serves as a central hub for content creators, vloggers, and anyone passionate about sharing their visual experiences with the world. With MediaUploadX, users can effortlessly upload their videos and photos, manage their media library, and enjoy a smooth playback experience.
## Tech Stack

- **Backend**: Django, Django Rest Framework, Django ORM, Django Channels, Token-based Authentication
- **Frontend**: Vue.js, Vuex, Axios, Bootstrap, Custom CSS
- **Database**: PostgreSQL


## Features

- **User Authentication**: MediaUploadX incorporates a secure user authentication system, ensuring that only authorized users can upload and access their content.

- **Video Upload**: Users can easily upload their videos to the platform using a straightforward and intuitive interface. The application supports various video formats for maximum flexibility.

- **Media Management**: The platform offers a comprehensive media management system, enabling users to organize their uploaded videos efficiently.

- **Video Playback**: MediaUploadX provides a smooth and responsive video playback feature, ensuring users can enjoy their content without interruptions.

- **User Profiles**: Each user has a personalized profile page, showcasing their uploaded videos and offering an easy way for others to discover their content.

- **Search and Filters**: Users can search for specific videos or use filters to explore content by categories, upload date, or user.

- **RESTful API**: The Django Rest Framework enables the development of a powerful and easy-to-use API for seamless interaction with the frontend.

- **Database** : The application uses a relational database (e.g., PostgreSQL) to store user data, media metadata, and other relevant information.



## Run Locally

Clone the project

```bash
  git clone https://github.com/pnaskardev/MediaUploadX.git
```

Go to the project directory

```bash
cd CircleUp
```
Install venv

```bash
pip install venv
```

Create a python virtual environement

```bash
python -m venv venv
```

Start the virtual environement

```bash
venv\Scripts\activate
```

install required packages

```bash
pip install -r requirements.txt
```
Create and migrate the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
Start the Server
```bash
python manage.py runserver
```

**In a seperate terminal** 
Go to the frontend directory

```bash
cd frontend
npm install
```

Start the React development server:
```bash
npm start

```

Access the App at 

```bash
http://127.0.0.1:3000/
```


## Screenshots



## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Authors

- [@pnaskardev](https://www.github.com/pnaskardev)

