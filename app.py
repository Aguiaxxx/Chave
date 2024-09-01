import json
from playwright.sync_api import sync_playwright

# Função para gravar os eventos de clique
def log_click(click_data):
    with open("cliques.json", "a") as file:
        file.write(json.dumps(click_data) + "\n")

def main():
    with sync_playwright() as p:
        # Lançar o navegador
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Função de callback para capturar eventos de clique
        def handle_click(route):
            click_data = {
                "url": page.url,
                "timestamp": page.evaluate("Date.now()"),
                "x": route.event["x"],
                "y": route.event["y"],
                "button": route.event["button"],
            }
            log_click(click_data)

        # Adiciona o ouvinte de eventos para clicks na página
        page.on("click", handle_click)

        # Navegar para uma página
        page.goto("https://example.com")

        # Manter o navegador aberto para capturar os cliques
        page.wait_for_timeout(30000)  # Aguarda 30 segundos para capturar cliques
        browser.close()

if __name__ == "__main__":
    main()
