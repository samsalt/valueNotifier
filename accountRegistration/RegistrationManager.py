from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/valuenotifier'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=True)
    stock_id = db.Column(db.String(20), nullable=False)

class InvitationCode(db.Model):
    __tablename__ = 'invitation_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    used = db.Column(db.Boolean, default=False, nullable=False)

# API route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    # Validate the input
    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')  # Optional
    stock_id = data.get('stock_id')
    invitation_code = data.get('invitation_code')

    if not all([username, email, stock_id, invitation_code]):
        return jsonify({"error": "Missing required fields."}), 400

    # Check if the invitation code exists and is unused
    code_entry = InvitationCode.query.filter_by(code=invitation_code, used=False).first()
    if not code_entry:
        return jsonify({"error": "Invalid or already used invitation code."}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already registered."}), 400

    # Save the user to the database
    try:
        new_user = User(username=username, email=email, phone_number=phone_number, stock_id=stock_id)
        db.session.add(new_user)

        # Mark the invitation code as used
        code_entry.used = True
        db.session.commit()

        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to register user.", "details": str(e)}), 500

# Run the application
if __name__ == '__main__':
    # Ensure the database tables are created
    with app.app_context():
        db.create_all()

    app.run(debug=True)
