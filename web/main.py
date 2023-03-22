from website import create_app 

app = create_app() # Create a app (code body in init)

if __name__=='__main__': 
    app.run(debug=True) # run the app if called (debug mode)