from app import app, db
import admin
import views
import models

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

