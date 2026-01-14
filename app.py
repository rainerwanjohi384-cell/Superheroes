#!/usr/bin/env python
"""
Superheroes API - A Flask application for managing heroes and their superpowers.
"""
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)

class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')
    
    def to_dict(self, only_basic=False):
        result = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        if not only_basic:
            result['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return result

class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')
    
    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("description must be present and at least 20 characters long")
        return value
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(100), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(f"strength must be one of {valid_strengths}")
        return value
    
    def to_dict(self):
        return {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength,
            'hero': {
                'id': self.hero.id,
                'name': self.hero.name,
                'super_name': self.hero.super_name
            },
            'power': self.power.to_dict()
        }

@app.route('/heroes', methods=['GET'])
def get_heroes():
    """Get all heroes with basic info only (no hero_powers)."""
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(only_basic=True) for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    """Get a specific hero with their hero_powers."""
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict())

@app.route('/powers', methods=['GET'])
def get_powers():
    """Get all powers."""
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    """Get a specific power."""
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    """Update a power's description."""
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    
    if 'description' in data:
        power.description = data['description']
    
    try:
        db.session.commit()
        return jsonify(power.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    """Create a new association between a hero and a power."""
    data = request.get_json()
    
    try:
        hero_power = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

def init_db():
    """Initialize the database with seed data."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create Powers
        powers = [
            Power(name='super strength', description='gives the wielder super-human strengths'),
            Power(name='flight', description='gives the wielder the ability to fly through the skies at supersonic speed'),
            Power(name='super human senses', description='allows the wielder to use her senses at a super-human level'),
            Power(name='elasticity', description='can stretch the human body to extreme lengths'),
        ]
        
        for power in powers:
            db.session.add(power)
        db.session.commit()
        
        # Create Heroes
        heroes = [
            Hero(name='Kamala Khan', super_name='Ms. Marvel'),
            Hero(name='Doreen Green', super_name='Squirrel Girl'),
            Hero(name='Gwen Stacy', super_name='Spider-Gwen'),
            Hero(name='Janet Van Dyne', super_name='The Wasp'),
            Hero(name='Wanda Maximoff', super_name='Scarlet Witch'),
            Hero(name='Carol Danvers', super_name='Captain Marvel'),
            Hero(name='Jean Grey', super_name='Dark Phoenix'),
            Hero(name='Ororo Munroe', super_name='Storm'),
            Hero(name='Kitty Pryde', super_name='Shadowcat'),
            Hero(name='Elektra Natchios', super_name='Elektra'),
        ]
        
        for hero in heroes:
            db.session.add(hero)
        db.session.commit()
        
        # Create HeroPowers
        hero_powers = [
            HeroPower(hero_id=1, power_id=2, strength='Strong'),
            HeroPower(hero_id=2, power_id=1, strength='Average'),
            HeroPower(hero_id=3, power_id=3, strength='Strong'),
            HeroPower(hero_id=4, power_id=2, strength='Strong'),
            HeroPower(hero_id=5, power_id=1, strength='Average'),
            HeroPower(hero_id=6, power_id=2, strength='Strong'),
            HeroPower(hero_id=7, power_id=4, strength='Weak'),
            HeroPower(hero_id=8, power_id=2, strength='Average'),
            HeroPower(hero_id=9, power_id=3, strength='Weak'),
            HeroPower(hero_id=10, power_id=1, strength='Strong'),
        ]
        
        for hero_power in hero_powers:
            db.session.add(hero_power)
        db.session.commit()
        
        print("✅ Database initialized and seeded successfully!")

if __name__ == '__main__':
    init_db()
    print("\n🚀 Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
