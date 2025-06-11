def get_learning_resources(career):
    """Get learning resources for a career (extendable)"""
    resources = {
        "Software Developer": ["freeCodeCamp", "The Odin Project", "LeetCode"],
        "Data Scientist": ["Kaggle", "Coursera Data Science Specialization"],
        "Graphic Designer": ["Behance", "Canva Design School", "Adobe Tutorials"]
    }
    return resources.get(career, ["LinkedIn Learning", "Coursera", "Udacity"])