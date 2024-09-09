from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name}, Number: {self.number}>"

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        number = request.form['number']

        new_contact = Contacts(first_name = first_name,  last_name = last_name, number = number)

        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect('/')
        except:
            return "Unable to add the contact"
        
    else:
        contacts = Contacts.query.all()
        return render_template('index.html', contacts = contacts)
    

@app.route('/delete/<int:id>')
def delete(id):
    contact_to_delete = Contacts.query.get_or_404(id)
    
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the contact.'


if __name__ == '__main__':
    app.run(debug=True)