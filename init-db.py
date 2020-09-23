from hook import create_app, db

# initializes db on cli call

def main():
    """ initialize db """
    print("Initializing db")
    db.create_all()
    print("DB initalized successfully!")


if __name__ == "__main__":
    create_app().app_context().push()
    # initializes db on cli call
    main()

# TODO: start working on the chat engine
