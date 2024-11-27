import psycopg2
from psycopg2 import sql
import secrets
import string

# a singleton class to generate invitation code and write it to database
class InvitationCodeGenerator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Generate a unique invitation code
    def generateInvCode(self, length=10):
        characters = string.ascii_letters + string.digits
        code =  ''.join(secrets.choice(characters) for _ in range(length))
        self.saveCodeToDB(code)
        return code

    # Insert the code into PostgreSQL
    def saveCodeToDB(self, code):
        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                dbname="valuenotifier",
                user="vu",
                password="vu101",
                host="localhost",  # Replace with your host if not local
                port="5432"        # Default PostgreSQL port
            )
            cursor = conn.cursor()

            # Insert the code into the database
            insertQuery = sql.SQL("""
                INSERT INTO invitation_codes (code) VALUES (%s)
            """)
            cursor.execute(insertQuery, (code,))

            # Commit the transaction
            conn.commit()
            print(f"Code {code} saved successfully.")
        except psycopg2.IntegrityError:
            # Handle duplicate code error
            print(f"Code {code} already exists.")
            conn.rollback()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the connection
            if conn:
                cursor.close()
                conn.close()

# Example usage
if __name__ == "__main__":
    generator = InvitationCodeGenerator()
    generator.generateInvCode()
