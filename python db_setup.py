tasks = [
 ("Signup kore income korun", 5, "manual"),
 ("Ad dekhun", 0.30, "auto"),
 ("Join Channel", 1, "manual"),
 ("TikTok video + follow", 0.5, "manual"),
 ("YouTube video + subscribe", 0.8, "manual"),
 ("Facebook like + comment + share", 1, "manual")
]

for t in tasks:
    c.execute("INSERT INTO tasks(title,reward,type) VALUES (?,?,?)", t)
