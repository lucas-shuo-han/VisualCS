"""The episode list: order, titles and output names, in every language.

Copy next to manim_kit.py as series.py. Episode numbers, title cards, "next
episode" lines, the series-end card and the video file names all come from
here, so reordering or retitling the series is a one-line change.
"""

SOURCE_LANG = "zh"          # the language the episode files are written in
LANGS = ["zh", "en"]        # languages to render (translation tables: i18n/epNN.py)

SERIES_NAME = {"zh": "CS182 · 深度学习", "en": "CS182 · Deep Learning"}

# Series-wide choices (all optional; the kit and tts.py read them):
# BURN_CAPTIONS = False     # clean frame; subtitles only in the .srt beside the video
# TEXT_FONT = "latex"       # labels and tick numbers in the typeface of the formulas (math-heavy series)
# TTS = {"engine": "edge", "rate": "-4%",                     # chosen by ear: scripts/audition.py
#        "voice": {"en": "en-US-AndrewNeural"}, "kokoro_voice": {"en": "am_michael"}}
# PACE = {"sentence": 0.75, "paragraph": 1.6, "beat": 1.8}    # pauses in seconds; defaults 0.4 / 1.0 / 0.8

EPISODES = [
    # file, scene class, then per language: title, subtitle, file-name slug
    {"file": "ep01_gradient_descent.py", "scene": "Ep01GradientDescent",
     "title": {"zh": "梯度下降", "en": "Gradient Descent"},
     "sub": {"zh": "损失曲面 · 学习率 · 收敛", "en": "Loss landscapes · learning rate · convergence"},
     "slug": {"zh": "梯度下降", "en": "gradient-descent"}},
    {"file": "ep02_backprop.py", "scene": "Ep02Backprop",
     "title": {"zh": "反向传播", "en": "Backpropagation"},
     "sub": {"zh": "链式法则，倒着跑", "en": "The chain rule, run backwards"},
     "slug": {"zh": "反向传播", "en": "backpropagation"}},
]
