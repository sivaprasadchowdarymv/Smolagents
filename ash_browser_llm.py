import time
import helium
from helium import *
from selenium import webdriver
import ollama

# ==============================
# Browser Control (Deterministic)
# ==============================
def run_browser():
    print("🚀 Starting browser...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = helium.start_chrome(headless=False, options=options)

    # Step 1: Search images
    go_to("https://duckduckgo.com")
    write("Itachi_Uchiha images")
    press(ENTER)
    time.sleep(2)

    try:
        click("Images")
    except:
        pass

    time.sleep(2)

    # Step 2: Wikipedia
    go_to("https://en.wikipedia.org/wiki/Itachi_Uchiha")
    time.sleep(3)

    print("✅ Browser steps done")


# ==============================
# LLM Reasoning (Ollama)
# ==============================
def run_llm():
    print("🤖 Generating answer using Ollama...")

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": "Describe Itachi_Uchiha's journey briefly."
            }
        ]
    )

    print("\n🧠 Final Answer:\n")
    print(response['message']['content'])


# ==============================
# MAIN
# ==============================
def main():
    run_browser()
    run_llm()


if __name__ == "__main__":
    main()