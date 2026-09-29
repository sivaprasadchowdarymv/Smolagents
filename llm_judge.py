import time
import json
import ollama
import helium
from helium import *
from selenium import webdriver

from smolagents import CodeAgent, DuckDuckGoSearchTool
from smolagents.cli import load_model

# ==============================
# 1. WEB AGENT (Browser + LLM)
# ==============================
def run_web_agent():
    print("🌐 Launching browser...")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = helium.start_chrome(headless=False, options=options)

    model = load_model("LiteLLMModel", "ollama/llama3")

    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        additional_authorized_imports=["helium", "time"],
        max_steps=3,
        verbosity_level=1,
    )

    agent.python_executor("from helium import *")

    TASK = """
    Execute these steps ONLY ONCE:

    1. go_to("https://duckduckgo.com")
    2. write("Harry Potter images")
    3. press(ENTER)
    4. click("Images")

    STOP after this.

    Then return:

    final_answer("Harry Potter has messy black hair, round glasses, and a lightning-shaped scar on his forehead.")
    """

    result = agent.run(TASK)

    return str(result)


# ==============================
# 2. RULE-BASED VALIDATION
# ==============================
def rule_check(answer):
    keywords = ["glasses", "scar", "hair"]

    matched = sum(k in answer.lower() for k in keywords)

    return {
        "rule_score": matched / len(keywords),
        "matched_keywords": matched
    }


# ==============================
# 3. LLM JUDGE (Ollama)
# ==============================
def judge_answer(answer):
    prompt = f"""
    You are an expert evaluator.

    Evaluate this answer:

    {answer}

    Ground truth:
    Harry Potter has messy black hair, round glasses, and a lightning-shaped scar.

    Evaluate:
    - correctness (yes/no)
    - completeness (0–10)
    - hallucination (yes/no)

    Return ONLY JSON:
    {{
        "verdict": "yes/no",
        "score": number,
        "hallucination": "yes/no",
        "reason": "short explanation"
    }}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response["message"]["content"])
    except:
        return {"error": "invalid_json", "raw": response["message"]["content"]}


# ==============================
# 4. FINAL SCORING
# ==============================
def combine_scores(rule, judge):
    if "error" in judge:
        return {"final_score": 0, "status": "FAIL"}

    final_score = 0.4 * rule["rule_score"] + 0.6 * (judge["score"] / 10)

    return {
        "final_score": round(final_score, 2),
        "status": "PASS" if final_score > 0.7 else "FAIL"
    }


# ==============================
# 5. LOGGER
# ==============================
def log_result(data):
    with open("agent_results.json", "a") as f:
        f.write(json.dumps(data) + "\n")


# ==============================
# 6. MAIN PIPELINE
# ==============================
def main():
    print("🚀 Starting full pipeline...\n")

    # Step 1: Run web agent
    answer = run_web_agent()

    print("\n🧠 Agent Output:\n", answer)

    # Step 2: Rule validation
    print("\n📏 Running rule-based validation...")
    rule = rule_check(answer)
    print(rule)

    # Step 3: LLM judge
    print("\n⚖️ Running LLM judge...")
    judge = judge_answer(answer)
    print(judge)

    # Step 4: Final scoring
    print("\n🏁 Final evaluation...")
    final = combine_scores(rule, judge)
    print(final)

    # Step 5: Logging
    log_result({
        "answer": answer,
        "rule": rule,
        "judge": judge,
        "final": final,
        "timestamp": time.time()
    })

    print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    main()