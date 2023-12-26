from flask import Flask,request,jsonify,render_template

class GUI:
    def __init__(self):
        """
        Initializes the GUI class.

        The GUI is built using Flask as the web framework and Jinja2 for rendering HTML templates.
        """
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            """
            Renders the index page.

            Returns:
                str: Rendered HTML content.
            """
            return render_template('templates/index.html')

    def run(self):
        """
        Runs the Flask web server.

        Starts the server and makes the GUI accessible at http://127.0.0.1:5000/.
        """
        self.app.run(debug=True)