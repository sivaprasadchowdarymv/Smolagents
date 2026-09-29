# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:20:39 2026

@author: mvspc
"""

import time
import helium
from helium import *
from selenium import webdriver
import ollama

# ==============================
# LLM (Ollama)
# ==============================
def llm(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


# ==============================
# TAO AGENT LOOP
# ==============================
def tao_agent():
    print("🚀 Starting browser...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = helium.start_chrome(headless=False, options=options)

    # ==========================
    # STEP 1
    # ==========================
    thought = "I should open DuckDuckGo to search for Harry Potter images"
    print("\n🧠 Thought:", thought)

    action = 'go_to("https://duckduckgo.com")'
    print("⚙️ Action:", action)
    go_to("https://duckduckgo.com")

    observation = "DuckDuckGo homepage opened"
    print("👁️ Observation:", observation)

    # ==========================
    # STEP 2
    # ==========================
    thought = "Now I should search for Harry Potter images"
    print("\n🧠 Thought:", thought)

    action = 'write("Harry Potter images") + press(ENTER)'
    print("⚙️ Action:", action)
    write("Harry Potter images")
    press(ENTER)
    time.sleep(2)

    observation = "Search results displayed"
    print("👁️ Observation:", observation)

    # ==========================
    # STEP 3
    # ==========================
    thought = "I should view image results"
    print("\n🧠 Thought:", thought)

    action = 'click("Images")'
    print("⚙️ Action:", action)
    try:
        click("Images")
    except:
        pass

    time.sleep(2)

    observation = "Image results visible"
    print("👁️ Observation:", observation)

    # ==========================
    # STEP 4
    # ==========================
    thought = "Now I will open Wikipedia for detailed info"
    print("\n🧠 Thought:", thought)

    action = 'go_to("https://en.wikipedia.org/wiki/Harry_Potter")'
    print("⚙️ Action:", action)
    go_to("https://en.wikipedia.org/wiki/Harry_Potter")

    time.sleep(3)

    observation = "Wikipedia page loaded"
    print("👁️ Observation:", observation)

    # ==========================
    # FINAL REASONING (LLM)
    # ==========================
    print("\n🤖 Generating final answer...")

    prompt = """
    Based on general knowledge, describe Harry Potter's appearance.
    """

    answer = llm(prompt)

    print("\n✅ FINAL ANSWER:\n")
    print(answer)


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    tao_agent()