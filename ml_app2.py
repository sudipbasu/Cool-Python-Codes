import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns


class MLGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Machine Learning Model Comparison")
        self.root.geometry("900x700")
        self.root.config(bg="#F0F0F0")

        # Variables
        self.file_path = None
        self.data = None
        self.selected_visualization = tk.StringVar()

        # Models dictionary
        self.models = {
            'Random Forest': RandomForestClassifier(),
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'SVM': SVC(),
            'Decision Tree': DecisionTreeClassifier()
        }
        self.results = {}

        # Title label
        self.title_label = tk.Label(root, text="Machine Learning Model Comparison", font=('Roboto', 18, 'bold'), bg="#E8EAF6", fg="#333", pady=20)
        self.title_label.pack()

        # Frame for buttons and dropdown
        control_frame = tk.Frame(root, bg="#E8EAF6")
        control_frame.pack(pady=20)

        # Upload button
        self.upload_button = tk.Button(control_frame, text="Upload CSV/Excel File", command=self.upload_file, font=('Roboto', 12, 'bold'), bg="#5C6BC0", fg="white", width=25, relief="flat")
        self.upload_button.grid(row=0, column=0, padx=20, pady=10)

        # Visualization dropdown
        visualization_label = tk.Label(control_frame, text="Select Visualization:", font=('Roboto', 12), bg="#E8EAF6")
        visualization_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.visualization_dropdown = ttk.Combobox(control_frame, textvariable=self.selected_visualization, state="readonly", width=22)
        self.visualization_dropdown['values'] = ["Correlation Heatmap", "Bar Plot", "Scatter Plot", "Histogram", "Pie Chart"]
        self.visualization_dropdown.grid(row=1, column=1, padx=10, pady=10)

        # Visualize button
        self.visualize_button = tk.Button(control_frame, text="Visualize Data", command=self.visualize_data, font=('Roboto', 12, 'bold'), bg="#5C6BC0", fg="white", width=25, relief="flat", state=tk.DISABLED)
        self.visualize_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Compare models button
        self.compare_button = tk.Button(control_frame, text="Compare ML Models", command=self.compare_models, font=('Roboto', 12, 'bold'), bg="#5C6BC0", fg="white", width=25, relief="flat", state=tk.DISABLED)
        self.compare_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Buttons for individual model accuracy
        button_frame = tk.Frame(root, bg="#E8EAF6")
        button_frame.pack(pady=20)

        self.rf_button = self.create_model_button(button_frame, "Random Forest Accuracy", "Random Forest")
        self.lr_button = self.create_model_button(button_frame, "Logistic Regression Accuracy", "Logistic Regression")
        self.svm_button = self.create_model_button(button_frame, "SVM Accuracy", "SVM")
        self.dt_button = self.create_model_button(button_frame, "Decision Tree Accuracy", "Decision Tree")

        # Table frame for showing results
        self.table_frame = tk.Frame(root, bg="#E8EAF6")
        self.table_frame.pack(pady=20)

    def create_model_button(self, parent, text, model_name):
        button = tk.Button(parent, text=text, font=('Roboto', 12, 'bold'), bg="#5C6BC0", fg="white", width=30, relief="flat", command=lambda: self.show_model_accuracy(model_name), state=tk.DISABLED)
        button.pack(pady=5)
        return button

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if not file_path:
            return
        try:
            if file_path.endswith(".csv"):
                self.data = pd.read_csv(file_path)
            else:
                self.data = pd.read_excel(file_path)
            self.file_path = file_path
            messagebox.showinfo("Success", "File uploaded successfully!")
            self.visualize_button.config(state=tk.NORMAL)
            self.compare_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {str(e)}")

    def visualize_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please upload a file first.")
            return

        try:
            visualization = self.selected_visualization.get()
            numeric_cols = self.data.select_dtypes(include=['number']).columns

            if visualization == "Correlation Heatmap":
                plt.figure(figsize=(10, 6))
                sns.heatmap(self.data[numeric_cols].corr(), annot=True, cmap="coolwarm")
                plt.title("Correlation Heatmap")
                plt.show()

            elif visualization == "Bar Plot":
                for col in numeric_cols[:1]:
                    plt.figure(figsize=(8, 6))
                    self.data[col].value_counts().head(10).plot(kind='bar', color='skyblue', title=f"Bar Graph for {col}")
                    plt.xlabel(col)
                    plt.ylabel("Count")
                    plt.show()

            elif visualization == "Scatter Plot" and len(numeric_cols) > 1:
                plt.figure(figsize=(8, 6))
                sns.scatterplot(data=self.data, x=numeric_cols[0], y=numeric_cols[1])
                plt.title(f"Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}")
                plt.xlabel(numeric_cols[0])
                plt.ylabel(numeric_cols[1])
                plt.show()

            elif visualization == "Histogram":
                for col in numeric_cols:
                    plt.figure(figsize=(8, 6))
                    self.data[col].plot(kind='hist', bins=20, color='orange', title=f"Histogram for {col}")
                    plt.xlabel(col)
                    plt.ylabel("Frequency")
                    plt.show()

            elif visualization == "Pie Chart":
                categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
                for col in categorical_cols[:1]:
                    plt.figure(figsize=(8, 6))
                    self.data[col].value_counts().plot(kind='pie', autopct='%1.1f%%', title=f"Pie Chart for {col}")
                    plt.ylabel('')
                    plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize data: {str(e)}")

    def compare_models(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please upload a file first.")
            return

        try:
            X = self.data.iloc[:, :-1]
            y = self.data.iloc[:, -1]

            if not pd.api.types.is_numeric_dtype(y):
                y = pd.factorize(y)[0]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

            for model_name, model in self.models.items():
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                self.results[model_name] = accuracy_score(y_test, predictions)

            self.display_results_table()

            messagebox.showinfo("Model Comparison", "Model accuracies calculated. Check the table below for details.")

            for button in [self.rf_button, self.lr_button, self.svm_button, self.dt_button]:
                button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare models: {str(e)}")

    def show_model_accuracy(self, model_name):
        if model_name in self.results:
            try:
                X = self.data.iloc[:, :-1]
                y = self.data.iloc[:, -1]

                if not pd.api.types.is_numeric_dtype(y):
                    y = pd.factorize(y)[0]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                model = self.models[model_name]
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)

                report = classification_report(y_test, predictions, output_dict=True)
                precision = report['weighted avg']['precision']
                recall = report['weighted avg']['recall']
                f1_score = report['weighted avg']['f1-score']
                accuracy = accuracy_score(y_test, predictions)

                cm = confusion_matrix(y_test, predictions)
                ConfusionMatrixDisplay(confusion_matrix=cm).plot(cmap="Blues")
                plt.title(f"Confusion Matrix for {model_name}")
                plt.show()

                metrics_message = (f"Model: {model_name}\n\n"
                                   f"Accuracy: {accuracy:.2f}\n"
                                   f"Precision: {precision:.2f}\n"
                                   f"Recall: {recall:.2f}\n"
                                   f"F1 Score: {f1_score:.2f}")
                messagebox.showinfo(f"{model_name} Evaluation Metrics", metrics_message)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to evaluate {model_name}: {str(e)}")

    def display_results_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.table_frame, columns=("Model", "Accuracy"), show="headings", height=5)
        tree.heading("Model", text="Model")
        tree.heading("Accuracy", text="Accuracy (%)")
        tree.column("Model", anchor="center", width=200)
        tree.column("Accuracy", anchor="center", width=150)

        for model_name, accuracy in self.results.items():
            tree.insert("", "end", values=(model_name, f"{accuracy * 100:.2f}"))

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MLGuiApp(root)
    app.run()
