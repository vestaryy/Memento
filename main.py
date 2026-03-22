from data import db_session
from data.users import User
from data.content import Content

def main():
    db_session.global_init("db/assistant.db")
    
    db_sess = db_session.create_session()
    
   

if __name__ == '__main__':
    main()