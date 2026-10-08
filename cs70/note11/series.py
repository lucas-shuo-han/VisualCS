"""series.py for CS70 Note 11, The Stable Matching Problem: one language, ten episodes."""

SOURCE_LANG = "en"
LANGS = [SOURCE_LANG]                    # strict mode: one language

SERIES_NAME = {"en": "Stable Matching, Step by Step"}

# Pauses of the voice in seconds: after a sentence, a paragraph (a line break in a beat), a beat.
# These give about 130 to 150 words per minute. Do not change them unless check.py's pace line says WARN.
PACE = {"sentence": 0.8, "paragraph": 1.5, "beat": 1.5}

EPISODES = [
    # file name, class name in that file, title, one-line subtitle, output file name
    # notes.txt lines 9 to 100
    {"file": "ep01_propose_reject.py", "scene": "Ep01ProposeReject",
     "title": {"en": "Propose and Reject"},
     "sub": {"en": "three jobs, three candidates, three days"},
     "slug": {"en": "propose-and-reject"}},
    # lines 101 to 132
    {"file": "ep02_residency_match.py", "scene": "Ep02ResidencyMatch",
     "title": {"en": "The Residency Match"},
     "sub": {"en": "why hospitals needed this algorithm"},
     "slug": {"en": "the-residency-match"}},
    # lines 143 to 198
    {"file": "ep03_rogue_couples.py", "scene": "Ep03RogueCouples",
     "title": {"en": "Rogue Couples"},
     "sub": {"en": "what makes a matching stable"},
     "slug": {"en": "rogue-couples"}},
    # lines 199 to 242
    {"file": "ep04_roommates.py", "scene": "Ep04Roommates",
     "title": {"en": "The Roommates Problem"},
     "sub": {"en": "a stable matching does not have to exist"},
     "slug": {"en": "the-roommates-problem"}},
    # lines 133 to 142 and 243 to 266
    {"file": "ep05_improvement_lemma.py", "scene": "Ep05ImprovementLemma",
     "title": {"en": "Offers Only Get Better"},
     "sub": {"en": "the algorithm halts, and the improvement lemma"},
     "slug": {"en": "offers-only-get-better"}},
    # lines 267 to 304
    {"file": "ep06_well_ordering.py", "scene": "Ep06WellOrdering",
     "title": {"en": "The First Counterexample"},
     "sub": {"en": "the well-ordering principle behind induction"},
     "slug": {"en": "the-first-counterexample"}},
    # lines 305 to 328
    {"file": "ep07_always_stable.py", "scene": "Ep07AlwaysStable",
     "title": {"en": "Always a Stable Matching"},
     "sub": {"en": "everyone is matched and no couple is rogue"},
     "slug": {"en": "always-a-stable-matching"}},
    # lines 329 to 415
    {"file": "ep08_optimal_partners.py", "scene": "Ep08OptimalPartners",
     "title": {"en": "The Best Partner You Can Keep"},
     "sub": {"en": "optimal and pessimal partners"},
     "slug": {"en": "the-best-partner-you-can-keep"}},
    # lines 416 to 437
    {"file": "ep09_job_optimal.py", "scene": "Ep09JobOptimal",
     "title": {"en": "The Proposers Win"},
     "sub": {"en": "the output is optimal for the jobs"},
     "slug": {"en": "the-proposers-win"}},
    # lines 438 to 474
    {"file": "ep10_candidate_pessimal.py", "scene": "Ep10CandidatePessimal",
     "title": {"en": "And the Candidates Lose"},
     "sub": {"en": "optimal for one side is pessimal for the other"},
     "slug": {"en": "and-the-candidates-lose"}},
]
