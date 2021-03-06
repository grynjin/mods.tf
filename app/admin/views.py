from flask.ext.login import current_user
from flask.ext.admin import Admin, expose, AdminIndexView, BaseView
from flask.ext.admin.contrib.sqla import ModelView
from flask import url_for
from jinja2 import Markup
from app import db
from ..users.models import User
from ..mods.models import Mod, ModPackage, PackageDownload, ModAuthor
from datetime import datetime, timedelta


class Auth(object):
    def is_accessible(self):
        return current_user.is_admin()


class AdminModelView(Auth, ModelView):
    """ Used for setting up admin-only model views """
    pass


class AdminIndex(Auth, AdminIndexView):
    @expose('/')
    def index(self):
        from collections import OrderedDict
        import datetime
        stats = OrderedDict([
            ("users", {"stat": User.query.filter_by(enabled=True).count()}),
            ("downloads", {"stat": PackageDownload.query.count()}),
            ("mods", {"stat": Mod.query.filter_by(visibility="Pu").count()}),
            ("unlisted mods", {"stat": Mod.query.filter_by(visibility="Pr").count(),
                               "url": url_for('modlists.index', _anchor='unlisted')}),
            ("hidden mods", {"stat": Mod.query.filter_by(visibility="H").count(),
                             "url": url_for('modlists.index', _anchor='hidden')}),
            ("uncompleted mods", {"stat": Mod.query.filter_by(completed=False).count(),
                                  "url": url_for('modlists.index', _anchor='uncompleted')}),
            ("valid packages", {"stat": ModPackage.query.filter(ModPackage.expire_date > datetime.datetime.utcnow()).count()}),
            ("expired packages - not deleted", {"stat": ModPackage.query.filter(ModPackage.expire_date < datetime.datetime.utcnow()).filter(ModPackage.deleted == False).count()})
        ])
        return self.render('admin/index.html', stats=stats)


class UserView(Auth, ModelView):
    def show_avatar(self, context, model, name):
        if not model.avatar_medium:
            return ''
        return Markup('<img src="{}">'.format(model.avatar_medium))

    def profile_url(self, context, model, name):
        if not model.profile_url:
            return ''
        return Markup('<a href="{0}" target="_blank">{0}</a>'.format(model.profile_url))

    column_display_pk = True
    column_exclude_list = ['avatar_small', 'avatar_large']
    form_excluded_columns = ['mod', 'author']
    column_formatters = {
        'avatar_medium': show_avatar,
        'profile_url': profile_url
    }
    column_searchable_list = ['name']
    form_ajax_refs = {
        'download': {
            'fields': (PackageDownload.package_id,),
            'page_size': 10
        }
    }


class ModView(Auth, ModelView):
    column_display_pk = True
    column_exclude_list = ['avatar_small', 'avatar_large']
    form_excluded_columns = ['author', 'class_model', 'package']
    column_searchable_list = ['name']
    form_ajax_refs = {
        'authors': {
            'fields': (User.account_id,),
            'page_size': 10
        }
    }


class BigDownloaders(Auth, BaseView):
    @staticmethod
    def user_download_count(hours=None):
        rows = db.session.query(PackageDownload, db.func.count(PackageDownload.id))
        if hours:
            _time_ago = datetime.utcnow() - timedelta(hours=hours)
            rows = rows.filter(PackageDownload.downloaded >= _time_ago)
        rows = rows.group_by(PackageDownload.user_id).\
            order_by(db.func.count(PackageDownload.package_id).desc()).\
            limit(30).\
            all()
        return rows

    @expose('/')
    def index(self):
        """ Renders a list of users who have done an lot of downloads in particular time frames. """

        return self.render(
            'admin/big_downloaders.html',
            daily_downloaders=self.user_download_count(24),
            weekly_downloaders=self.user_download_count(24 * 7),
            monthly_downloaders=self.user_download_count(24 * 31),
            all_time_downloaders=self.user_download_count()
        )


class SharedZips(Auth, BaseView):
    @expose('/')
    def index(self):
        """ Renders a list of mods which do not have the manifest_steamid within mod_authors. """

        mod_authors_sq = db.session.query(ModAuthor.user_id).filter(ModAuthor.mod_id == Mod.id).subquery
        shared_zip_mods = Mod.query.filter(Mod.manifest_steamid.notin_(mod_authors_sq()))

        return self.render(
            'admin/shared_zips.html',
            shared_zip_mods=shared_zip_mods
        )


class ModLists(Auth, BaseView):
    @staticmethod
    def mod_query(visibility=None, completed=True):
        rows = Mod.query
        if visibility:
            rows = rows.filter_by(visibility=visibility)
        rows = rows.filter_by(completed=completed)
        return rows.all()

    @expose('/')
    def index(self):
        """ Renders a list of mods with non-standard visibilities. """

        return self.render(
            'admin/mod_lists.html',
            unlisted=self.mod_query("Pr"),
            hidden=self.mod_query("H"),
            uncompleted=self.mod_query(completed=False)
        )


admin = Admin(name="mods.tf", index_view=AdminIndex())

admin.add_view(ModView(Mod, db.session, category="Models"))
admin.add_view(UserView(User, db.session, category="Models"))

admin.add_view(BigDownloaders(name="Big downloaders", category="Reports"))
admin.add_view(SharedZips(name="Shared zips", category="Reports"))

admin.add_view(ModLists(name="Mod lists", category="Lists"))