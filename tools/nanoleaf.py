from flask import Flask, render_template, request
from nanoleafapi import discovery, Nanoleaf

app = Flask(__name__, template_folder='./tools')

# Fonction pour obtenir l'adresse IP du Nanoleaf
def get_nanoleaf_ip():
    nanoleaf_dict = discovery.discover_devices(timeout=30)
    if nanoleaf_dict:
        return list(nanoleaf_dict.values())[0]
    else:
        return None
    
if __name__ == '__main__':
    app.run(debug=True, port=4880)

# Route pour allumer le Nanoleaf
@app.route('/turn_on', methods=['POST'])
def turn_on_nanoleaf():
    ip = get_nanoleaf_ip()
    if ip:
        nl = Nanoleaf(ip)
        nl.turn_on()
        return 'Nanoleaf allumé.'
    else:
        return 'Nanoleaf non trouvé.'


# Route pour le contrôle du Nanoleaf
@app.route('/control', methods=['POST'])
def control_nanoleaf():
    ip = get_nanoleaf_ip()
    if ip:
        nl = Nanoleaf(ip)
        action = request.form['action']
        if action == 'toggle':
            nl.toggle_power()
        elif action == 'set_color':
            color = tuple(map(int, request.form['color'].split(',')))
            nl.set_color(color)
        return 'Commande envoyée avec succès.'
    else:
        return 'Nanoleaf non trouvé.'

if __name__ == '__main__':
    app.run(debug=True)
