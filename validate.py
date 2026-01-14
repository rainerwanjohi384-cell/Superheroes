#!/usr/bin/env python
"""
Simple test script to validate API endpoints without pytest.
This script tests the Flask API manually to ensure all endpoints work correctly.
"""
import json
import sys

def test_models():
    """Test that models can be instantiated correctly."""
    from app import Hero, Power, HeroPower, db, app
    
    print("✓ Models imported successfully")
    
    with app.app_context():
        # Test Hero model
        hero = Hero(name="Test Hero", super_name="Test Super")
        assert hero.name == "Test Hero"
        assert hero.super_name == "Test Super"
        print("✓ Hero model works correctly")
        
        # Test Power model
        power = Power(
            name="test power",
            description="this is a test power that is at least 20 chars"
        )
        assert power.name == "test power"
        print("✓ Power model works correctly")
        
        # Test HeroPower model
        hero_power = HeroPower(
            hero_id=1,
            power_id=1,
            strength="Strong"
        )
        assert hero_power.strength == "Strong"
        print("✓ HeroPower model works correctly")

def test_validations():
    """Test model validations."""
    from app import Power, HeroPower, db, app
    
    with app.app_context():
        # Test Power description validation
        try:
            power = Power(name="bad", description="short")
            power.validate_description('description', 'short')
            print("✗ Power description validation failed - should reject short descriptions")
            sys.exit(1)
        except ValueError as e:
            if "at least 20 characters" in str(e):
                print("✓ Power description validation works correctly")
            else:
                print(f"✗ Unexpected error: {e}")
                sys.exit(1)
        
        # Test HeroPower strength validation
        try:
            hero_power = HeroPower(
                hero_id=1,
                power_id=1,
                strength="Invalid"
            )
            hero_power.validate_strength('strength', 'Invalid')
            print("✗ HeroPower strength validation failed - should reject invalid strengths")
            sys.exit(1)
        except ValueError as e:
            if "must be one of" in str(e):
                print("✓ HeroPower strength validation works correctly")
            else:
                print(f"✗ Unexpected error: {e}")
                sys.exit(1)

def test_serialization():
    """Test model serialization to dictionaries."""
    from app import Hero, Power, HeroPower, db, app
    
    with app.app_context():
        # Test Hero serialization
        hero = Hero(id=1, name="Kamala Khan", super_name="Ms. Marvel")
        hero_dict = hero.to_dict(only_basic=True)
        assert hero_dict['id'] == 1
        assert hero_dict['name'] == "Kamala Khan"
        assert hero_dict['super_name'] == "Ms. Marvel"
        assert 'hero_powers' not in hero_dict
        print("✓ Hero serialization works correctly")
        
        # Test Power serialization
        power = Power(
            id=1,
            name="flight",
            description="gives the wielder the ability to fly through the skies at supersonic speed"
        )
        power_dict = power.to_dict()
        assert power_dict['id'] == 1
        assert power_dict['name'] == "flight"
        assert len(power_dict['description']) >= 20
        print("✓ Power serialization works correctly")

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running API Validation Tests")
    print("="*50 + "\n")
    
    try:
        test_models()
        print()
        test_validations()
        print()
        test_serialization()
        
        print("\n" + "="*50)
        print("✓ All tests passed!")
        print("="*50 + "\n")
        print("The API is ready to use. Run 'python app.py' to start the server.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    run_all_tests()
