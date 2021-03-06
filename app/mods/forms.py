from flask.ext.wtf import Form
from wtforms import TextField, SelectField, SelectMultipleField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


class ItemSearch(Form):
    item_name = TextField('Item name:')
    classes = SelectMultipleField('Class:')
    equip_regions = QuerySelectMultipleField('Equip region:')
    bodygroups = QuerySelectMultipleField('Bodygroup:')


class AuthorField(Form):
    author = TextField('Author')

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(AuthorField, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)


class EditMod(Form):
    pretty_name = TextField('Name:', validators=[Required()])
    workshop_id = TextField('Workshop ID:')
    description = TextAreaField('Description:',
                                description="You can use Markdown to format your description; "
                                            "<a target=\"_blank\" "
                                            "href=\"http://daringfireball.net/projects/markdown/syntax\">syntax</a>.")
    tags = QuerySelectMultipleField("Tags:")
    authors = FieldList(FormField(AuthorField), min_entries=5)
    package_format = SelectField("Package format:", validators=[Required()])
    equip_regions = QuerySelectMultipleField("Equip regions:", validators=[Required()])
    bodygroups = QuerySelectMultipleField("Bodygroups:")
    visibility = SelectField("Visibility:", validators=[Required()])
    publish = SubmitField("Save")


class ModSearch(Form):
    item_name = TextField('Item name:')
    classes = SelectMultipleField('Class:')
    equip_regions = QuerySelectMultipleField('Equip region:')
    bodygroups = QuerySelectMultipleField('Bodygroup:')
    tags = QuerySelectMultipleField('Tags:')
    submit = SubmitField("Submit")