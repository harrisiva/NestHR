from website import create_app 
#NOTE: Currently only supports one user at a time (need to implement session management code to models for multiple user capability)

app = create_app() # Create a app (code body in init)

if __name__=='__main__': 
    app.run(debug=True, port=3000) # run the app if called (debug mode)