from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'reeshika-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reeshika.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'


# ==================== MODELS ====================
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(255))

    def set_password(self, p):
        self.password_hash = generate_password_hash(p)

    def check_password(self, p):
        return check_password_hash(self.password_hash, p)


class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    product = db.Column(db.String(200))
    message = db.Column(db.Text)
    source = db.Column(db.String(50), default='website')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    product = db.Column(db.String(200))
    quantity = db.Column(db.String(20))
    branch = db.Column(db.String(100))
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(uid):
    return Admin.query.get(int(uid))


# ==================== COMPANY DATA ====================
COMPANY = {
    "name": "Reeshika Electronics",
    "tagline": "EV Chargers",
    "phone": "9886369502",
    "phone_display": "98863 69502",
    "whatsapp": "9886369502",
    "email": "reeshikaelectronics@gmail.com",
    "branches": [
        {
            "icon": "fa-warehouse",
            "title": "Head Office",
            "address": "Ravuru Village, Indukurpet Mandal, SPSR Nellore, Andhra Pradesh - 524314",
            "city": "Nellore"
        },
        {
            "icon": "fa-building",
            "title": "Branch - Bengaluru",
            "address": "9th Main Road, Banashankari 2nd Stage, Banashankari, Bengaluru, Karnataka - 560070",
            "city": "Bengaluru"
        },
        {
            "icon": "fa-city",
            "title": "Branch - New Delhi",
            "address": "RZ 45, Old Roshanpura, J Block, Najafgarh, New Delhi - 110043",
            "city": "New Delhi"
        }
    ],
    "map_embed": "https://www.google.com/maps?q=Banashankari+2nd+Stage+Bengaluru+560070&output=embed",
}

# Products
TWO_WHEELER = [
    {"voltage": "48V", "current": "6A", "name": "48V 6A Charger", "type": "2W", "power": "288W"},
    {"voltage": "60V", "current": "6A", "name": "60V 6A Charger", "type": "2W", "power": "360W"},
    {"voltage": "72V", "current": "6A", "name": "72V 6A Charger", "type": "2W", "power": "432W"},
    {"voltage": "48V", "current": "10A", "name": "48V 10A Charger", "type": "2W", "power": "480W"},
    {"voltage": "60V", "current": "10A", "name": "60V 10A Charger", "type": "2W", "power": "600W"},
    {"voltage": "72V", "current": "10A", "name": "72V 10A Charger", "type": "2W", "power": "720W"},
]

THREE_WHEELER = [
    {"voltage": "48V", "current": "15A", "name": "48V 15A Charger", "type": "3W", "power": "720W"},
    {"voltage": "60V", "current": "15A", "name": "60V 15A Charger", "type": "3W", "power": "900W"},
    {"voltage": "72V", "current": "15A", "name": "72V 15A Charger", "type": "3W", "power": "1080W"},
    {"voltage": "48V", "current": "20A", "name": "48V 20A Charger", "type": "3W", "power": "960W"},
    {"voltage": "60V", "current": "20A", "name": "60V 20A Charger", "type": "3W", "power": "1200W"},
    {"voltage": "72V", "current": "20A", "name": "72V 20A Charger", "type": "3W", "power": "1440W"},
    {"voltage": "48V", "current": "30A", "name": "48V 30A Charger", "type": "3W", "power": "1440W"},
    {"voltage": "60V", "current": "30A", "name": "60V 30A Charger", "type": "3W", "power": "1800W"},
    {"voltage": "72V", "current": "30A", "name": "72V 30A Charger", "type": "3W", "power": "2160W"},
    {"voltage": "48V", "current": "35A", "name": "48V 35A Charger", "type": "3W", "power": "1680W"},
    {"voltage": "60V", "current": "35A", "name": "60V 35A Charger", "type": "3W", "power": "2100W"},
    {"voltage": "72V", "current": "35A", "name": "72V 35A Charger", "type": "3W", "power": "2520W"},
    {"voltage": "48V", "current": "40A", "name": "48V 40A Charger", "type": "3W", "power": "1920W"},
    {"voltage": "60V", "current": "40A", "name": "60V 40A Charger", "type": "3W", "power": "2400W"},
    {"voltage": "72V", "current": "40A", "name": "72V 40A Charger", "type": "3W", "power": "2880W"},
    {"voltage": "48V", "current": "50A", "name": "48V 50A Charger", "type": "3W", "power": "2400W"},
    {"voltage": "60V", "current": "50A", "name": "60V 50A Charger", "type": "3W", "power": "3000W"},
    {"voltage": "72V", "current": "50A", "name": "72V 50A Charger", "type": "3W", "power": "3600W"},
]

SPECIAL_PRODUCTS = [
    {
        "image": "/static/images/onboard_charger.jpg",
        "name": "On-Board Charger",
        "subtitle": "For Three Wheeler",
        "desc": "Compact on-board charger for three wheeler EVs with high efficiency.",
        "features": ["Compact Design", "High Efficiency", "Durable Build"]
    },
    {
        "image": "/static/images/charger_50a.jpg",
        "name": "50A Charger",
        "subtitle": "Heavy Duty",
        "desc": "High power 50A charger suitable for fast charging of three wheelers.",
        "features": ["50A Output", "Fast Charging", "Robust Design"]
    },
    {
        "image": "/static/images/ev_charger.jpg",
        "name": "EV Charger",
        "subtitle": "Universal",
        "desc": "Reliable EV charger suitable for multiple battery configurations.",
        "features": ["Multi-Voltage", "Smart Protection", "Long Life"]
    },
]


# ==================== PUBLIC ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html',
                           company=COMPANY,
                           two_wheeler=TWO_WHEELER,
                           three_wheeler=THREE_WHEELER,
                           special=SPECIAL_PRODUCTS,
                           total_products=len(TWO_WHEELER) + len(THREE_WHEELER))


# ==================== API ROUTES ====================
@app.route('/api/enquiry', methods=['POST'])
def api_enquiry():
    try:
        d = request.get_json() or request.form
        e = Enquiry(
            name=d.get('name', ''), phone=d.get('phone', ''),
            email=d.get('email', ''), product=d.get('product', ''),
            message=d.get('message', ''), source=d.get('source', 'website')
        )
        db.session.add(e)
        db.session.commit()
        return jsonify({"status": "success", "message": "Thank you! We'll contact you soon."})
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)}), 500


@app.route('/api/order', methods=['POST'])
def api_order():
    try:
        d = request.get_json() or request.form
        o = Order(
            name=d.get('name', ''), phone=d.get('phone', ''),
            email=d.get('email', ''), product=d.get('product', ''),
            quantity=d.get('quantity', ''), branch=d.get('branch', ''),
            address=d.get('address', ''), notes=d.get('notes', '')
        )
        db.session.add(o)
        db.session.commit()
        return jsonify({"status": "success", "message": "Order received! We'll confirm shortly."})
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)}), 500


# ==================== ADMIN ROUTES ====================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '')
        admin = Admin.query.filter_by(username=u).first()
        if admin and admin.check_password(p):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password!', 'error')
    return render_template('admin_login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@app.route('/admin')
@login_required
def admin_dashboard():
    enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_dashboard.html',
                           enquiries=enquiries,
                           orders=orders,
                           total_enquiries=len(enquiries),
                           total_orders=len(orders))


@app.route('/admin/delete/enquiry/<int:id>', methods=['POST'])
@login_required
def delete_enquiry(id):
    e = Enquiry.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete/order/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    o = Order.query.get_or_404(id)
    db.session.delete(o)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


# ==================== INIT DB ====================
def init_db():
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('reeshika@2025')
            db.session.add(admin)
            db.session.commit()
            print("\n✅ Default Admin Created")
            print("   Username: admin")
            print("   Password: reeshika@2025\n")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
