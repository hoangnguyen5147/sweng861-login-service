import os  
import requests 
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from flask import Flask, redirect, session, request
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()

@app.route('/google_authorize')
def authorize():
   flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                "project_id": os.getenv('GOOGLE_PROJECT_ID'),
                "auth_uri": os.getenv('GOOGLE_AUTH_URI'),
                "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
                "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URI'),
                "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                "redirect_uris": [os.getenv('GOOGLE_REDIRECT_URI')]
                }
        },
        scopes=os.getenv('GOOGLE_SCOPES').split()
   )
   flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
   authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true',prompt='consent')
   session['state'] = state
   return redirect(authorization_url)

@app.route('/facebook_authorize')
def facebook_authorize():
   facebook_auth_url = f"{os.getenv('FB_AUTH_URI')}?client_id={os.getenv('FB_APP_ID')}&redirect_uri={os.getenv('FB_REDIRECT_URI')}&state={{st=state123abc,ds=123456789}}&scope={os.getenv('FB_SCOPES')}"
   return redirect(facebook_auth_url)

@app.route('/facebook_callback')
def facebook_callback():
   if 'error' in request.args:
      return 'Error: ' + request.args['error_description']
   code = request.args.get('code')
   token_params = {
        'client_id': os.getenv('FB_APP_ID'),
        'redirect_uri': os.getenv('FB_REDIRECT_URI'),
        'client_secret': os.getenv('FB_APP_SECRET'),
        'code': code
   }
   response = requests.get(os.getenv('FB_TOKEN_URI'), params=token_params)
   access_token = response.json().get('access_token')
   if not access_token:
      return 'Error retrieving access token'
   userinfo_params = {
        'fields': 'name,email,picture',
        'access_token': access_token
   }
   user_info_response = requests.get(os.getenv('FB_USER_INFO_URI'), params=userinfo_params)
   user_info = user_info_response.json()
   session['user'] = user_info
   return f'''
    <h2>Welcome, {user_info["name"]}</h2>
    <p>Email: {user_info.get("email", "Not provided")}</p>
    <img src="{user_info["picture"]["data"]["url"]}" alt="Profile Picture"><br><br>
    <a href="/logout"><button>Logout</button></a>
'''
   
@app.route('/google_callback')
def google_callback():
   state = session['state']
   if not state:
        return 'State parameter missing in session.', 400
   flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                "project_id": os.getenv('GOOGLE_PROJECT_ID'),
                "auth_uri": os.getenv('GOOGLE_AUTH_URI'),
                "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
                "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URI'),
                "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                "redirect_uris": [os.getenv('GOOGLE_REDIRECT_URI')]
                }
        },
        scopes=os.getenv('GOOGLE_SCOPES').split(),
        state=state
   )
   flow.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
   authorization_response = request.url
   flow.fetch_token(authorization_response=authorization_response)
   credentials = flow.credentials

   response = requests.get(os.getenv('GOOGLE_USER_INFO'), params={'alt': 'json'}, headers={'Authorization': 'Bearer ' + credentials.token})
   if response.status_code != 200:
        return 'Failed to fetch user info: ' + response.text, 400
   
   user_info = response.json()
   session['user'] = user_info
   return f'''
    <h2>Welcome, {user_info["name"]}</h2>
    <p>Email: {user_info["email"]}</p>
    <img src="{user_info["picture"]}" alt="Profile Picture"><br><br>
    <a href="/logout"><button>Logout</button></a>
'''

@app.route('/logout')
def logout():
   session.clear()
   return f'''
   <p>You have been logged out.</p><br>
   <a href="/"><button>Home</button></a>
   '''

@app.route('/')
def login_page():
  return f'''
  <h1>Login Page</h1>
  <a href="/google_authorize"><button>Login With Google</button></a><br><br>
  <a href="/facebook_authorize"><button>Login With Facebook</button></a>
  '''
      
if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080, debug=True)