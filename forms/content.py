from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired

class ContentForm(FlaskForm):
    photo = FileField('Выберите фото', validators=[DataRequired()])
    description = TextAreaField('Что вы чувствовали в этот момент?', validators=[DataRequired()])
    submit = SubmitField('Сохранить в архив')
