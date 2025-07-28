REALMS = []

realm_names = [
    "Body Tempering",
    "Qi Condensation",
    "Foundation Establishment",
    "Core Formation",
    "Nascent Soul",
    "Soul Transformation",
    "Spirit Severing",
    "Void Refinement",
    "Immortal Ascension",
    "Heavenly Immortal",
    "Golden Immortal",
    "Empyrean Immortal",
    "True God",
    "Heavenly Dao Lord",
]

stage_names = [
    "1st Stage",
    "2nd Stage",
    "3rd Stage",
    "4th Stage",
    "5th Stage",
    "6th Stage",
    "7th Stage",
    "8th Stage",
    "9th Stage (Peak)",
]

base_exp = 10
scaling_factor = 1.6

for i, realm in enumerate(realm_names):
    for j, stage in enumerate(stage_names):
        name = f"{realm} - {stage}"
        exp_required = int(base_exp * ((i + 1) ** 2) * ((j + 1) ** scaling_factor))
        REALMS.append({"name": name, "exp_required": exp_required})

def get_realm_info(stage):
    """Get realm information for a given stage"""
    if stage >= len(REALMS):
        return REALMS[-1]  # Return max realm if beyond limit
    return REALMS[stage]