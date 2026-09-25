"""
Rule-based keyword-matching FAQ provider.

This is NOT a language model — it's a small, transparent set of
canned answers to the example questions in spec §6, always shaped
into the required Problem/Cause/Action/Precautions/Expert structure.
It's the honest default (see get_ai_provider() in service.py): rather
than faking an LLM, unmatched questions get a clear "I can only help
with a few common topics right now" response instead of an invented
answer. A real LLM provider can replace this later without changing
respond()'s signature or the response shape.
"""
from .base import AIAssistantProvider

# Each topic: keywords to match (English + a few Telugu terms), and a
# structured answer in English + Telugu.
FAQ_TOPICS = [
    {
        "id": "crop_selection",
        "keywords_en": ["which crop", "what crop", "crop should i grow", "best crop", "what to grow", "what should i grow", "crop to grow", "recommend a crop", "recommend crop"],
        "keywords_te": ["ఏ పంట", "పంట వేయాలి", "పంట సూచించు", "ఏ పంట వేయాలి"],
        "en": {
            "problem": "You're deciding which crop to grow.",
            "possible_cause": "Crop choice depends on your soil type, season, water availability, and local climate.",
            "recommended_action": "Use the Crop Recommendation tool with your soil and climate details for a ranked list of suitable crops.",
            "precautions": "Don't switch crops based on price alone — factor in your soil's suitability and water access.",
            "when_to_contact_expert": "If you're planning a large investment or a crop you haven't grown before, consult your local agriculture extension officer first.",
        },
        "te": {
            "problem": "మీరు ఏ పంట వేయాలో నిర్ణయించుకుంటున్నారు.",
            "possible_cause": "పంట ఎంపిక మీ నేల రకం, సీజన్, నీటి లభ్యత మరియు స్థానిక వాతావరణంపై ఆధారపడి ఉంటుంది.",
            "recommended_action": "మీ నేల మరియు వాతావరణ వివరాలతో క్రాప్ రికమండేషన్ టూల్‌ని ఉపయోగించండి.",
            "precautions": "ధర ఆధారంగా మాత్రమే పంట మార్చవద్దు — నేల అనుకూలత మరియు నీటి లభ్యతను పరిగణించండి.",
            "when_to_contact_expert": "పెద్ద పెట్టుబడి లేదా కొత్త పంట అయితే, స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
        },
    },
    {
        "id": "yellow_leaves",
        "keywords_en": ["yellow", "yellowing", "leaves turning", "leaf turning", "leaves are yellow", "leaf color", "leaf colour"],
        "keywords_te": ["ఆకులు పసుపు", "పసుపు రంగు", "ఆకులు పచ్చగా లేవు", "ఆకులు మారుతున్నాయి"],
        "en": {
            "problem": "Your crop's leaves are turning yellow.",
            "possible_cause": "Commonly caused by nitrogen deficiency, overwatering/poor drainage, or early-stage disease.",
            "recommended_action": "Check soil moisture first — if waterlogged, improve drainage. If soil looks dry and depleted, consider a nitrogen top-dressing (see Fertilizer Recommendation).",
            "precautions": "Don't apply extra fertilizer or pesticide without confirming the cause — over-application can worsen the problem.",
            "when_to_contact_expert": "If yellowing spreads rapidly or leaves show spots/lesions alongside it, get an in-person diagnosis promptly — this can indicate disease.",
        },
        "te": {
            "problem": "మీ పంట ఆకులు పసుపు రంగులోకి మారుతున్నాయి.",
            "possible_cause": "సాధారణంగా నత్రజని లోపం, ఎక్కువ నీరు నిలవడం, లేదా ప్రారంభ దశ వ్యాధి వల్ల ఇలా జరుగుతుంది.",
            "recommended_action": "ముందుగా నేల తేమను తనిఖీ చేయండి — నీరు నిలిచి ఉంటే డ్రైనేజీ మెరుగుపరచండి. నేల పొడిగా ఉంటే నత్రజని ఎరువు వేయడాన్ని పరిశీలించండి.",
            "precautions": "కారణం నిర్ధారించకుండా అదనపు ఎరువు లేదా పురుగుమందు వేయవద్దు.",
            "when_to_contact_expert": "పసుపు రంగు వేగంగా వ్యాపిస్తే లేదా మచ్చలు కనిపిస్తే వెంటనే నిపుణుడిని సంప్రదించండి.",
        },
    },
    {
        "id": "fertilizer_timing",
        "keywords_en": ["when should i apply fertilizer", "fertilizer timing", "when to fertilize", "when do i fertilize", "when to apply fertilizer", "when should i fertilize", "best time for fertilizer", "fertilizer schedule"],
        "keywords_te": ["ఎరువు ఎప్పుడు", "ఎప్పుడు ఎరువు వేయాలి", "ఎరువు సమయం"],
        "en": {
            "problem": "You want to know when to apply fertilizer.",
            "possible_cause": "Timing depends on your crop's growth stage — basal doses go in at sowing, top-dressing happens during active growth.",
            "recommended_action": "Use the Fertilizer Recommendation tool with your crop and growth stage for a specific application schedule.",
            "precautions": "Avoid applying fertilizer right before heavy rain — much of it washes away instead of reaching the roots.",
            "when_to_contact_expert": "If your crop shows stunted growth despite fertilizing on schedule, get your soil tested by a local agriculture office.",
        },
        "te": {
            "problem": "ఎరువు ఎప్పుడు వేయాలో మీరు తెలుసుకోవాలనుకుంటున్నారు.",
            "possible_cause": "సమయం పంట పెరుగుదల దశపై ఆధారపడి ఉంటుంది — విత్తే సమయంలో బేసల్ డోస్, పెరుగుదల సమయంలో టాప్-డ్రెస్సింగ్.",
            "recommended_action": "మీ పంట మరియు పెరుగుదల దశతో ఫెర్టిలైజర్ రికమండేషన్ టూల్‌ని ఉపయోగించండి.",
            "precautions": "భారీ వర్షానికి ముందు ఎరువు వేయవద్దు — ఎక్కువ భాగం కొట్టుకుపోతుంది.",
            "when_to_contact_expert": "షెడ్యూల్ ప్రకారం ఎరువు వేసినా పెరుగుదల తక్కువగా ఉంటే, నేల పరీక్ష చేయించండి.",
        },
    },
    {
        "id": "rice_water",
        "keywords_en": ["how much water does rice need", "rice water", "water rice", "watering rice",
                        "irrigate rice", "rice irrigation", "water for rice", "rice needs water",
                        "water requirement rice", "rice water requirement"],
        "keywords_te": ["వరి నీరు", "వరికి నీరు", "వరి నీటిపారుదల", "వరి నీళ్ళు"],
        "en": {
            "problem": "You're asking about rice's water requirement.",
            "possible_cause": "Rice needs standing water for most of its growth cycle — roughly 150-300mm rainfall/irrigation equivalent depending on soil and climate.",
            "recommended_action": "Maintain 2-5cm of standing water through the vegetative stage; you can let the field dry briefly before harvest.",
            "precautions": "Continuous deep flooding beyond what's needed wastes water — alternate wetting and drying can save water without hurting yield.",
            "when_to_contact_expert": "If water access is limited in your area, ask your local agriculture office about water-saving rice cultivation methods (e.g. AWD/SRI).",
        },
        "te": {
            "problem": "వరి నీటి అవసరం గురించి మీరు అడుగుతున్నారు.",
            "possible_cause": "వరి పెరుగుదల చక్రంలో ఎక్కువ భాగం నిలిచిన నీరు అవసరం — నేల మరియు వాతావరణాన్ని బట్టి సుమారు 150-300mm వర్షపాతం/నీటిపారుదల సమానం.",
            "recommended_action": "పెరుగుదల దశలో 2-5cm నిలిచిన నీటిని ఉంచండి; కోతకు ముందు పొలాన్ని కొద్దిగా ఆరనివ్వవచ్చు.",
            "precautions": "అవసరానికి మించి నిరంతరం లోతైన నీరు నిల్వ చేయడం వృధా — తడి-పొడి పద్ధతి నీటిని ఆదా చేస్తుంది.",
            "when_to_contact_expert": "నీటి లభ్యత తక్కువగా ఉంటే, నీటిని ఆదా చేసే వరి సాగు పద్ధతుల గురించి స్థానిక వ్యవసాయ కార్యాలయాన్ని అడగండి.",
        },
    },
    {
        "id": "low_rainfall",
        "keywords_en": ["low rainfall", "rainfall is low", "drought", "no rain", "not enough rain",
                        "little rain", "less rainfall", "water shortage", "hasnt rained",
                        "hasn't rained", "no rainfall", "dry spell", "rain stopped",
                        "no water", "crop is drying", "crops drying"],
        "keywords_te": ["తక్కువ వర్షం", "వర్షం లేదు", "వర్షం రావట్లేదు", "నీరు లేదు"],
        "en": {
            "problem": "Rainfall has been low for your crop.",
            "possible_cause": "Insufficient rainfall stresses crops during critical growth stages, especially flowering and grain-fill.",
            "recommended_action": "Prioritize irrigation during flowering/fruiting stages if water is limited; consider mulching to retain soil moisture.",
            "precautions": "Don't over-irrigate to compensate all at once — sudden waterlogging after drought stress can shock the plant.",
            "when_to_contact_expert": "If this is a season-long shortage, ask your local agriculture office about drought-tolerant crop varieties for next season.",
        },
        "te": {
            "problem": "మీ పంటకు వర్షపాతం తక్కువగా ఉంది.",
            "possible_cause": "సరిపడా వర్షం లేకపోవడం ముఖ్యమైన పెరుగుదల దశలలో, ముఖ్యంగా పూత మరియు గింజ నింపే సమయంలో పంటపై ఒత్తిడి కలిగిస్తుంది.",
            "recommended_action": "నీరు పరిమితంగా ఉంటే పూత/కాయ దశలలో నీటిపారుదలకు ప్రాధాన్యత ఇవ్వండి; నేల తేమను నిలుపుకోవడానికి మల్చింగ్ పరిశీలించండి.",
            "precautions": "ఒకేసారి ఎక్కువ నీరు పెట్టవద్దు — ఒత్తిడి తర్వాత అకస్మాత్తుగా నీరు నిలవడం మొక్కకు హాని చేస్తుంది.",
            "when_to_contact_expert": "ఇది సీజన్ మొత్తం కొరత అయితే, తదుపరి సీజన్ కోసం కరువును తట్టుకునే రకాల గురించి అడగండి.",
        },
    },
    {
        "id": "fertilizer_choice",
        "keywords_en": ["which fertilizer", "what fertilizer", "suitable fertilizer", "best fertilizer", "recommend fertilizer", "fertilizer should i use", "fertilizer to use"],
        "keywords_te": ["ఏ ఎరువు", "ఏ ఎరువు వేయాలి", "ఎరువు సూచించు", "ఏ ఎరువు మంచిది"],
        "en": {
            "problem": "You want to know which fertilizer suits your crop.",
            "possible_cause": "The right fertilizer depends on which nutrient (N/P/K) your soil is deficient in for that specific crop.",
            "recommended_action": "Use the Fertilizer Recommendation tool with your crop and current soil NPK levels for a specific recommendation and quantity.",
            "precautions": "Never mix multiple chemical fertilizers without checking compatibility — some combinations reduce effectiveness or harm the crop.",
            "when_to_contact_expert": "If you don't know your soil's current NPK levels, get a soil test done before applying any fertilizer.",
        },
        "te": {
            "problem": "మీ పంటకు ఏ ఎరువు సరిపోతుందో మీరు తెలుసుకోవాలనుకుంటున్నారు.",
            "possible_cause": "సరైన ఎరువు మీ నేలలో ఆ నిర్దిష్ట పంటకు ఏ పోషకం (N/P/K) లోపించిందనే దానిపై ఆధారపడి ఉంటుంది.",
            "recommended_action": "మీ పంట మరియు ప్రస్తుత నేల NPK స్థాయిలతో ఫెర్టిలైజర్ రికమండేషన్ టూల్‌ని ఉపయోగించండి.",
            "precautions": "అనుకూలతను తనిఖీ చేయకుండా బహుళ రసాయన ఎరువులను కలపవద్దు.",
            "when_to_contact_expert": "మీ నేల ప్రస్తుత NPK స్థాయిలు తెలియకపోతే, ఏదైనా ఎరువు వేయడానికి ముందు నేల పరీక్ష చేయించండి.",
        },
    },
]

FALLBACK = {
    "en": {
        "problem": "I couldn't match your question to a topic I currently cover.",
        "possible_cause": (
            "This assistant currently answers questions about: "
            "crop selection, yellow/discoloured leaves, fertilizer timing, "
            "fertilizer choice, rice water needs, and low rainfall/drought. "
            "Your question didn't closely match any of these."
        ),
        "recommended_action": (
            "Try rephrasing — for example: 'which crop should I grow?', "
            "'why are my leaves turning yellow?', 'when should I fertilize?', "
            "'which fertilizer for cotton?', 'how much water does rice need?', "
            "or 'what to do when rainfall is low?'. "
            "You can also use the Crop/Fertilizer Recommendation tools directly."
        ),
        "precautions": "",
        "when_to_contact_expert": "For anything urgent or specific to your field, contact your local agriculture extension officer.",
    },
    "te": {
        "problem": "మీ ప్రశ్నను నేను ప్రస్తుతం కవర్ చేసే అంశంతో సరిపోల్చలేకపోయాను.",
        "possible_cause": (
            "ఈ అసిస్టెంట్ ప్రస్తుతం ఈ అంశాలపై సమాధానం ఇస్తుంది: "
            "పంట ఎంపిక, పసుపు ఆకులు, ఎరువు సమయం, ఏ ఎరువు వేయాలి, వరి నీటి అవసరం, తక్కువ వర్షపాతం."
        ),
        "recommended_action": (
            "ఉదాహరణకు ఇలా అడగండి: 'ఏ పంట వేయాలి?', 'ఆకులు పసుపు ఎందుకు అవుతున్నాయి?', "
            "'ఎప్పుడు ఎరువు వేయాలి?', 'ఏ ఎరువు మంచిది?'. "
            "లేదా క్రాప్/ఫెర్టిలైజర్ రికమండేషన్ టూల్స్‌ని నేరుగా ఉపయోగించండి."
        ),
        "precautions": "",
        "when_to_contact_expert": "అత్యవసరమైనది లేదా మీ పొలానికి ప్రత్యేకమైనది అయితే, స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
    },
}


class RuleBasedFAQProvider(AIAssistantProvider):
    def respond(self, *, question: str, language: str, context: dict) -> dict:
        q = question.lower().strip()
        lang = language if language in ("en", "te") else "en"

        # Use farmer's known crops from profile context to boost relevance
        farmer_crops = [c.lower() for c in (context.get("crops_grown") or [])]

        for topic in FAQ_TOPICS:
            keywords = topic["keywords_en"] + topic.get("keywords_te", [])
            if any(kw in q for kw in keywords):
                answer = dict(topic[lang])
                answer["provider"] = "rule_based"
                answer["topic"] = topic["id"]
                # Personalize with profile context if available
                if farmer_crops and topic["id"] in ("crop_selection", "fertilizer_choice", "fertilizer_timing"):
                    crops_str = ", ".join(farmer_crops)
                    answer = dict(answer)
                    answer["recommended_action"] = (
                        f"Based on your profile crops ({crops_str}): " + answer["recommended_action"]
                    )
                return answer

        answer = dict(FALLBACK[lang])
        answer["provider"] = "rule_based"
        answer["topic"] = "unmatched"
        return answer
