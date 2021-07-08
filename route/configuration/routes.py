from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from route.models import Pointage, Detailpointage, User, Config
from route.configuration.forms import ConfigForm
from route import db
from route.config import Default
from route.pointage import services


configuration = Blueprint('configuration', __name__)

@configuration.route('/config', methods=['GET', 'POST'])
@login_required
def list_config():
    configs = Config.query.all()
    return render_template('config.html', title='Listes config', configs=configs)



@configuration.route('/configuration/<int:config_id>/update', methods=['GET', 'POST'])
@login_required
def updateConfig(config_id):
    config = Config.query.get_or_404(config_id)
    form = ConfigForm()
    if form.validate_on_submit():
        config.cle = form.cle.data
        config.description = form.description.data
        config.valeur = form.valeur.data

        db.session.commit()
        flash('Your configuration has been updated!', 'success')
        return redirect(url_for('configuration.list_config'))
    else:
        form.cle.data = config.cle
        form.description.data = config.description
        form.valeur.data = config.valeur
    return render_template('config_form.html', title='Update config', form=form, legend='Update config')
