from main import db, Task, User

# create new tables within db
db.create_all()

db.session.add(Task('finish ORM lesson 2'))
db.session.add(Task('post lesson video'))

db.session.add(User('fengli@gmail.com','cheese'))
db.session.add(User('chris@launchcode.org', '12345'))

db.session.commit()

tasks = Task.query.all()
tasks[0].name