# Treatment and pathogen reference database for all 16 classes the
# CNN was trained on. This is static reference information only -
# actual detection and confidence always come from the live model.

DISEASE_INFO = {
    "Pepper Bell Bacterial Spot": {
        "pathogen": "Xanthomonas campestris pv. vesicatoria (Bacterium)",
        "treatment": "1. Remove and destroy infected leaves.\n2. Apply copper-based bactericides on a regular schedule.\n3. Avoid overhead irrigation and working with plants while foliage is wet.",
        "remediation_speed": "Medium Priority",
    },
    "Pepper Bell Healthy": {
        "pathogen": "None detected",
        "treatment": "No treatment needed. Continue regular monitoring and balanced fertilization.",
        "remediation_speed": "No Action Needed",
    },
    "Potato Early Blight": {
        "pathogen": "Alternaria solani (Fungus)",
        "treatment": "1. Remove lower infected leaves.\n2. Apply chlorothalonil or mancozeb-based fungicides.\n3. Rotate crops and avoid planting potatoes in the same spot each season.",
        "remediation_speed": "Medium Priority",
    },
    "Potato Late Blight": {
        "pathogen": "Phytophthora infestans (Oomycete)",
        "treatment": "1. Destroy infected plant debris immediately - this pathogen spreads fast.\n2. Apply fungicides containing mancozeb or chlorothalonil.\n3. Improve field drainage and spacing to reduce humidity around plants.",
        "remediation_speed": "Critical Alert",
    },
    "Potato Healthy": {
        "pathogen": "None detected",
        "treatment": "No treatment needed. Continue regular monitoring.",
        "remediation_speed": "No Action Needed",
    },
    "Tomato Bacterial Spot": {
        "pathogen": "Xanthomonas spp. (Bacterium)",
        "treatment": "1. Remove infected foliage.\n2. Apply copper-based sprays.\n3. Use disease-free certified seed and avoid handling wet plants.",
        "remediation_speed": "Medium Priority",
    },
    "Tomato Early Blight": {
        "pathogen": "Alternaria solani (Fungus)",
        "treatment": "1. Remove infected lower leaves to prevent spore splash.\n2. Apply copper-based fungicides or chlorothalonil weekly.\n3. Use drip irrigation instead of overhead watering.",
        "remediation_speed": "High Priority",
    },
    "Tomato Late Blight": {
        "pathogen": "Phytophthora infestans (Oomycete)",
        "treatment": "1. Remove and destroy infected plants promptly.\n2. Apply protective fungicides before wet weather.\n3. Space plants for good air circulation.",
        "remediation_speed": "Critical Alert",
    },
    "Tomato Leaf Mold": {
        "pathogen": "Passalora fulva (Fungus)",
        "treatment": "1. Improve greenhouse or field ventilation to lower humidity.\n2. Remove affected leaves.\n3. Apply approved fungicides if the infection spreads.",
        "remediation_speed": "Medium Priority",
    },
    "Tomato Septoria Leaf Spot": {
        "pathogen": "Septoria lycopersici (Fungus)",
        "treatment": "1. Remove infected lower leaves.\n2. Apply fungicide sprays at the first sign of spotting.\n3. Mulch around the base of plants to reduce soil splash.",
        "remediation_speed": "Medium Priority",
    },
    "Tomato Spider Mites": {
        "pathogen": "Tetranychus urticae (Pest - two-spotted spider mite)",
        "treatment": "1. Spray leaves (including undersides) with water to dislodge mites.\n2. Apply insecticidal soap or neem oil.\n3. Introduce natural predators like ladybugs where feasible.",
        "remediation_speed": "Medium Priority",
    },
    "Tomato Target Spot": {
        "pathogen": "Corynespora cassiicola (Fungus)",
        "treatment": "1. Remove infected leaves and plant debris.\n2. Apply fungicides labeled for target spot.\n3. Avoid dense planting to improve air flow.",
        "remediation_speed": "Medium Priority",
    },
    "Tomato Yellow Leaf Curl Virus": {
        "pathogen": "TYLCV, spread by whiteflies",
        "treatment": "1. Remove and destroy infected plants to limit spread.\n2. Control whitefly populations with insecticidal soap or approved insecticides.\n3. Use reflective mulches and resistant varieties where available.",
        "remediation_speed": "Critical Alert",
    },
    "Tomato Mosaic Virus": {
        "pathogen": "Tobamovirus (ToMV)",
        "treatment": "1. Remove and destroy infected plants - there is no cure once infected.\n2. Disinfect tools between plants.\n3. Wash hands before handling healthy plants, especially after smoking (tobacco can carry the virus).",
        "remediation_speed": "Critical Alert",
    },
    "Tomato Healthy": {
        "pathogen": "None detected",
        "treatment": "No treatment needed. Continue regular monitoring and balanced fertilization.",
        "remediation_speed": "No Action Needed",
    },
    "Unknown Disease": {
        "pathogen": "Not confidently identified",
        "treatment": "The model could not confidently match this leaf to a known class. Try a clearer, well-lit, close-up photo of the affected area, or consult a local agricultural expert.",
        "remediation_speed": "Verify Manually",
    },
}
