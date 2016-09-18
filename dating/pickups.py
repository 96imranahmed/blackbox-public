import random as r

PICKUPS = ["Hey, tie your shoes! I don’t want you falling for anyone else.",
            "Hey, do you believe in love at the first sight, or should I walk by again.",
            "If you were a fruit you’d be a fineapple."]

NERDY_PICKUPS = ["Damn girl, is your name Wifi? Because I’m feeling a connection",
                "Are you made of beryllium, gold, and titanium? You must be because you are BeAuTi-ful.",
                "If you were a triangle you'd be acute one.",
                "Are you a singularity? Because the closer I get to you, the faster time seems to slip by.",
                "Do you have 11 protons? Cause you're sodium fine.",
                "You're sweeter than 3.14",
                "Are you a carbon sample? Because I want to date you.",
                "I'd like to calculate the slope of those curves.",
                "According to the second law of thermodynamics, you're supposed to share your hotness with me.",
                "Are you sitting on the F5 key? Because your backside is refreshing.",
                "If I was an enzyme, I’d be helicase so I could unzip your genes."]

def get_pickups(nerdy):
    if nerdy:
        return NERDY_PICKUPS[r.randint(0, len(NERDY_PICKUPS) - 1)]
    else:
        return PICKUPS[r.randint(0, len(PICKUPS) - 1)]