import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from dados import ARQ_NOTICIAS, ARQ_COMPLETAS


def criar_driver():
    opts = Options()
    opts.add_argument("--headless=new")      # sem abrir janela
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def extrair_artigo(driver, url, espera=15):
    driver.get(url)
    try:
        WebDriverWait(driver, espera).until(
            lambda d: "news.google.com" not in d.current_url
        )
    except TimeoutException:
        return url, ""
    time.sleep(2)
    paragrafos = driver.find_elements(By.TAG_NAME, "p")
    texto = " ".join(p.text.strip() for p in paragrafos if len(p.text.strip()) > 60)
    return driver.current_url, texto


def main():
    df = pd.read_csv(ARQ_NOTICIAS)
    driver = criar_driver()
    urls_finais, textos = [], []
    try:
        for i, link in enumerate(df["link"], 1):
            print(f"[{i}/{len(df)}] {link[:70]}...")
            try:
                url_final, texto = extrair_artigo(driver, link)
            except WebDriverException as e:
                print("  erro:", type(e).__name__)
                url_final, texto = link, ""
            urls_finais.append(url_final)
            textos.append(texto)
            time.sleep(1)
    finally:
        driver.quit()

    df["url_final"] = urls_finais
    df["texto"] = textos
    df["tamanho_texto"] = df["texto"].str.len()
    df.to_csv(ARQ_COMPLETAS, index=False)
    ok = (df["tamanho_texto"] > 0).sum()
    print(f"Salvo em {ARQ_COMPLETAS}. Matérias com texto: {ok}/{len(df)}")


if __name__ == "__main__":
    main()