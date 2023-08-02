from jinja2 import FileSystemLoader, Environment

env = Environment(loader=FileSystemLoader("./"))
print(env.get_template("base.html").render())
print('________________________________________________')
print(env.get_template("sub.html").render())