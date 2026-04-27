"""
Crop disease knowledge base — 38 documents for ChromaDB RAG.
Each document contains: symptoms, causes, treatment, prevention.
"""

DISEASE_KNOWLEDGE = [
    {
        "id": "apple_scab",
        "class_name": "Apple___Apple_scab",
        "document": """
        Disease: Apple Scab
        Crop: Apple
        Pathogen: Venturia inaequalis (fungus)
        Symptoms: Olive-green to brown velvety spots on leaves and fruit. 
        Leaves may curl and drop early. Fruit shows dark scabby lesions, 
        cracking, and deformation. Severe infections cause early defoliation.
        Causes: Fungal spores spread via wind and rain in cool, wet spring weather.
        Temperature 16-24°C with wet conditions accelerates spread.
        Treatment: Apply fungicides (captan, mancozeb, myclobutanil) at 7-10 day 
        intervals during wet periods. Remove and destroy infected leaves and fruit.
        Prevention: Plant resistant varieties. Rake fallen leaves. 
        Improve air circulation by pruning. Apply dormant sprays.
        Severity: Moderate to High
        """,
    },
    {
        "id": "apple_black_rot",
        "class_name": "Apple___Black_rot",
        "document": """
        Disease: Apple Black Rot
        Crop: Apple
        Pathogen: Botryosphaeria obtusa (fungus)
        Symptoms: Circular brown lesions on leaves with purple borders. 
        Fruit shows brown rot starting at calyx end, turning black and mummified.
        Bark cankers appear as sunken, reddish-brown areas.
        Causes: Fungal infection through wounds, insect damage, or natural openings.
        Warm humid weather (24-29°C) promotes rapid spread.
        Treatment: Prune and destroy infected wood. Apply fungicides (captan, 
        thiophanate-methyl). Remove mummified fruit from trees and ground.
        Prevention: Maintain tree vigor. Remove dead wood promptly. 
        Control insects that cause wounds. Apply protective fungicide sprays.
        Severity: Moderate to High
        """,
    },
    {
        "id": "apple_cedar_rust",
        "class_name": "Apple___Cedar_apple_rust",
        "document": """
        Disease: Cedar Apple Rust
        Crop: Apple
        Pathogen: Gymnosporangium juniperi-virginianae (fungus)
        Symptoms: Bright orange-yellow spots on upper leaf surfaces in spring.
        Spots develop tube-like structures on leaf undersides. 
        Fruit and twigs may also be infected causing deformation.
        Causes: Requires both apple/crabapple and eastern red cedar as hosts.
        Spores spread from cedar galls to apple during wet spring weather.
        Treatment: Apply fungicides (myclobutanil, triadimefon) from pink bud 
        stage through petal fall. Remove nearby cedar trees if possible.
        Prevention: Plant resistant apple varieties. Remove juniper/cedar hosts 
        within 1-2 mile radius if feasible.
        Severity: Moderate
        """,
    },
    {
        "id": "apple_healthy",
        "class_name": "Apple___healthy",
        "document": """
        Status: Healthy Apple Plant
        Crop: Apple
        Indicators: Deep green uniform leaf color. No spots, lesions or 
        discoloration. Normal leaf shape and size. Good fruit development.
        Maintenance: Regular irrigation, balanced fertilization (NPK), 
        annual pruning for air circulation, pest monitoring.
        Preventive Care: Apply dormant oil spray in late winter. 
        Monitor for early disease signs weekly during growing season.
        Soil pH: 6.0-7.0 optimal. Well-draining soil preferred.
        Severity: None
        """,
    },
    {
        "id": "blueberry_healthy",
        "class_name": "Blueberry___healthy",
        "document": """
        Status: Healthy Blueberry Plant
        Crop: Blueberry
        Indicators: Bright green leaves, no spots or abnormalities.
        Normal berry development and coloration.
        Maintenance: Acidic soil pH 4.5-5.5 essential. 
        Mulch with pine bark to maintain acidity and moisture.
        Fertilize with acid-forming fertilizers (ammonium sulfate).
        Preventive Care: Prune old canes annually. Net against birds.
        Monitor for mummy berry and stem blight diseases.
        Severity: None
        """,
    },
    {
        "id": "cherry_powdery_mildew",
        "class_name": "Cherry_(including_sour)___Powdery_mildew",
        "document": """
        Disease: Cherry Powdery Mildew
        Crop: Cherry (Sweet and Sour)
        Pathogen: Podosphaera clandestina (fungus)
        Symptoms: White powdery coating on young leaves, shoots, and fruit.
        Infected leaves curl upward and may turn yellow. 
        Fruit develops russeting and may crack.
        Causes: Fungal spores thrive in warm days (20-25°C) with cool nights 
        and high humidity. Dry weather does NOT stop spread.
        Treatment: Apply sulfur-based or systemic fungicides (myclobutanil, 
        trifloxystrobin). Remove heavily infected shoots.
        Prevention: Plant resistant varieties. Avoid excessive nitrogen.
        Improve air circulation with proper spacing and pruning.
        Severity: Moderate
        """,
    },
    {
        "id": "cherry_healthy",
        "class_name": "Cherry_(including_sour)___healthy",
        "document": """
        Status: Healthy Cherry Plant
        Crop: Cherry
        Indicators: Dark green glossy leaves, no discoloration or spots.
        Good fruit set and development.
        Maintenance: Full sun location. Well-draining soil pH 6.0-7.0.
        Annual pruning after harvest. Balanced NPK fertilization.
        Preventive Care: Monitor for brown rot and leaf spot diseases.
        Apply dormant copper spray before bud break.
        Severity: None
        """,
    },
    {
        "id": "corn_cercospora",
        "class_name": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "document": """
        Disease: Corn Gray Leaf Spot (Cercospora Leaf Spot)
        Crop: Corn (Maize)
        Pathogen: Cercospora zeae-maydis (fungus)
        Symptoms: Rectangular pale-brown to gray lesions parallel to leaf veins.
        Lesions have distinct parallel edges, 1-6 cm long. 
        Severe infections cause complete leaf blighting from lower leaves upward.
        Causes: Favored by warm (25-30°C), humid conditions and heavy dew.
        Minimum tillage systems increase risk due to infected crop debris.
        Treatment: Apply strobilurin or triazole fungicides at tasseling stage.
        Foliar applications of propiconazole or azoxystrobin are effective.
        Prevention: Plant resistant hybrids. Practice crop rotation.
        Reduce residue with tillage. Ensure proper plant spacing.
        Severity: High — can reduce yield 30-50% in severe cases
        """,
    },
    {
        "id": "corn_common_rust",
        "class_name": "Corn_(maize)___Common_rust_",
        "document": """
        Disease: Corn Common Rust
        Crop: Corn (Maize)
        Pathogen: Puccinia sorghi (fungus)
        Symptoms: Small circular to elongated brick-red pustules on both leaf 
        surfaces. Pustules rupture releasing reddish-brown powdery spores.
        Late-season infections turn black (telial stage).
        Causes: Cool temperatures (16-23°C) with high humidity and heavy dew.
        Wind-dispersed spores from southern regions spread northward.
        Treatment: Apply triazole or strobilurin fungicides if infection 
        appears before tasseling. Mancozeb provides moderate control.
        Prevention: Plant resistant hybrids. Early planting avoids peak 
        spore periods. Monitor fields regularly from V6 stage.
        Severity: Low to Moderate in resistant hybrids
        """,
    },
    {
        "id": "corn_northern_blight",
        "class_name": "Corn_(maize)___Northern_Leaf_Blight",
        "document": """
        Disease: Northern Corn Leaf Blight
        Crop: Corn (Maize)
        Pathogen: Exserohilum turcicum (fungus)
        Symptoms: Long cigar-shaped grayish-green to tan lesions (2.5-15 cm).
        Lesions appear first on lower leaves then move upward.
        Dark green sooty appearance from fungal sporulation in lesion centers.
        Causes: Moderate temperatures (18-27°C) with frequent rainfall and 
        heavy dews. Spread is rapid in dense canopy conditions.
        Treatment: Foliar fungicides (propiconazole, pyraclostrobin) applied 
        at tasseling provide best economic returns.
        Prevention: Resistant hybrids most cost-effective control.
        Crop rotation. Tillage to bury residue.
        Severity: High — major yield loss pathogen in corn
        """,
    },
    {
        "id": "corn_healthy",
        "class_name": "Corn_(maize)___healthy",
        "document": """
        Status: Healthy Corn Plant
        Crop: Corn (Maize)
        Indicators: Uniform green color, erect plants, good ear development.
        No lesions, spots, or abnormal coloration.
        Maintenance: Optimal plant density 65,000-75,000 plants/acre.
        Split nitrogen application: 30% at planting, 70% at V6.
        Irrigation at silking and grain fill stages critical.
        Preventive Care: Scout fields weekly from V4 through R1.
        Monitor for corn earworm, aphids and disease pressure.
        Severity: None
        """,
    },
    {
        "id": "grape_black_rot",
        "class_name": "Grape___Black_rot",
        "document": """
        Disease: Grape Black Rot
        Crop: Grape
        Pathogen: Guignardia bidwellii (fungus)
        Symptoms: Circular reddish-brown lesions on leaves with dark borders.
        Black pycnidia dots visible in lesion centers. 
        Berries shrivel and turn into hard black mummies.
        Causes: Wet warm weather (26-29°C) during bloom and fruit development.
        Overwinters in mummified berries and infected canes.
        Treatment: Apply fungicides (mancozeb, myclobutanil, captan) starting 
        at budbreak. Critical period is from bloom to 4 weeks after.
        Prevention: Remove mummies from vines and ground. Prune infected canes.
        Train vines for maximum air circulation.
        Severity: High — can cause total crop loss
        """,
    },
    {
        "id": "grape_esca",
        "class_name": "Grape___Esca_(Black_Measles)",
        "document": """
        Disease: Grape Esca (Black Measles)
        Crop: Grape
        Pathogen: Complex of fungi (Phaeomoniella, Phaeoacremonium)
        Symptoms: Tiger-stripe pattern on leaves (yellow/red between veins).
        Berries show dark spots (measles). Internal wood shows brown streaking.
        Apoplexy form: sudden wilting and death of entire vine.
        Causes: Fungal complex enters through pruning wounds.
        Stress conditions (drought, excess vigor) trigger symptoms.
        Treatment: No effective curative treatment. 
        Remove and burn severely infected vines.
        Paint pruning wounds with fungicide paste (thiophanate-methyl).
        Prevention: Make clean pruning cuts. Avoid pruning in wet weather.
        Apply wound protectants immediately after pruning.
        Severity: High — chronic and potentially fatal to vines
        """,
    },
    {
        "id": "grape_leaf_blight",
        "class_name": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "document": """
        Disease: Grape Leaf Blight (Isariopsis Leaf Spot)
        Crop: Grape
        Pathogen: Pseudocercospora vitis (fungus)
        Symptoms: Angular dark brown spots on upper leaf surface.
        Spots have yellow halos and may merge causing leaf drop.
        Dark sporulation visible on lower leaf surface.
        Causes: Warm humid conditions. Infection via stomata and wounds.
        Causes: Warm humid conditions (25-30°C). Common in late season.
        Treatment: Copper-based fungicides or mancozeb applied preventively.
        Ensure good coverage on lower leaf surfaces.
        Prevention: Improve air circulation by leaf removal in fruit zone.
        Avoid overhead irrigation. Remove infected leaf debris.
        Severity: Moderate
        """,
    },
    {
        "id": "grape_healthy",
        "class_name": "Grape___healthy",
        "document": """
        Status: Healthy Grape Vine
        Crop: Grape
        Indicators: Deep green leaves with normal shape. No spots or lesions.
        Good cluster development and berry sizing.
        Maintenance: Annual dormant pruning (retain 2-4 buds per spur).
        Balanced fertilization — avoid excess nitrogen after fruit set.
        Irrigation: Drip irrigation preferred to keep foliage dry.
        Preventive Care: Apply dormant copper spray. 
        Scout weekly for powdery mildew and downy mildew from budbreak.
        Severity: None
        """,
    },
    {
        "id": "orange_huanglongbing",
        "class_name": "Orange___Haunglongbing_(Citrus_greening)",
        "document": """
        Disease: Citrus Greening (Huanglongbing - HLB)
        Crop: Orange / Citrus
        Pathogen: Candidatus Liberibacter asiaticus (bacterium)
        Symptoms: Asymmetric yellowing (blotchy mottle) of leaves. 
        Stunted growth, twig dieback. Fruit remains green, is small, 
        lopsided, bitter, and full of aborted seeds.
        Causes: Spread by Asian citrus psyllid insect vector.
        Currently NO cure exists. Most destructive citrus disease worldwide.
        Treatment: No cure. Aggressive psyllid control with insecticides.
        Remove and destroy infected trees immediately to protect neighbors.
        Nutritional sprays may temporarily improve appearance.
        Prevention: Use certified disease-free nursery stock only.
        Control psyllid populations with systemic insecticides.
        Establish new groves away from infected areas.
        Severity: CRITICAL — fatal to citrus trees, no recovery possible
        """,
    },
    {
        "id": "peach_bacterial_spot",
        "class_name": "Peach___Bacterial_spot",
        "document": """
        Disease: Peach Bacterial Spot
        Crop: Peach
        Pathogen: Xanthomonas arboricola pv. pruni (bacterium)
        Symptoms: Small water-soaked spots on leaves turning purple-brown 
        with yellow halos. Spots may fall out leaving shot-hole appearance.
        Fruit shows sunken pits, cracking, and gummosis. 
        Causes: Warm (24-29°C) rainy weather with wind. 
        Bacteria overwinter in infected twig cankers and buds.
        Treatment: Copper hydroxide sprays from budbreak through summer.
        Oxytetracycline (antibiotic) sprays during bloom where permitted.
        Prevention: Plant resistant varieties. Avoid overhead irrigation.
        Windbreaks reduce spread. Remove infected twigs during pruning.
        Severity: Moderate to High
        """,
    },
    {
        "id": "peach_healthy",
        "class_name": "Peach___healthy",
        "document": """
        Status: Healthy Peach Tree
        Crop: Peach
        Indicators: Glossy green leaves, vigorous shoot growth.
        Good fruit sizing and color development. No gummosis or cankers.
        Maintenance: Annual dormant pruning for open-center canopy.
        Thin fruit to 15-20 cm spacing for size and quality.
        Fertilize based on annual shoot growth (45-60 cm optimal).
        Preventive Care: Dormant copper spray for leaf curl and bacterial spot.
        Monitor for oriental fruit moth and peach tree borer.
        Severity: None
        """,
    },
    {
        "id": "pepper_bacterial_spot",
        "class_name": "Pepper,_bell___Bacterial_spot",
        "document": """
        Disease: Pepper Bacterial Spot
        Crop: Bell Pepper
        Pathogen: Xanthomonas euvesicatoria (bacterium)
        Symptoms: Small water-soaked circular spots on leaves turning brown 
        with yellow halos. Severe defoliation occurs. Fruit shows raised 
        scabby lesions reducing marketability.
        Causes: Warm (24-30°C) wet weather. Spread by rain splash and 
        wind. Seed transmission is primary introduction route.
        Treatment: Copper bactericides combined with mancozeb applied 
        weekly during wet periods. Avoid resistance by rotating chemistries.
        Prevention: Use certified disease-free seed or hot-water treated seed.
        Avoid overhead irrigation. Crop rotation with non-solanaceous crops.
        Severity: Moderate to High
        """,
    },
    {
        "id": "pepper_healthy",
        "class_name": "Pepper,_bell___healthy",
        "document": """
        Status: Healthy Bell Pepper Plant
        Crop: Bell Pepper
        Indicators: Dark green sturdy leaves, good flower set and fruit development.
        No spots, wilting, or abnormal growth.
        Maintenance: Consistent moisture — avoid drought stress and waterlogging.
        Calcium sprays prevent blossom end rot. Support plants with stakes.
        Fertilize with balanced NPK plus calcium and magnesium.
        Preventive Care: Monitor for aphids, thrips, and spider mites.
        Rotate crops every 3-4 years. Mulch to conserve moisture.
        Severity: None
        """,
    },
    {
        "id": "potato_early_blight",
        "class_name": "Potato___Early_blight",
        "document": """
        Disease: Potato Early Blight
        Crop: Potato
        Pathogen: Alternaria solani (fungus)
        Symptoms: Dark brown concentric ring lesions (target-board pattern) 
        on older lower leaves first. Yellow halo surrounds lesions.
        Severe defoliation reduces tuber yield and size.
        Causes: Warm (24-29°C) humid conditions. Stress (drought, nutrient 
        deficiency) increases susceptibility. Overwinters in infected debris.
        Treatment: Apply chlorothalonil, mancozeb, or azoxystrobin fungicides 
        preventively starting at first symptom appearance.
        Prevention: Use certified seed tubers. Maintain plant nutrition.
        Crop rotation (3+ years). Destroy volunteer potato plants.
        Severity: Moderate
        """,
    },
    {
        "id": "potato_late_blight",
        "class_name": "Potato___Late_blight",
        "document": """
        Disease: Potato Late Blight
        Crop: Potato
        Pathogen: Phytophthora infestans (oomycete)
        Symptoms: Water-soaked pale green to brown lesions on leaves with 
        white mold on undersides in humid conditions. 
        Entire field can collapse within days. Tuber rot (brown granular).
        Causes: Caused Irish Potato Famine of 1840s. Cool (10-20°C) wet 
        weather. Can spread at epidemic rate under favorable conditions.
        Treatment: Apply mancozeb, chlorothalonil, or specific oomycete 
        fungicides (metalaxyl, cymoxanil) immediately upon detection.
        Prevention: Plant resistant varieties. Apply preventive fungicides 
        in high-risk weather. Destroy infected plant material immediately.
        Severity: CRITICAL — can destroy entire crop in days
        """,
    },
    {
        "id": "potato_healthy",
        "class_name": "Potato___healthy",
        "document": """
        Status: Healthy Potato Plant
        Crop: Potato
        Indicators: Uniform dark green foliage, vigorous upright growth.
        No lesions, wilting, or discoloration. Good tuber set.
        Maintenance: Hill soil around stems twice during growing season.
        Consistent irrigation — avoid waterlogging. Stop irrigation 2 
        weeks before harvest to harden skin.
        Preventive Care: Scout weekly for early and late blight.
        Apply preventive fungicides in wet weather periods.
        Severity: None
        """,
    },
    {
        "id": "raspberry_healthy",
        "class_name": "Raspberry___healthy",
        "document": """
        Status: Healthy Raspberry Plant
        Crop: Raspberry
        Indicators: Vigorous cane growth, healthy green leaves, good fruit set.
        No rust spots, cane diseases, or yellowing.
        Maintenance: Remove old fruited canes after harvest.
        Train new canes to trellis. Soil pH 5.5-6.5.
        Mulch to suppress weeds and conserve moisture.
        Preventive Care: Monitor for raspberry cane borer and aphids.
        Apply dormant lime sulfur spray for cane diseases.
        Severity: None
        """,
    },
    {
        "id": "soybean_healthy",
        "class_name": "Soybean___healthy",
        "document": """
        Status: Healthy Soybean Plant
        Crop: Soybean
        Indicators: Uniform trifoliate leaves, vigorous growth, good pod set.
        Proper nodulation on roots (nitrogen fixation). No yellowing or lesions.
        Maintenance: Inoculate seed with Bradyrhizobium before planting.
        Optimal plant population 250,000-350,000 plants/acre.
        Preventive Care: Scout for soybean rust, sudden death syndrome.
        Monitor for soybean aphid and bean leaf beetle populations.
        Severity: None
        """,
    },
    {
        "id": "squash_powdery_mildew",
        "class_name": "Squash___Powdery_mildew",
        "document": """
        Disease: Squash Powdery Mildew
        Crop: Squash / Cucurbits
        Pathogen: Podosphaera xanthii (fungus)
        Symptoms: White powdery coating on upper and lower leaf surfaces.
        Infected leaves yellow and die prematurely. 
        Reduces fruit size and quality. Does NOT require wet leaves to spread.
        Causes: Warm days (20-30°C), cool nights, and HIGH humidity.
        Unlike most fungal diseases, spreads in DRY conditions too.
        Treatment: Apply potassium bicarbonate, sulfur, or systemic fungicides 
        (myclobutanil, tebuconazole). Neem oil provides organic option.
        Prevention: Plant resistant varieties. Ensure good air circulation.
        Avoid water stress. Grow in full sun locations.
        Severity: Moderate
        """,
    },
    {
        "id": "strawberry_leaf_scorch",
        "class_name": "Strawberry___Leaf_scorch",
        "document": """
        Disease: Strawberry Leaf Scorch
        Crop: Strawberry
        Pathogen: Diplocarpon earlianum (fungus)
        Symptoms: Small dark purple to reddish spots on upper leaf surface.
        Spots enlarge with tan or gray centers. In severe cases leaves 
        turn entirely reddish-purple (scorched appearance) and die.
        Causes: Wet cool weather. Spreads by rain splash.
        Most severe in poorly drained fields.
        Treatment: Apply captan or thiram fungicides. 
        Remove and destroy heavily infected leaves.
        Prevention: Plant certified disease-free transplants.
        Renovate plantings annually after fruiting. Avoid overhead irrigation.
        Severity: Moderate
        """,
    },
    {
        "id": "strawberry_healthy",
        "class_name": "Strawberry___healthy",
        "document": """
        Status: Healthy Strawberry Plant
        Crop: Strawberry
        Indicators: Bright green trifoliate leaves, good runner production.
        Uniform berry development, good size and red coloration.
        Maintenance: Soil pH 5.5-6.5. Renovate June-bearing plants after 
        harvest. Replace plants every 3-4 years.
        Preventive Care: Monitor for two-spotted spider mites.
        Drip irrigation preferred. Straw mulch protects fruit.
        Severity: None
        """,
    },
    {
        "id": "tomato_bacterial_spot",
        "class_name": "Tomato___Bacterial_spot",
        "document": """
        Disease: Tomato Bacterial Spot
        Crop: Tomato
        Pathogen: Xanthomonas vesicatoria (bacterium)
        Symptoms: Small water-soaked circular spots on leaves (1-3mm), 
        turning brown with yellow halos. Scab-like lesions on fruit.
        Severe defoliation exposes fruit to sunscald.
        Causes: Warm (24-30°C) wet weather. Rain splash spreads bacteria.
        Seed and transplant transmission introduces to new fields.
        Treatment: Copper hydroxide + mancozeb tank mix applied weekly.
        Bactericides less effective once disease is established.
        Prevention: Certified disease-free seed. Hot-water seed treatment.
        Drip irrigation. Stake and prune for air circulation.
        Severity: Moderate to High
        """,
    },
    {
        "id": "tomato_early_blight",
        "class_name": "Tomato___Early_blight",
        "document": """
        Disease: Tomato Early Blight
        Crop: Tomato
        Pathogen: Alternaria solani (fungus)
        Symptoms: Dark brown concentric ring lesions (target pattern) on 
        older lower leaves first. Yellow halo around lesions. 
        Stem lesions (collar rot) can girdle seedlings.
        Causes: Warm (24-29°C) humid conditions. Stressed plants more 
        susceptible. Survives in crop debris and soil.
        Treatment: Apply chlorothalonil, mancozeb, or azoxystrobin starting 
        at first symptom appearance. 7-10 day spray intervals.
        Prevention: Crop rotation. Stake plants. Mulch to prevent 
        soil splash. Remove lower leaves touching soil.
        Severity: Moderate — most common tomato disease
        """,
    },
    {
        "id": "tomato_late_blight",
        "class_name": "Tomato___Late_blight",
        "document": """
        Disease: Tomato Late Blight
        Crop: Potato
        Pathogen: Phytophthora infestans (oomycete)
        Symptoms: Large irregularly shaped water-soaked greenish-gray lesions.
        White mold on leaf undersides in humid conditions. 
        Brown greasy lesions on stems. Fruit shows large brown lesions.
        Causes: Cool (10-20°C) wet foggy conditions. Spreads extremely rapidly.
        Spores travel miles on wind. Can destroy crop in 1 week.
        Treatment: Apply metalaxyl, mancozeb, chlorothalonil IMMEDIATELY.
        Destroy infected plants — do NOT compost.
        Prevention: Resistant varieties. Preventive fungicide program.
        Avoid overhead irrigation. Destroy all solanaceous crop debris.
        Severity: CRITICAL — fastest spreading tomato disease
        """,
    },
    {
        "id": "tomato_leaf_mold",
        "class_name": "Tomato___Leaf_Mold",
        "document": """
        Disease: Tomato Leaf Mold
        Crop: Tomato
        Pathogen: Passalora fulva (fungus)
        Symptoms: Pale greenish-yellow spots on upper leaf surface.
        Olive-green to grayish-brown velvet mold on lower leaf surface.
        Older leaves affected first. Primarily a greenhouse/tunnel disease.
        Causes: High humidity (>85%) with moderate temperatures (22-25°C).
        Thrives in enclosed growing environments with poor ventilation.
        Treatment: Apply copper-based fungicides or chlorothalonil.
        Reduce humidity by improving ventilation immediately.
        Prevention: Resistant varieties most effective. 
        Maintain humidity below 85%. Stake for air flow. Prune lower leaves.
        Severity: Moderate — mainly in protected cultivation
        """,
    },
    {
        "id": "tomato_septoria",
        "class_name": "Tomato___Septoria_leaf_spot",
        "document": """
        Disease: Tomato Septoria Leaf Spot
        Crop: Tomato
        Pathogen: Septoria lycopersici (fungus)
        Symptoms: Numerous small circular spots (3-6mm) with white or 
        gray centers and dark brown margins. Black fruiting bodies (pycnidia)
        visible in spot centers. Severe defoliation from bottom up.
        Causes: Warm (20-25°C) wet rainy conditions. 
        Spreads rapidly by rain splash. Survives on debris and weeds.
        Treatment: Chlorothalonil, mancozeb, or copper fungicides at 
        7-10 day intervals. Begin at first symptom appearance.
        Prevention: Crop rotation (2+ years). Stake plants. 
        Mulch soil. Remove infected lower leaves. Avoid wetting foliage.
        Severity: High — causes severe defoliation reducing yield
        """,
    },
    {
        "id": "tomato_spider_mites",
        "class_name": "Tomato___Spider_mites Two-spotted_spider_mite",
        "document": """
        Disease: Tomato Spider Mite Damage
        Crop: Tomato
        Pest: Tetranychus urticae (Two-spotted spider mite)
        Symptoms: Stippling (tiny yellow dots) on upper leaf surface.
        Bronze or silvery leaf sheen. Fine webbing on leaf undersides.
        Leaves yellow and drop. Severe damage causes plant death.
        Causes: Hot dry conditions (30°C+) favor rapid mite reproduction.
        Drought stress worsens damage. Over-use of insecticides 
        kills natural predators allowing mite outbreaks.
        Treatment: Apply acaricides (abamectin, bifenazate, spiromesifen).
        Rotate chemistry to prevent resistance. Strong water spray.
        Neem oil effective for organic control.
        Prevention: Maintain plant moisture. Avoid broad-spectrum insecticides.
        Introduce predatory mites (Phytoseiidae). Monitor in hot dry periods.
        Severity: High in hot dry weather
        """,
    },
    {
        "id": "tomato_target_spot",
        "class_name": "Tomato___Target_Spot",
        "document": """
        Disease: Tomato Target Spot
        Crop: Tomato
        Pathogen: Corynespora cassiicola (fungus)
        Symptoms: Brown circular lesions with concentric rings on leaves.
        Lesions have yellow halos. Fruit shows sunken brown spots.
        Stems and petioles also affected.
        Causes: Warm (25-30°C) humid conditions. Spread by rain splash 
        and air currents. Survives in infected plant debris.
        Treatment: Apply azoxystrobin, chlorothalonil, or mancozeb fungicides.
        Early application critical — difficult to control once established.
        Prevention: Avoid dense planting. Stake for air circulation.
        Crop rotation. Remove and destroy infected plant material.
        Severity: Moderate to High
        """,
    },
    {
        "id": "tomato_yellow_leaf_curl",
        "class_name": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "document": """
        Disease: Tomato Yellow Leaf Curl Virus (TYLCV)
        Crop: Tomato
        Pathogen: Tomato yellow leaf curl virus (Begomovirus)
        Symptoms: Upward curling and yellowing of leaf margins and tips.
        Stunted plant growth. Flowers drop reducing fruit set dramatically.
        Affected plants produce few to no fruit.
        Causes: Transmitted exclusively by silverleaf whitefly (Bemisia tabaci).
        Cannot spread plant-to-plant without insect vector.
        Treatment: NO cure once infected. Remove and destroy infected plants.
        Control whitefly populations aggressively with imidacloprid or 
        thiamethoxam. Yellow sticky traps to monitor populations.
        Prevention: Use virus-resistant tomato varieties (first choice).
        Reflective mulches repel whiteflies. Insect-proof screens in nurseries.
        Severity: High — causes near total crop failure in susceptible varieties
        """,
    },
    {
        "id": "tomato_mosaic_virus",
        "class_name": "Tomato___Tomato_mosaic_virus",
        "document": """
        Disease: Tomato Mosaic Virus (ToMV)
        Crop: Tomato
        Pathogen: Tomato mosaic virus (Tobamovirus)
        Symptoms: Light and dark green mosaic mottling pattern on leaves.
        Leaves may show fern-leaf distortion. Stunted growth.
        Fruit shows internal brown discoloration. Yellow spotting on fruit.
        Causes: Extremely stable virus — persists in soil and debris for 
        2+ years. Mechanically transmitted through contact, tools, 
        and hands. Seed transmission possible.
        Treatment: No cure. Rogue and destroy infected plants.
        Disinfect tools with 10% bleach solution between plants.
        Prevention: Certified virus-free seed. Resistant varieties.
        Wash hands thoroughly before working with plants.
        Avoid tobacco use near plants (related virus).
        Severity: Moderate to High — spreads easily by contact
        """,
    },
    {
        "id": "tomato_healthy",
        "class_name": "Tomato___healthy",
        "document": """
        Status: Healthy Tomato Plant
        Crop: Tomato
        Indicators: Deep green leaves, vigorous growth, good flower and 
        fruit set. No spots, wilting, or discoloration.
        Maintenance: Stake or cage plants. Consistent deep watering.
        Fertilize with phosphorus-rich fertilizer at transplant, then 
        switch to potassium-rich during fruiting.
        Calcium sprays prevent blossom end rot.
        Preventive Care: Scout weekly for early and late blight, 
        septoria leaf spot. Apply preventive copper spray in wet weather.
        Severity: None
        """,
    },
]