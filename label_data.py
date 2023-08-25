import tkinter as tk
from tkinter import filedialog
import json
import os

class DataLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Labeling App")

        self.root_path = None
        self.json_data = None
        self.current_case_id = None
        self.labeled_data = []

        self.load_button = tk.Button(root, text="Load JSON", command=self.load_json)
        self.load_button.pack(pady=10)

        self.case_label = tk.Label(root, text="Case:")
        self.case_label.pack()
        self.case_text = tk.Text(root, height=10, width=50)
        self.case_text.pack()

        self.question_label = tk.Label(root, text="Question:")
        self.question_label.pack()
        self.question_text = tk.Text(root, height=10, width=50)
        self.question_text.pack()

        self.answer_label = tk.Label(root, text="Answer:")
        self.answer_label.pack()
        self.answer_text = tk.Text(root, height=10, width=50)
        self.answer_text.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_data)
        self.save_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next Case", command=self.load_next_case)
        self.next_button.pack()

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.root_path = file_path
            with open(file_path, "r") as file:
                self.json_data = json.load(file)
                self.current_case_id = None
                self.labeled_data = []
                self.load_next_case()

    def load_next_case(self):
        if self.json_data and not self.labeled_data and self.current_case_id is None:
            case_ids = list(self.json_data["cases"].keys())
            self.current_case_id = case_ids[0] if case_ids else None
        elif self.json_data and self.labeled_data and self.current_case_id:
            case_ids = list(self.json_data["cases"].keys())
            current_index = case_ids.index(self.current_case_id)
            next_index = (current_index + 1) % len(case_ids)
            self.current_case_id = case_ids[next_index]
        else:
            self.current_case_id = None

        self.load_case_content()

    def load_case_content(self):
        if self.json_data and self.current_case_id:
            case = self.json_data["cases"][self.current_case_id]
            self.case_text.delete("1.0", tk.END)
            self.question_text.delete("1.0", tk.END)
            self.answer_text.delete("1.0", tk.END)
            self.case_text.insert("1.0", json.dumps(case, indent=4))

    def save_data(self):
        if self.current_case_id:
            question = self.question_text.get("1.0", tk.END).strip()
            answer = self.answer_text.get("1.0", tk.END).strip()
            if question and answer:
                self.labeled_data.append({"question": question, "answer": answer})
                if len(self.labeled_data) < 2:
                    self.load_next_case()
                else:
                    self.save_labeled_data()

    def save_labeled_data(self):
        if self.labeled_data:
            save_path = os.path.join(os.path.dirname(self.root_path), "devzone_question_answer.json")
            with open(save_path, "w") as file:
                json.dump(self.labeled_data, file, indent=4)
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataLabelingApp(root)
    root.mainloop()
