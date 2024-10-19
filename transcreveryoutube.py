import tkinter as tk
from tkinter import messagebox, scrolledtext
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from collections import Counter
import re

# Extrai a transcrição do vídeo
def obter_transcricao(video_id):
    try:
        transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        texto = " ".join([entry['text'] for entry in transcricao])
        return texto
    except Exception as e:
        return f"Erro ao obter a transcrição: {e}"

# Resume o texto
def resumir_texto(texto, num_sentencas=5):
    parser = PlaintextParser.from_string(texto, Tokenizer("portuguese"))
    summarizer = LsaSummarizer()
    resumo = summarizer(parser.document, num_sentencas)
    return " ".join(str(frase) for frase in resumo)

# Extrai os tópicos principais
def extrair_topicos(texto, num_topicos=5):
    palavras = re.findall(r'\b\w+\b', texto.lower())
    palavras_comuns = Counter(palavras).most_common(num_topicos)
    return [palavra for palavra, _ in palavras_comuns]

# Extrai o ID do vídeo da URL
def extrair_id_video(url):
    padrao = r"(?<=v=)[\w-]+|(?<=be/)[\w-]+"
    match = re.search(padrao, url)
    return match.group(0) if match else None

# Analisa o vídeo
def analisar_video():
    url = url_entry.get()
    video_id = extrair_id_video(url)
    
    if not video_id:
        messagebox.showerror("Erro", "URL do vídeo inválida.")
        return
    
    transcricao = obter_transcricao(video_id)
    if "Erro" in transcricao:
        messagebox.showerror("Erro", transcricao)
        return
    
    resumo = resumir_texto(transcricao)
    topicos = extrair_topicos(transcricao)
    
    # Exibe o resumo e os tópicos
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Resumo:\n{resumo}\n\nTópicos principais: {', '.join(topicos)}")

# Interface gráfica
janela = tk.Tk()
janela.title("Analisador de Vídeos do YouTube")
janela.geometry("600x400")

# Rótulo e entrada para a URL
url_label = tk.Label(janela, text="Digite a URL do vídeo do YouTube:")
url_label.pack(pady=10)
url_entry = tk.Entry(janela, width=50)
url_entry.pack(pady=5)

# Botão para analisar o vídeo
analyze_button = tk.Button(janela, text="Analisar Vídeo", command=analisar_video)
analyze_button.pack(pady=10)

# Área de texto para exibir o resultado
result_text = scrolledtext.ScrolledText(janela, height=15, wrap=tk.WORD)
result_text.pack(pady=10)

# Iniciar a interface
janela.mainloop()
