from route.models import Pointage, Detailpointage, Config, User
from route.config import Default
from route import db
from flask import abort, flash
from sqlalchemy import func
from route.config import Default

def insertdb_pointage(user, feries, jours, nuits):
	try:
		pointage = Pointage(iduser=int(user))
		db.session.add(pointage)
		last = db.session.query(func.max(Pointage.id)).scalar()
		# print("last={}".format(last))
		for day in Default.DAYS:
			ferie = int(feries.get(day)) if len(feries.get(day)) > 0 else 0
			jour = int(jours.get(day)) if len(jours.get(day)) > 0 else 0
			nuit = int(nuits.get(day)) if len(nuits.get(day)) > 0 else 0
			if jour > Default.TEMPS_JOUR or nuit > Default.TEMPS_NUIT or ferie > 24:
				db.session.rollback()
				flash("Donnees Invalide", 'danger')
				abort(500)
			details = Detailpointage(idpointage=int(last),
									jour=day,
									est_ferier=ferie,
									heure_jour=jour,
									heure_nuit=nuit)
			db.session.add(details)
	except:
		db.session.rollback()
		flash("Donnees Invalide", 'danger')
		abort(500)
	try:
		db.session.commit()
	except:
		db.session.rollback()
		flash("Donnees Invalide", 'danger')
		abort(500)
	return last

def updatedb_pointage(user, feries, jours, nuits):
	try:
		pointage = Pointage.query.filter_by(iduser=int(user)).first()
		for day in Default.DAYS:
			ferie = int(feries.get(day)) if len(feries.get(day)) > 0 else 0
			jour = int(jours.get(day)) if len(jours.get(day)) > 0 else 0
			nuit = int(nuits.get(day)) if len(nuits.get(day)) > 0 else 0
			if jour > Default.TEMPS_JOUR or nuit > Default.TEMPS_NUIT or ferie > 24:
				db.session.rollback()
				flash("Donnees Invalide", 'danger')
				abort(500)
			detail = Detailpointage.query.filter_by(idpointage=pointage.id, jour=day).first()

			detail.jour=day
			detail.est_ferier=ferie
			detail.heure_jour=jour
			detail.heure_nuit=nuit
			# db.session.commit()
	except:
		db.session.rollback()
		flash("Donnees Invalide", 'danger')
		abort(500)
	try:
		db.session.commit()
	except:
		db.session.rollback()
		flash("Donnees Invalide", 'danger')
		abort(500)
	return pointage.id



def heure_journuit(details):
	somj = 0
	somn = 0
	for detail in details:
		if detail.est_ferier == 0 and detail.jour != "DIMANCHE":
			somj += detail.heure_jour
			somn += detail.heure_nuit

	return somj, somn

def heure_dimanche(details):
	dim = 0
	for detail in details:
		if detail.est_ferier == 0 and detail.jour == "DIMANCHE":
			dim += detail.heure_jour
			dim += detail.heure_nuit

	return dim

def heure_ferie_trav(details):
	som = 0
	for detail in details:
		if detail.est_ferier > 0:
			som += detail.heure_jour
			som += detail.heure_nuit

	return som

def heure_ferie(details):
	som = 0
	for detail in details:
		if detail.est_ferier > 0:
			som += detail.est_ferier

	return som

def heure_total(details):
	"""
		return heure total semaine
	"""
	som = 0
	for detail in details:
		som += detail.est_ferier
		som += detail.heure_jour
		som += detail.heure_nuit

	return som

def heure_supp(user, details):
	total = heure_total(details)
	total -= heure_ferie_trav(details)
	heure_norm = user.cat.heure_hebdo
	supp_total =  max(0, (total - heure_norm))
	supp30 = min(8, supp_total)
	supp50 = max(0, min(12, supp_total - supp30))
	return supp30, supp50



def calcul_heure(user, pointage):
	details = Detailpointage.query.filter_by(idpointage=pointage.id)
	jour, nuit = heure_journuit(details)
	dimanche = heure_dimanche(details)
	ferie_trav = heure_ferie_trav(details)
	ferie = heure_ferie(details)
	supp30, supp50 = heure_supp(user, details)
	result = {}
	result["Nb heure jour"] = jour
	result["Nb heure nuit"] = nuit
	result["Nb heure dimanche"] = dimanche
	result["Nb heure jour ferie travaille"] = ferie_trav
	result["Nb heure jour ferie"] = ferie
	result["Nb heure supp 30%"] = supp30
	result["Nb heure supp 50%"] = supp50
	# print(result)
	return result
	# print("jour={}, nuit={}".format(jour, nuit))
	# print("dimanche={}".format(dimanche))
	# print("ferie_trav={}".format(ferie_trav))
	# print("sup30={}, supp50={}".format(supp30, supp50))


def tomap(configs):
	m = {}
	for config in configs:
		m[config.cle] = config.valeur
	return m


def fiche_de_paie(user, pointage):
	heures = calcul_heure(user, pointage)
	heure_hebdo = user.cat.heure_hebdo
	salaire_hebdo = user.cat.salaire_hebdo
	taux_h = float(salaire_hebdo/heure_hebdo)
	paie ={}
	arr = []

	configs = Config.query.all()
	map_conf = tomap(configs)
	total_paye = 0
	for key, value in heures.items():
		val = float(value)
		arr.append(value)
		if key == "Nb heure nuit":
			th = taux_h  * float(map_conf.get("HM30"))/100
			arr.append(th)
		elif key == "Nb heure dimanche":
			th = taux_h  * float(map_conf.get("HM40"))/100
			arr.append(th)
		elif key == "Nb heure supp 30%":
			th = taux_h  * (float(map_conf.get("HS30"))-100)/100
			arr.append(th)
		elif key == "Nb heure supp 50%":
			th = taux_h  * (float(map_conf.get("HS50"))-100)/100
			arr.append(th)
		elif key == "Nb heure jour ferie travaille":
			th = taux_h  * float(map_conf.get("HM50"))/100
			arr.append(th)
		else:
			th = taux_h * 100/100
			arr.append(th)

		arr.append(th * val)
		paie[key] = arr
		arr = list()
		total_paye += (th * val)

	heuret = heure_total(Detailpointage.query.filter_by(idpointage=pointage.id))
	heuretdiff = heure_hebdo - heuret
	indemnite = user.cat.indemnite if heuretdiff <= 0 else 0
	total_with_impot = (1 - float(map_conf.get("Impot")) / 100) * total_paye
	total_without_impot = total_paye
	total_paye = float(indemnite) + total_with_impot
	return paie, indemnite, total_paye, total_with_impot, total_without_impot

def users_total():
	users = User.query.all()
	all_users = {}
	all_total = 0
	for user in users:
		pointage = Pointage.query.filter_by(iduser=user.id).first()
		if pointage != None:
			_, _, total, _, _ = fiche_de_paie(user, pointage)
			all_users[user.matricule] = total
			all_total += total
		else:
			all_users[user.matricule] = 0
			all_total += 0

	# print(all_users)
	return all_users, all_total

def dummy_fiche():
	keys = ["Nb heure jour", "Nb heure nuit", "Nb heure dimanche", "Nb heure jour ferie travaille",
			"Nb heure jour ferie", "Nb heure supp 30%", "Nb heure supp 50%"]
	res = {}
	for key in keys:
		res[key] = [0, 0, 0]
	return res

def paie_total():
	users = User.query.all()
	keys = ["Nb heure jour", "Nb heure nuit", "Nb heure dimanche", "Nb heure jour ferie travaille",
			"Nb heure jour ferie", "Nb heure supp 30%", "Nb heure supp 50%"]
	dummy = dummy_fiche()
	ans = {}
	all_total = 0
	res = []
	for user in users:
		pointage = Pointage.query.filter_by(iduser=user.id).first()
		if pointage != None:
			res.append(fiche_de_paie(user, pointage))
		else:
			res.append((dummy, 0, 0, 0, 0))

	for key in keys:
		t, m = 0, 0
		for result in res:
			paie, indemnite, total_paye, _, _ = result
			t += paie[key][0]
			m += paie[key][2]
		ans[key] = [t, m]

	return ans