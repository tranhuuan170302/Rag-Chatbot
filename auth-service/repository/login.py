from typing import Dict, Any
from sqlalchemy.orm import Session
from models.data.sqlalchemy_models import Login
from sqlalchemy import desc

class LoginRepository:
    
    def __init__(self, sess: Session):
        self.sess = sess
    
    def insert_login(self, login: Login) -> bool:
        """_summary_

        Args:
            login (Login): email address of the user, password of the user

        Returns:
            bool: (true or false)
        """
        try:
            self.sess.add(login)
            self.sess.commit()
        except Exception as e:
            print(f"Error during commit: {e}")
            return False
    
    def update_login(self, id: int, details:Dict[str, Any]) -> bool:
        try:
            self.sess.query(Login.id).filter(Login.id == id).update(details)
            self.sess.commit()
        except:
            return False
        return True    
    
    def get_all_login_username(self, email: str):
        return self.sess.query(Login).filter(Login.email == email).one_or_none()