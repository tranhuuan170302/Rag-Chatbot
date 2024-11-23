from typing import Dict, Any
from sqlalchemy.orm import Session
from models.data.sqlalchemy_models import Signup
from sqlalchemy import desc

class SignupRepository:
    
    def __init__(self, sess:Session):
        self.sess = sess
    
    def insert_signup(self, signup: Signup) -> bool:
        try:
            self.sess.add(signup)
            print("pass add stage")
            self.sess.commit()
            print(f'signup id: ${signup.id}')
        except Exception as e:
            print(f"Error during commit: {e}")
            self.sess.rollback()
            return False
        return True
    
    def get_signup_email(self, email: str):
        return self.sess.query(Signup).filter(Signup.email == email).one_or_none()