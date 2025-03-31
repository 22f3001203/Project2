from bs4 import BeautifulSoup
import json
import os

html_folder = "downloaded_pages"
output_json = "data/questions_answers.json"
qa_list = []

for filename in os.listdir(html_folder):
    if filename.endswith(".html"):  
        file_path = os.path.join(html_folder, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        # Find all question blocks
        for question_block in soup.find_all("div", class_="mb-3"):
            # Extract question text inside <p> tag
            question_tag = question_block.find("p")
            question_text = question_tag.get_text(strip=True) if question_tag else "Question not found"

            # Extract answer from the <div class="valid-feedback">
            answer_tag = question_block.find("div", class_="valid-feedback")
            answer_text = answer_tag.get_text(strip=True) if answer_tag else "Answer not found"

            # Store in list
            qa_list.append({"question": question_text, "answer": answer_text})

os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(qa_list, json_file, indent=4, ensure_ascii=False)

print(f"✅ Processed {len(qa_list)} questions and saved to {output_json}")
