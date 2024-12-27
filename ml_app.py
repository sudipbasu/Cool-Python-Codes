import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns

class MLGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Machine Learning Model Comparison")
        self.root.geometry("800x600")
        self.root.config(bg="#F0F0F0")

        # Variables
        self.file_path = None
        self.data = None

        # Fonts and Colors
        self.font = ('Roboto', 12)
        self.button_font = ('Roboto', 12, 'bold')
        self.bg_color = "#5C6BC0"  # Professional blue for buttons
        self.fg_color = "white"  # White text color
        self.hover_color = "#3F51B5"  # Darker blue for hover effect
        self.bg_gradient_start = "#FFFFFF"  # Soft white background
        self.bg_gradient_end = "#E8EAF6"  # Light blue gradient

        # Title label with gradient effect
        self.title_label = tk.Label(root, text="Machine Learning Model Comparison", font=('Roboto', 18, 'bold'), bg=self.bg_gradient_start, fg="#333", pady=20)
        self.title_label.pack()

        # Frame for buttons
        button_frame = tk.Frame(root, bg=self.bg_gradient_start)
        button_frame.pack(pady=40)

        # Upload button with icon and tooltip
        self.upload_button = self.create_button(button_frame, "Upload CSV/Excel File", self.upload_file, "Upload your data file")
        self.upload_button.grid(row=0, column=0, padx=25, pady=10)

        # Visualize button with icon and tooltip
        self.visualize_button = self.create_button(button_frame, "Visualize Data", self.visualize_data, "Visualize your dataset", state=tk.DISABLED)
        self.visualize_button.grid(row=1, column=0, padx=25, pady=10)

        # Compare Models button with icon and tooltip
        self.compare_button = self.create_button(button_frame, "Compare ML Models", self.compare_models, "Compare the performance of different models", state=tk.DISABLED)
        self.compare_button.grid(row=2, column=0, padx=25, pady=10)

        # Exit button with tooltip and custom style
        self.exit_button = self.create_button(button_frame, "Exit", self.root.quit, "Exit the application", bg="red", hover_color="#d32f2f")
        self.exit_button.grid(row=3, column=0, padx=25, pady=20)

    def create_button(self, parent, text, command, tooltip_text, state=tk.NORMAL, bg=None, hover_color=None):
        # Create a modern button with icon and hover effect
        button = tk.Button(parent, text=text, font=self.button_font, command=command, state=state,
                           bg=bg or self.bg_color, fg=self.fg_color, width=30, height=2, relief="flat", padx=15, pady=10, bd=2, highlightthickness=0)
        button.bind("<Enter>", lambda event, button=button, hover_color=hover_color or self.hover_color: button.config(bg=hover_color))
        button.bind("<Leave>", lambda event, button=button: button.config(bg=self.bg_color))
        
        # Tooltip
        button_tooltip = self.create_tooltip(button, tooltip_text)

        return button

    def create_tooltip(self, widget, text):
        tooltip = tk.Label(self.root, text=text, bg="yellow", fg="black", font=("Arial", 10, "italic"), padx=5, pady=5, relief="solid", bd=1, anchor="w")
        tooltip.place_forget()  # Initially hidden

        def show_tooltip(event):
            tooltip.place(x=event.x_root + 10, y=event.y_root + 10)

        def hide_tooltip(event):
            tooltip.place_forget()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

        return tooltip

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
            numeric_cols = self.data.select_dtypes(include=['number']).columns

            if len(numeric_cols) == 0:
                messagebox.showwarning("No Numeric Data", "No numeric columns available for visualization.")
                return

            # Correlation Heatmap
            plt.figure(figsize=(10, 6))
            sns.heatmap(self.data[numeric_cols].corr(), annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")
            plt.show()

            # Bar Plot
            for col in numeric_cols[:1]:  # Visualize the first numeric column
                plt.figure(figsize=(8, 6))
                self.data[col].value_counts().head(10).plot(kind='bar', color='skyblue', title=f"Bar Graph for {col}")
                plt.xlabel(col)
                plt.ylabel("Count")
                plt.show()

            # Scatter Plot
            if len(numeric_cols) > 1:
                plt.figure(figsize=(8, 6))
                sns.scatterplot(data=self.data, x=numeric_cols[0], y=numeric_cols[1])
                plt.title(f"Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}")
                plt.xlabel(numeric_cols[0])
                plt.ylabel(numeric_cols[1])
                plt.show()

            # Histogram
            for col in numeric_cols:
                plt.figure(figsize=(8, 6))
                self.data[col].plot(kind='hist', bins=20, color='orange', title=f"Histogram for {col}")
                plt.xlabel(col)
                plt.ylabel("Frequency")
                plt.show()

            # Pie Charts
            categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
            for col in categorical_cols[:1]:  # Limit to the first categorical column for clarity
                plt.figure(figsize=(8, 6))
                self.data[col].value_counts().plot(kind='pie', autopct='%1.1f%%', title=f"Pie Chart for {col}")
                plt.ylabel('')  # Hide the y-label for better aesthetics
                plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize data: {str(e)}")

    def compare_models(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please upload a file first.")
            return

        try:
            # Assume last column is the target
            X = self.data.iloc[:, :-1]
            y = self.data.iloc[:, -1]

            if not pd.api.types.is_numeric_dtype(y):
                y = pd.factorize(y)[0]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

            # Models to compare
            models = {
                'Random Forest': RandomForestClassifier(),
                'Logistic Regression': LogisticRegression(max_iter=1000),
                'SVM': SVC(),
                'Decision Tree': DecisionTreeClassifier()
            }

            results = {}
            for model_name, model in models.items():
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                results[model_name] = accuracy

            # Display results
            results_str = "\n".join([f"{name}: {accuracy:.2f}" for name, accuracy in results.items()])
            messagebox.showinfo("Model Comparison Results", results_str)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare models: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MLGuiApp(root)
    root.mainloop()
