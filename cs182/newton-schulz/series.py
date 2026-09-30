"""The episode list: order, titles and output names, in every language.

Episode numbers, title cards, "next episode" lines, the series-end card and
the video file names all come from here.
"""

SOURCE_LANG = "zh"          # the episode files are written in Chinese
LANGS = ["zh", "en"]        # English comes from i18n/epNN.py

SERIES_NAME = {"zh": "CS182 · 第五次讨论课", "en": "CS182 · Discussion 5"}

EPISODES = [
    {"file": "ep01_newton_schulz.py", "scene": "Ep01NewtonSchulz",
     "title": {"zh": "Newton–Schulz 迭代：一个奇异值去哪儿", "en": "Newton–Schulz: Where Does a Singular Value Go?"},
     "sub": {"zh": "不动点 · 蛛网图 · √3 与 √5 · 交替的吸引区",
             "en": "Fixed points · cobwebs · √3 and √5 · alternating basins"},
     "slug": {"zh": "Newton-Schulz迭代-奇异值去哪儿", "en": "newton-schulz-where-does-a-singular-value-go"}},
]
