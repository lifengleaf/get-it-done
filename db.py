from main import db, Task, User

db.drop_all()
# create new tables within db
db.create_all()

feng = User('feng@gmail.com','cheese')
task1 = Task('finish ORM lesson 2', feng)
db.session.add(feng)
db.session.add(task1)

chris = User('chris@launchcode.org', '123')
task2 = Task('post lesson video', chris)
db.session.add(chris)
db.session.add(task2)

db.session.commit()

tasks = Task.query.all()
users = User.query.all()

tasks[0].name
users[0].tasks[0].name