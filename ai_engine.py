import json
from PIL import Image
from transformers import pipeline
from cachetools import TTLCache
import traceback


image_classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

cache = TTLCache(maxsize=100, ttl=3600)



def preprocess_image(image_path):

    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))

    return image



def generate_design(image_path, style_theme):

    cache_key = f"{image_path}_{style_theme}"

    if cache_key in cache:
        return cache[cache_key]

    try:

        image = preprocess_image(image_path)

        predictions = image_classifier(image)

        room_type = predictions[0]["label"]

        recommendations = generate_recommendations(room_type, style_theme)

        result = {
            "room_type": room_type,
            "style": style_theme,
            "recommendations": recommendations
        }

        cache[cache_key] = result

        return result

    except Exception as e:

        print("AI generation error:", traceback.format_exc())

        return {
            "error": "AI generation failed",
            "message": str(e)
        }
def generate_recommendations(room_type, style):

    design_library = {

        "modern": {
            "colors": ["white", "gray", "black"],
            "furniture": [
                "minimalist sofa",
                "glass coffee table",
                "metal floor lamp"
            ],
            "placement": "open space layout with clean lines"
        },

        "scandinavian": {
            "colors": ["light wood", "cream", "soft gray"],
            "furniture": [
                "wooden sofa",
                "fabric armchair",
                "round coffee table"
            ],
            "placement": "airy layout with natural light"
        },

        "traditional": {
            "colors": ["brown", "beige", "gold"],
            "furniture": [
                "classic sofa",
                "wooden cabinet",
                "ornate coffee table"
            ],
            "placement": "balanced symmetrical arrangement"
        }
    }

    style_data = design_library.get(style, design_library["modern"])

    return {
        "room_detected": room_type,
        "color_scheme": style_data["colors"],
        "furniture": style_data["furniture"],
        "placement": style_data["placement"]
    }