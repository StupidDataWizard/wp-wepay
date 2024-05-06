import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.style.use('bmh')
    plt.figure(figsize=(8,5))
    #plt.title('Salden der WePay Nutzer')
    
    #plt.xticks(rotation=45)
    colors = ['green' if i > 0 else 'red' for i in y]
    plt.bar(x,y, color=colors)

    plt.axhline(y=0,linewidth=1, color='black', linestyle="dashed")
    
    plt.xlabel('Nutzer')
    plt.ylabel('Salden in €')
    plt.tight_layout()
    graph = get_graph()
    return graph