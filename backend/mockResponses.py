import random


MOCK_RESPONSES = [
    {
        "real_summary": "Scientists have discovered a new exoplanet that may support life.",
        "fake_summary": "Scientists have found an exoplanet populated by an advanced alien civilization.",
        "explanation": "The fake summary introduces an impossible scientific claim about aliens with no supporting evidence."
    },
    {
        "real_summary": "The government reports a 2.5% increase in GDP for the last quarter.",
        "fake_summary": "The government secretly manipulates GDP numbers to hide economic collapse.",
        "explanation": "The fake story uses conspiracy-style language to create distrust in official statistics."
    },
    {
        "real_summary": "A new medical study shows that exercise reduces the risk of heart disease.",
        "fake_summary": "A viral post claims that drinking soda every day reduces heart disease risk.",
        "explanation": "The fake summary misinterprets science and promotes an unhealthy habit."
    }
]

def get_mock_response():
    return random.choice(MOCK_RESPONSES)
