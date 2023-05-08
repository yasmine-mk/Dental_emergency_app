import streamlit as st
import markdown
import pickle as pkl


def rapport_creator(rapport, pred, remarks):
    """Create rapport"""
    
    # Chooses correct prefix for name
    mr =  "Mr," if rapport["Sexe"] == "homme" else "Mme,"
    
    # First header
    result = '# Rapport dentaire de ' + mr + rapport['Nom'] + " " + rapport['Prenom']
    
    # Details about patient
    for key, value in rapport.items():
        result += f"\n### {key}: {value}"
    
    # Final results and remarks
    result += f"\n# Resultat final : {pred}"
    if remarks != "":
        result += f"\n## Remarques de docteur : {remarks}"
    result += f"\n#### Explication de {pred}:\n{explanations[pred]}"
    return result

def markdown_to_html(md_string):
    """Converts a Markdown string to HTML"""
    html = markdown.markdown(md_string)
    return html

def features_from_form(result, label_encoders):
    features = []
    for key, value in result.items():
        if key != "Prenom" and key != "Nom":
            if key == 'Age Patient':
                features.append([value])
                continue   
            print(key, value) 
            features.append(label_encoders[key].transform([value]))
    return features


explanations = {"pulpite reversible": """Une pulpite réversible est une inflammation de la pulpe dentaire qui peut être guérie sans
intervention dentaire majeure. Elle peut être causée par une carie dentaire profonde, une blessure
ou une infection.
La conduite à tenir face à une pulpite réversible consiste à consulter un dentiste dès que possible
pour un examen et un traitement approprié. Le dentiste peut recommander des analgésiques pour
soulager la douleur et peut prescrire des antibiotiques si une infection est présente. Dans certains
cas, le dentiste peut effectuer une obturation dentaire pour protéger la pulpe dentaire et éviter toute
aggravation de la condition.
Il est important de noter que si la pulpite n'est pas traitée rapidement, elle peut évoluer vers une
pulpite irréversible qui nécessite une intervention dentaire plus complexe comme une endodontie
(traitement de canal) ou une extraction de la dent affectée. Il est donc recommandé de prendre des
mesures préventives pour éviter les caries dentaires et de consulter un dentiste régulièrement pour
maintenir une bonne santé bucco-dentaire.""",
"pulpite irreversible symptomatique": """
Une pulpite irréversible symptomatique est une inflammation de la pulpe dentaire qui ne peut pas
être guérie sans intervention dentaire majeure. Les symptômes comprennent une douleur intense et
persistante, une sensibilité au chaud ou au froid, une sensibilité à la pression et une enflure.
La conduite à tenir face à une pulpite irréversible symptomatique est de consulter rapidement un
dentiste pour un examen et un traitement approprié. Le dentiste peut recommander un traitement
de canal pour éliminer l'infection de la pulpe dentaire, ou une extraction de la dent affectée si le
traitement de canal n'est pas possible. Dans certains cas, le dentiste peut prescrire des analgésiques
pour soulager la douleur et des antibiotiques pour prévenir la propagation de l'infection.
Il est important de noter que si la pulpite irréversible symptomatique n'est pas traitée rapidement,
elle peut entraîner des complications plus graves telles qu'une infection généralisée, une cellulite ou
une septicémie. Il est donc essentiel de consulter un dentiste dès que possible pour un traitement approprié. Il est également recommandé de prendre des mesures préventives pour éviter les caries
dentaires et de consulter un dentiste régulièrement pour maintenir une bonne santé bucco-dentaire. 
""", 
"pulpite irreversible asymptomatique": """
Une pulpite irréversible asymptomatique est une inflammation de la pulpe dentaire qui ne présente
pas de symptômes perceptibles, tels que douleur ou sensibilité. Cependant, cette condition peut être
détectée par des examens dentaires tels que des radiographies ou des tests de vitalité pulpaire.
La conduite à tenir face à une pulpite irréversible asymptomatique consiste en une surveillance
régulière de la dent affectée par un dentiste pour déterminer si des symptômes se développent. Si
des symptômes se développent, un traitement de canal ou une extraction de la dent peut être
nécessaire. Dans certains cas, le dentiste peut recommander un traitement préventif, tel qu'une
obturation dentaire, pour éviter que la pulpite ne se développe en une condition symptomatique
nécessitant un traitement plus agressif.
Il est important de noter que la pulpite irréversible asymptomatique peut se développer en une
condition symptomatique sans avertissement, il est donc essentiel de consulter régulièrement un
dentiste pour détecter et traiter toute condition dentaire le plus tôt possible. Les mesures
préventives telles que le brossage régulier des dents, l'utilisation de fil dentaire et des visites
régulières chez le dentiste peuvent aider à maintenir une bonne santé bucco-dentaire et prévenir les
pulpite irréversible asymptomatiques""", 
"parodontite apicale aiguë": """La parodontite apicale aiguë est une infection bactérienne grave de la racine dentaire et de l'os de
soutien de la dent, qui peut causer des douleurs, un gonflement et une sensibilité à la pression.
La conduite à tenir face à une parodontite apicale aiguë consiste à consulter rapidement un dentiste
ou un endodontiste (un spécialiste des traitements de canal) pour un traitement. Le traitement
consiste généralement en un traitement de canal pour éliminer l'infection de la racine dentaire, ou
une extraction de la dent affectée si le traitement de canal n'est pas possible.
Dans certains cas, le dentiste ou l'endodontiste peut prescrire des antibiotiques pour réduire
l'infection et soulager la douleur et le gonflement. Cependant, l'utilisation d'antibiotiques ne suffit
pas à elle seule pour traiter la parodontite apicale aiguë et un traitement dentaire est toujours
nécessaire. 
Il est important de noter que si la parodontite apicale aiguë n'est pas traitée rapidement, elle peut
entraîner des complications plus graves telles qu'une infection généralisée, une cellulite ou une
septicémie. Il est donc essentiel de consulter un dentiste ou un endodontiste dès que possible pour
un traitement approprié. Il est également recommandé de prendre des mesures préventives pour
éviter les caries dentaires et la gingivite en maintenant une bonne hygiène bucco-dentaire et en ayant
des visites régulières chez le dentiste.""",
"abcès apicale aigu": """
Un abcès apical aigu est une infection bactérienne grave qui se développe au bout de la racine
dentaire et qui peut provoquer une douleur intense, un gonflement et une fièvre.
La conduite à tenir face à un abcès apical aigu consiste à consulter immédiatement un dentiste ou un
endodontiste pour un traitement. Le traitement peut inclure un traitement de canal pour éliminer
l'infection de la racine dentaire, une incision et un drainage pour évacuer l'abcès, ou une extraction
de la dent affectée si le traitement de canal n'est pas possible.
Dans certains cas, le dentiste ou l'endodontiste peut prescrire des antibiotiques pour réduire
l'infection et soulager les symptômes, mais cela ne suffit pas à traiter complètement l'abcès.
Il est important de noter que si l'abcès apical aigu n'est pas traité rapidement, il peut se propager à
d'autres parties du corps, entraîner des complications graves et mettre la vie en danger. Il est donc
essentiel de consulter un dentiste ou un endodontiste dès que possible pour un traitement
approprié.
Il est également recommandé de prendre des mesures préventives pour éviter les caries dentaires et
la gingivite en maintenant une bonne hygiène bucco-dentaire, en évitant de manger des aliments
sucrés et en ayant des visites régulières chez le dentiste.""", 
"cellulite": """
La cellulite dentaire est une infection bactérienne grave qui se propage au-delà des tissus mous de la
bouche et qui peut provoquer une douleur intense, un gonflement et une fièvre. 
La conduite à tenir face à une cellulite dentaire consiste à consulter immédiatement un dentiste ou
un médecin. Le traitement peut inclure des antibiotiques pour réduire l'infection et soulager les
symptômes, une incision pour drainer l'infection, ou une combinaison des deux.
Dans certains cas, le dentiste ou le médecin peut recommander une hospitalisation pour un
traitement plus agressif. Si l'infection est très avancée ou si elle met la vie en danger, une intervention
chirurgicale peut être nécessaire pour enlever le tissu infecté.
Il est important de noter que si la cellulite dentaire n'est pas traitée rapidement, elle peut se
propager à d'autres parties du corps, entraîner des complications graves et mettre la vie en danger. Il
est donc essentiel de consulter un dentiste ou un médecin dès que possible pour un traitement
approprié.
Il est également recommandé de prendre des mesures préventives pour éviter les caries dentaires et
la gingivite en maintenant une bonne hygiène bucco-dentaire, en évitant de manger des aliments
sucrés et en ayant des visites régulières chez le dentiste""", "abcès apical chronique": """Un abcès apical chronique est une infection bactérienne de la racine dentaire qui se développe
lentement et qui peut causer peu ou pas de douleur.
La conduite à tenir face à un abcès apical chronique dépend de la gravité de l'infection et de
l'étendue des dommages causés aux tissus dentaires et osseux. Dans certains cas, le dentiste ou
l'endodontiste peut recommander un traitement de canal pour éliminer l'infection de la racine
dentaire.
Cependant, si le traitement de canal n'est pas possible ou si l'infection est trop avancée, l'extraction
de la dent affectée peut être nécessaire. Dans certains cas, une combinaison de traitement de canal
et d'extraction dentaire peut être recommandée.
Si l'infection est très avancée et qu'il y a un risque de propagation de l'infection, des antibiotiques
peuvent être prescrits pour aider à réduire l'infection et à prévenir les complications. 
Il est important de noter que si l'abcès apical chronique n'est pas traité, l'infection peut se propager à
d'autres parties du corps et entraîner des complications graves. Il est donc essentiel de consulter un
dentiste ou un endodontiste dès que possible pour un traitement approprié.
Il est également recommandé de prendre des mesures préventives pour éviter les caries dentaires et
la gingivite en maintenant une bonne hygiène bucco-dentaire, en évitant de manger des aliments
sucrés et en ayant des visites régulières chez le dentiste""", "septite": """La septite dentaire est une inflammation locale du septum dentaire, qui est situé entre deux dents.
Cette inflammation peut être causée par plusieurs facteurs.
La conduite à tenir face à une septite dentaire consiste à consulter un dentiste qui procédera au
nettoyage du septum pour éliminer l'inflammation. Il est également important de maintenir une
bonne hygiène bucco-dentaire, comme un brossage quotidien après chaque repas et l'utilisation d'un
bain de bouche pour une période de 10 jours maximum.
Il est recommandé d'éliminer les causes possibles de la septite dentaire pour éviter les récidives de
l'inflammation. Si la septite dentaire n'est pas traitée, elle peut causer des complications plus graves,
comme la formation d'un abcès ou une perte osseuse autour des dents. Il est donc important de
consulter un dentiste dès que possible pour un traitement approprié""",
"gingivite": """
La gingivite dentaire est une inflammation de la gencive, souvent causée par une accumulation de
plaque dentaire sur les dents et le long de la ligne des gencives. Les symptômes de la gingivite
incluent des gencives rouges, gonflées et qui saignent facilement lors du brossage des dents ou de
l'utilisation du fil dentaire.
La conduite à tenir face à une gingivite dentaire est de maintenir une bonne hygiène bucco-dentaire,
notamment en brossant les dents deux fois par jour avec un dentifrice fluoré et en utilisant du fil
dentaire pour éliminer les résidus alimentaires et la plaque dentaire. Une visite régulière chez le
dentiste pour un nettoyage dentaire professionnel peut également aider à prévenir la gingivite. 
Si la gingivite est déjà présente, le traitement peut inclure un nettoyage professionnel des dents pour
éliminer la plaque et le tartre, ainsi que l'utilisation de bains de bouche antiseptiques pour aider à
réduire l'inflammation. Dans les cas plus graves, un traitement parodontal peut être nécessaire pour
traiter l'infection et restaurer la santé des gencives.
Il est important de traiter la gingivite rapidement, car si elle n'est pas traitée, elle peut évoluer en une
maladie des gencives plus grave, appelée parodontite, qui peut endommager les gencives, les os de la
mâchoire et les dents""", "traumatisme dentaire": """Le traumatisme dentaire est une blessure qui affecte les dents, la bouche ou les mâchoires. Les
traumatismes dentaires peuvent être causés par diverses raisons, telles qu'un accident, une chute ou
un coup violent à la bouche. Les types courants de traumatismes dentaires incluent les fractures, les
luxations et les avulsions dentaires (quand une dent est complètement expulsée de son alvéole).
La conduite à tenir face à un traumatisme dentaire dépendra du type et de la gravité de la blessure. Il
est important de consulter un dentiste dès que possible, même si la douleur ou les symptômes ne
sont pas graves, car certains traumatismes peuvent ne pas présenter de symptômes immédiats, mais
peuvent causer des complications plus tard.
En attendant la consultation avec le dentiste, il est recommandé d'appliquer de la glace sur la zone
touchée pour réduire l'enflure et la douleur, ainsi que de prendre des analgésiques si nécessaire. Si
une dent est expulsée, il est important de la manipuler avec précaution, de la nettoyer doucement
avec de l'eau tiède et de la replacer dans son alvéole aussi rapidement que possible.
Le traitement du traumatisme dentaire dépendra du type et de la gravité de la blessure, et peut
inclure des mesures comme la restauration de la dent endommagée, la réimplantation de la dent
expulsée ou la pose d'une prothèse dentaire pour remplacer une dent manquante. Dans les cas plus
graves, une intervention chirurgicale peut être nécessaire.
Il est important de suivre les instructions du dentiste pour le traitement et le suivi, ainsi que de
maintenir une bonne hygiène bucco-dentaire pour favoriser la guérison et prévenir les complications""", "extrusion dentaire": """L'extrusion dentaire est une blessure dentaire qui survient lorsque la dent est partiellement expulsée
de son alvéole. Elle est généralement causée par un traumatisme direct ou indirect à la dent. Les
symptômes peuvent inclure une douleur intense, une mobilité de la dent et une inflammation des
tissus environnants.
La conduite à tenir face à une extrusion dentaire est de consulter un dentiste immédiatement. Il est
important de ne pas essayer de replacer la dent soi-même, car cela peut causer des dommages
supplémentaires aux tissus environnants. Le dentiste examinera la dent et les tissus environnants
pour déterminer la gravité de la blessure.
Dans certains cas, la dent peut être remise en place dans l'alvéole avec précaution. Dans d'autres cas,
une intervention chirurgicale peut être nécessaire pour réparer les dommages aux tissus
environnants ou pour extraire la dent endommagée. Des radiographies peuvent également être
nécessaires pour évaluer l'étendue des dommages aux racines de la dent.
Une fois que la dent a été replacée ou retirée, un suivi régulier avec le dentiste est important pour
surveiller la guérison et prévenir les complications. Des médicaments pour soulager la douleur et
réduire l'inflammation peuvent être prescrits, et des conseils pour l'hygiène bucco-dentaire peuvent
également être donnés pour favoriser la guérison et prévenir les infections""", "péricoronarite": """La péricoronarite est une inflammation de la gencive autour d'une dent partiellement éruptive, le
plus souvent une dent de sagesse. Cela se produit lorsque la dent ne peut pas émerger correctement
de la gencive, ce qui crée un espace où les bactéries peuvent s'accumuler et causer une infection. Les
symptômes incluent une douleur, une enflure, une rougeur et une difficulté à ouvrir la bouche.
La conduite à tenir face à une péricoronarite est de consulter un dentiste dès que possible. Le
dentiste examinera la zone affectée et peut prescrire des antibiotiques pour traiter l'infection si elle
est sévère. Il peut également nettoyer la zone pour éliminer les débris et les bactéries accumulés.
En plus du traitement médical, une bonne hygiène bucco-dentaire est importante pour prévenir les
péricoronarites. Il est recommandé de se brosser les dents deux fois par jour, de passer du fil dentaire
quotidiennement et d'utiliser un bain de bouche. Si la péricoronarite est causée par une dent de
sagesse partiellement éruptive, le dentiste peut recommander son extraction pour prévenir les futurs
épisodes d'inflammation"""}