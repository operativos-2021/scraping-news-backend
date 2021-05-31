from clasificator.StringTagger.StringClf import Classifier
from clasificator.StringTagger.getPage import getTextPage
import json
import os 

actual_path = os.path.dirname(os.path.abspath(__file__))
scrape_result_path = actual_path.replace('\clasificator','/scraping/scrape_result.json')

clf = Classifier()
training_data = { # Datos para entrenar al clasificador
	"Ciencia":[
		'https://es.yourdictionary.com/frases/ciencia'
	],
	"Deportes":[
		"https://es.yourdictionary.com/frases/deporte"
	],
	"Tecnologia":[
		'https://es.yourdictionary.com/frases/tecnología'
	],
	"Medicina":[
		"https://es.yourdictionary.com/frases/salud",
		"https://es.yourdictionary.com/frases/medicina"

	],
	"Política":[
		"https://es.yourdictionary.com/frases/política",
	],
	"Economía":[
		"https://es.yourdictionary.com/frases/economía",
	]
}

def initClassifier():
	print(clf)
	 # Instancia del clasificador
	for category,urls in training_data.items(): # Entrenamos al clasificador con el contenido de cada pagina
		for url in urls:
			clf.train(getTextPage(url),category) # El metodo "getTextPage", recive como argumento una url para extraer su texto

def classifyNews():
	f = open(scrape_result_path, "r")
	news = json.loads(f.read())
	for new in news:
		for notice in news[new]:
			clas = classifyText(notice["headline"])
			notice["class"] = clas
	return news

def classifyText(text):
	# Iniciamos el proceso de clasificación con el metodo "String"
	# Solo le pasamos como argumento el texto que deseamos etiquetar (clasificar)
	clas = clf.String(text)
	return clas
