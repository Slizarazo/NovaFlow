from flask import Flask, g, render_template, current_app

def before_template_rendered(sender, template, context, **extra):
    print(f"Template: {template.name}")
    print("Context variables:")
    for key, value in context.items():
        print(f"- {key}: {type(value)}")
        if key == 'config':
            print(f"  Config has keys: {dir(value)}")
            if hasattr(value, 'get'):
                print(f"  NAVIGATION exists: {value.get('NAVIGATION') is not None}")
            else:
                print("  Config object doesn't have get method")

app = Flask(__name__)

# Import the signal
from flask import template_rendered
template_rendered.connect(before_template_rendered, app)

if __name__ == '__main__':
    app.run(debug=True)