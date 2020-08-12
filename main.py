from flask import Flask, request, jsonify
from model import db
from model import Villain

app = Flask("app")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

"""
# If villain.db is empty, run the two below in Terminal first 

from flask import Flask
from model import db, Villain
app = Flask("app")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()
"""

# Get our model up and running
db.init_app(app)

# Serving Static Files
@app.route("/")
def villain_cards():
    return app.send_static_file("villain.html")


@app.route("/add")
def add():
    return app.send_static_file("addvillain.html")


@app.route("/delete")
def delete():
    return app.send_static_file("deletevillain.html")


@app.route("/update")
def update():
    return app.send_static_file("updatevillain.html")


# ALL VILLAINS
@app.route("/api/villains/")
def get_villains():
    # breakpoint()
    villains = Villain.query.all()
    data = []
    for villain in villains:
        data.append(
            {
                "name": villain.name,
                "description": villain.description,
                "interests": villain.interests,
                "url": villain.url,
                "date_added": villain.date_added,
            }
        )
    return jsonify(data)


# ADD VILLAIN
@app.route("/api/villains/add", methods=["POST"])
def add_villain():
    errors = []
    name = request.form.get("name")
    if not name:
        errors.append("Oops! Looks like you forgot a name!")

    description = request.form.get("description")
    if not description:
        errors.append("Oops! Looks like you forgot a description!")

    interests = request.form.get("interests")
    if not interests:
        errors.append("Oops! Looks like you forgot some interests!")

    url = request.form.get("url")
    if not url:
        errors.append("Oops! Looks like you forgot an image!")

    villain = Villain.query.filter_by(name=name).first()
    if villain:
        errors.append("Oops! A villain with that name already exists!")

    if errors:
        return jsonify({"errors": errors})
    else:
        new_villain = Villain(
            name=name, description=description, interests=interests, url=url
        )
        db.session.add(new_villain)
        db.session.commit()
        return jsonify({"status": "success"})


# UPDATE VILLAIN
@app.route("/api/villains/update", methods=["POST"])
def update_villain():
    print("WE MADE IT")
    print("hit update villain")
    name = request.form.get("name")
    villain = Villain.query.filter_by(name=name).first()
    print(villain.name)
    if villain:
        description = request.form.get("description")
        interests = request.form.get("interests")
        url = request.form.get("url")
        villain.description = description
        villain.interests = interests
        villain.url = url
        db.session.commit()
        return jsonify({"status": "success"})
    else:
        return jsonify({"errors": ["Oops! A villain with that name doesn't exist!"]})


# SELECT VILLAIN TO UPDATE
@app.route("/api/villains/select", methods=["POST"])
def select_villain():
    print("hit select villain")
    data = []
    name = request.form.get("name")
    villain = Villain.query.filter_by(name=name).first()
    if villain:
        data.append(
            {
                "name": villain.name,
                "description": villain.description,
                "interests": villain.interests,
                "url": villain.url,
            }
        )
        return jsonify(data)
    else:
        return jsonify({"errors": ["Something went wrong."]})


# DELETE VILLAIN
@app.route("/api/villains/delete", methods=["POST"])
def delete_villain():
    name = request.form.get("name")
    villain = Villain.query.filter_by(name=name).first()
    if villain:
        db.session.delete(villain)
        db.session.commit()
        return jsonify({"status": "success"})
    else:
        return jsonify({"errors": ["Oops! A villain with that name doesn't exist!"]})


@app.route("/api/")
def get_endpoints():
    endpoints = {
        "api/villains/": "GET - Retrieves all villain data from the database",
        "api/villains/add": "POST - Add a villain to the database",
        "api/villains/delete": "POST - Delete a villain from the database",
        "api/villains/update": "POST - Update an existing villain",
    }
    return jsonify(endpoints)


if __name__ == "__main__":
    app.debug = True
    app.run()

# app.run(host='0.0.0.0', port=8080)
