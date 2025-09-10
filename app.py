import cohere
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

class Form(FlaskForm):
    text = StringField('Enter text to chat', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()
    co = cohere.Client('YOUR_COHERE_API_KEY')  # Replace with your API key
    output = None
    if form.validate_on_submit():
        text = form.text.data
        response = co.generate(
            model='command-nightly',  # 'command' or latest model
            prompt=text,
            max_tokens=300,
            temperature=0.9,
            k=0,
            p=0.75,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        output = response.generations.text
    return render_template('home.html', form=form, output=output)

if __name__ == "__main__":
    app.run(debug=True)
