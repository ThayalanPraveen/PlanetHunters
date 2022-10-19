from cryptography.fernet import Fernet
import joblib

key = Fernet.generate_key()
fernet = Fernet(key)
joblib.dump(fernet,"loader.joblib")