# function analyzeRepo(repoName, language = "unknown") {
#   const stats = {
#     name: repoName,
#     language: language,
#     score: 0
#   }

#   if (language === "Python") {
#     stats.score = 10
#   } else if (language === "JavaScript") {
#     stats.score = 8
#   }

#   return `${stats.name} (${stats.language}): score ${stats.score}`
# }

def analyzeRepo(repoName, language = "unknown"):
    stats = {
        "name": repoName,
        "language": language,
        "score": 0
    }
    if (language == "Python"):
        stats["score"] = 10
    elif (language == "JavaScript"):
        stats["score"] = 8
    
    return f"{stats['name']} ({stats['language']}): score {stats['score']}"

print(analyzeRepo("langchain", "Python"))
print(analyzeRepo("react", "JavaScript"))
print(analyzeRepo("vue"))
