import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_greengrass_recipe():
    print("==================================================")
    print("PHASE 11 AWS IOT GREENGRASS COMPONENT TEST")
    print("==================================================")
    
    recipe_path = "cloud/greengrass/recipe.json"
    assert os.path.exists(recipe_path), f"Greengrass recipe not found at {recipe_path}"
    
    with open(recipe_path, "r") as f:
        recipe = json.load(f)
        
    assert recipe["ComponentName"] == "com.smartcity.traffic.ai"
    assert recipe["ComponentVersion"] == "1.0.0"
    assert "Manifests" in recipe
    
    print(f"Verified Greengrass Recipe Component Name: {recipe['ComponentName']}")
    print(f"Verified Greengrass Recipe Version: {recipe['ComponentVersion']}")
    
    print("\n==================================================")
    print("PHASE 11 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_greengrass_recipe()
