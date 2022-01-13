from dash import Dash
from layout import layout
from callbacks import get_callbacks

app = Dash(__name__)
app.layout = layout

get_callbacks(app)

if __name__ == '__main__':
   app.run_server(debug=True)
