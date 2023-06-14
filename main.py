# Script containing init of app
# Author: Jakub Sikula

# Import the api modules
from api import create_app

app = create_app()
app.run(debug=True, host='0.0.0.0')