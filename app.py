from flask import request, url_for, g
from flask.ext.api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy
import arrow
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from flask.ext.cors import CORS


app = FlaskAPI(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
db = SQLAlchemy(app)



class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=False)
    ticketcode = db.Column(db.String(80), unique=True, primary_key=True)
    arrived = db.Column(db.Boolean, unique=False)
    arrived_at = db.Column(db.String(80), unique=False)

    def __init__(self, ticketcode):
        self.ticketcode = ticketcode
        self.arrived = False
        self.arrived_at = ""

    def __repr__(self):
        return '<User %r>' % self.ticketcode




def arrived():
    return len(Ticket.query.filter_by(arrived=True).all())



def not_in_list_repr(ticketcode, arrived):
    return {    
        'ticketcode' : str(ticketcode),
        'status' : 'nil',
        'count_arrived' : arrived
    }

def arrived_repr(ticketcode, ticket, arrived):
    return {
        'ticketcode' : str(ticketcode),
        'status' : 'arr',
        'timestamp' : arrow.get(ticket.arrived_at).format('YYYY-MM-DD HH:mm:ss ZZ'),
        'human_timestamp' : arrow.get(ticket.arrived_at).humanize(),
        'count_arrived' : arrived
    }
def not_arrived_repr(ticketcode, ticket, arrived):
    return {
        'ticketcode' : str(ticketcode),
        'status' : 'n_arr',
        'count_arrived' : arrived
    }

def already_arrived_repr(ticketcode, ticket, arrived):
    return {
        'ticketcode' : str(ticketcode),
        'status' : 'a_arr',
        'timestamp' : arrow.get(ticket.arrived_at).format('YYYY-MM-DD HH:mm:ss ZZ'),
        'human_timestamp' : arrow.get(ticket.arrived_at).humanize(),
        'count_arrived' : arrived
    }

def all_tickets_repr(arrived, not_arrived):
    count_arrived = len(arrived)
    count_not_arrived = len(not_arrived)
    
    not_arrived_ticketcodes = []
    for i in not_arrived:
        not_arrived_ticketcodes.append(i.ticketcode)
    
    arrived_ticketcodes = {}
    for i in arrived:
        arrived_ticketcodes[i.ticketcode] = arrow.get(i.arrived_at).format('YYYY-MM-DD HH:mm:ss ZZ')

    return {
        'count_arrived' : count_arrived,
        'count_not_arrived' : count_not_arrived,
        'arrived' : arrived_ticketcodes,
        #'not_arrived' : not_arrived_ticketcodes
    }




@app.route("/", methods=['GET'])
def all_tickets():
    if request.method == 'GET':
        arrived = Ticket.query.filter_by(arrived=True).all()
        not_arrived = Ticket.query.filter_by(arrived=False).all()
        return all_tickets_repr(arrived, not_arrived)


@app.route("/<int:ticketcode>/", methods=['GET', 'POST']) #, 'PUT', 'DELETE']
def arrive(ticketcode):
    if request.method =='GET':
        ticketcode = str(ticketcode)
        ticket = Ticket.query.get(ticketcode)
        if ticket != None:
            if ticket.arrived == True:
                return already_arrived_repr(ticketcode, ticket, arrived())
            else:
                return not_arrived_repr(ticketcode, ticket, arrived())
        else:
            return not_in_list_repr(ticketcode, arrived())

    if request.method =='POST':
        ticketcode = str(ticketcode)
        ticket = Ticket.query.get(ticketcode)
        if ticket != None:
            if ticket.arrived == True:
                return already_arrived_repr(ticketcode, ticket, arrived())
            else:
                ticket.arrived = True
                ticket.arrived_at = arrow.utcnow().timestamp
                db.session.commit()
                return arrived_repr(ticketcode, ticket, arrived())
        else:
            return not_in_list_repr(ticketcode, arrived())
    #if request.method == 'PUT':


if __name__ == "__main__":
    admin = Admin(app)
    admin.add_view(ModelView(Ticket, db.session))
    app.run(debug=True, host="0.0.0.0")
