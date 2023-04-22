import os
import openai
openai.organization = "org-XOIaTvOT7o7SoUAZ0MxFItSW"
openai.api_key = os.getenv("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")
openai.api_key = "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"
openai.Model.list()

# Define helper function
def generate_text(prompt, model="text-davinci-003", max_tokens=100):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Define research topic and sections
topic = "Predictive Analytics for Hedge Funds using Big Data and AI"
sections = ["Introduction", "Literature Review", "Methodology", "Results", "Discussion", "Conclusion"]

# Generate paper content
paper_content = f"Research Proposal: {topic}\n\n"
for section in sections:
    content = generate_text(f"Write a detailed section about {section} for a research paper on the topic: {topic}", max_tokens=500)
    paper_content += f"{section}\n{content}\n\n"

# Save the research paper to a file
with open("research_paper.txt", "w") as f:
    f.write(paper_content)

print("Research paper saved as 'research_paper.txt'")
