## Author 
**Hoang Nguyen**

This is a symbol web application to demonstrate the implementation and use of OAuth2.0 authorization

## Application Features:
    . Google OAuth2.0
    . Facebook OAuth2.0

## Step 1: Installation: 
Make sure you have Python 3.7+ install.
Clone the project from github
```bash
git clone https://github.com/hoangnguyen5147/sweng861-login-service.git
cd project-repository
pip install -r requirements.txt
```

## Step 2: Download and Add .env file: 
Download `env` file from Azure container via shared link (The link to the download env will be provided separately).
Rename `env` to `.env` file after download.
Add the downloaded `.env` file in the root directory of the project repository.
Note: you can create your own `.env` file following the same format from the provided `.env` file to use your own client ids and client secrets 

## Hidden File: 
`.` file is hidden by default so following the following instruction if you can't see the file in your directory.
macOS (Finder): Open folder where `.env` is -> Press `Command + Shift + .` 
Windows (File Explorer): Open folder where `.env` is -> Select the `View` tab at the top -> Check the box `Hidden Items`.

## Step 3: Usage: 
Enter the following comamnd to run the app in terminal: python app.py
Successfully running app.py will output the following lines
```bash
 * Serving Flask app `app`
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:8080
Press CTRL+C to quit
 * Restarting with watchdog (fsevents)
 * Debugger is active!
 * Debugger PIN: 306-095-811
```

 ## Step 4: Open web browser: 
 Open your web browser at http://localhost:8080 
 Choose Between `Login with Google` or `Login with Facebook` and following the prompt to enter your user name and password for authorization

 ## Project Structure:
your-project/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
└── docs/
    └── OAuth2.pdf

## Flow Charts:
[View Flow Diagram](docs/OAuth2.pdf)

