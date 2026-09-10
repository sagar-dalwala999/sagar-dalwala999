"""Content for the fun account (sagar-dalwala999) — chemistry-lab / desert case-file theme."""

NAME = "Sagar Dalwala"
PERSONA = "Jesse Pinkman"           # the display name he set on the fun account
HANDLE = "sagar-dalwala999"         # owner of the profile repo this README lives in
STATS_USER = "sagar-dalwala999"     # whose stats / snake are shown
GITHUB = f"https://github.com/{HANDLE}"
MAIN_ACCOUNT = "https://github.com/Sagar-Dalwala"
EMAIL = "sagardalwala.vision@gmail.com"
LINKEDIN = "https://linkedin.com/in/sagar-dalwala"
LOCATION = "India"

TAGLINE = "the fun lab of Sagar Dalwala — experimental builds only"

# the hero spells SAGAR with real elements
ELEMENTS = [("S", 16, "Sulfur", "32.06"), ("Ag", 47, "Silver", "107.87"), ("Ar", 18, "Argon", "39.95")]

TYPING_LINES = [
    "the fun lab of Sagar Dalwala",
    "experimental builds only",
    "99.1% pure TypeScript",
    "yeah, science!",
]

# case-file lines (label, value)
ABOUT = [
    ("SUBJECT", "Sagar Dalwala, a.k.a. Jesse Pinkman"),
    ("STATUS", "cooking side projects, breaking builds, fixing them again"),
    ("KNOWN FOR", "MERN × AI · hackathons · forks of anything shiny"),
    ("MAIN LAB", "github.com/Sagar-Dalwala  (the serious one)"),
    ("LOCATION", "India · UTC+5:30"),
]

# (symbol, atomic-number, repo-name, url, one-liner, tags, is_fork)
PROJECTS = [
    ("Se", 34, "autonomous-seo-platform", f"{GITHUB}/autonomous-seo-platform",
     "Autonomous SEO optimisation platform — research, client deliverables, and a proof-of-concept crawler + analyser.",
     ["TypeScript", "crawler", "SEO"], False),
    ("Re", 75, "ReplitAppNative", f"{GITHUB}/ReplitAppNative",
     "Native app experiment built on Replit — the kind of thing that only exists on the fun account.",  # TODO(sagar): fix this one-liner
     ["React Native", "experiment"], False),
    ("As", 33, "android-sms-gateway", f"{GITHUB}/android-sms-gateway",
     "SMS gateway for Android — send and receive texts through an API, on-device or via a cloud server.",
     ["Kotlin", "Android", "API"], True),
    ("O", 8, "OpenVoice", f"{GITHUB}/OpenVoice",
     "Instant voice cloning by MIT and MyShell — audio foundation model, poked at for the AI video pipeline.",
     ["Python", "voice", "AI"], True),
]

# lab results: (label, year, result, liquid colour key)
WINS = [
    ("NASA Space Apps Challenge", "2024", "Best Use of Science — winner", "blue"),
    ("IIIT-Allahabad Hackathon", "2023", "Face recognition system", "green"),
    ("Odoo × Mindbend Hackathon", "2025", "Top 50 of 2,500 teams", "amber"),
]

# reagents: (symbol, name, group, real_element)
STACK = [
    ("Re", "React", "frontend", True), ("Ne", "Next.js", "frontend", True), ("Ts", "TypeScript", "frontend", True),
    ("Ta", "Tailwind", "frontend", True), ("Rx", "Redux", "frontend", False),
    ("No", "Node.js", "backend", True), ("Es", "Express", "backend", True), ("Mo", "MongoDB", "backend", True),
    ("Pr", "Prisma", "backend", True), ("Fa", "FastAPI", "backend", False),
    ("La", "LangChain", "ai", True), ("Hf", "Hugging Face", "ai", True), ("O", "OpenAI", "ai", True), ("P", "Python", "ai", True),
    ("Db", "Docker", "infra", True), ("Ga", "GCP", "infra", True), ("Ge", "Git", "infra", True), ("Cl", "Cloudinary", "infra", True),
]

STATS_SAMPLE = {"repos": 23, "followers": 2, "contributions": 364, "hackathons": 3, "stars": 4, "prs": 9}
LANGS_SAMPLE = [("TypeScript", 41), ("Python", 23), ("Kotlin", 14), ("JavaScript", 12), ("Other", 10)]
