from main import db, Task

# create new tables within db
db.create_all()

db.session.add(Task('finish ORM lesson 2'))
db.session.add(Task('post lesson video'))

db.session.commit()

tasks = Task.query.all()
tasks[0].name