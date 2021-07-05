from route.models import Pointage, Detailpointage
from route.config import Default
from route import db
from flask import abort, flash
from sqlalchemy import func

def insertdb_pointage(user, feries, jours, nuits):
	try:
		pointage = Pointage(iduser=int(user))
		db.session.add(pointage)
		last = db.session.query(func.max(Pointage.id)).scalar()
		print("last={}".format(last))
		for day in Default.DAYS:
			ferie = int(feries.get(day))
			jour = int(jours.get(day)) if len(jours.get(day)) > 0 else 0
			nuit = int(nuits.get(day)) if len(nuits.get(day)) > 0 else 0
			details = Detailpointage(idpointage=int(last),
									jour=day,
									est_ferier=ferie,
									heure_jour=jour,
									heure_nuit=nuit)
			db.session.add(details)
	except:
		flash("Donnees Invalide", 'danger')
		abort(500)
	db.session.commit()

	