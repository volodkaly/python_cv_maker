import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


class CVMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customizable CV Maker")
        self.root.geometry("600x700")

        # User data dictionary with max lengths
        self.user_data = {
            "name": tk.StringVar(),
            "email": tk.StringVar(),
            "phone": tk.StringVar(),
            "education": tk.StringVar(),
            "experience": tk.StringVar(),
            "skills": tk.StringVar(),
        }

        self.profile_pic_path = None  # To store the profile picture path

        # Create the form
        self.create_form()

    def create_form(self):
        ttk.Label(self.root, text="Customizable CV Maker", font=("Arial", 16)).pack(pady=10)

        # Name
        self.create_limited_entry("Name:", "name", 40)

        # Email
        self.create_limited_entry("Email:", "email", 40)

        # Phone
        self.create_limited_entry("Phone:", "phone", 20)

        # Education
        self.create_limited_entry("Education (separate with commas):", "education", 200)

        # Experience
        self.create_limited_entry("Work Experience (separate with commas):", "experience", 200)

        # Skills
        self.create_limited_entry("Skills (separate with commas):", "skills", 200)

        # Add profile picture
        ttk.Button(self.root, text="Add Profile Picture", command=self.add_profile_picture).pack(pady=10)
        self.profile_pic_label = ttk.Label(self.root, text="No picture selected.")
        self.profile_pic_label.pack()

        # Generate button
        ttk.Button(self.root, text="Generate CV", command=self.generate_cv).pack(pady=20)

    def create_limited_entry(self, label_text, field_name, max_length):
        """Creates a labeled entry with input length validation."""
        ttk.Label(self.root, text=label_text).pack(anchor="w", padx=20, pady=5)
        
        validate_command = (self.root.register(self.validate_length), "%P", max_length)
        ttk.Entry(
            self.root,
            textvariable=self.user_data[field_name],
            validate="key",
            validatecommand=validate_command,
        ).pack(fill="x", padx=20)

    @staticmethod
    def validate_length(new_value, max_length):
        """Validates that the input does not exceed the maximum length."""
        return len(new_value) <= int(max_length)

    def add_profile_picture(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")],
            title="Select Profile Picture"
        )
        if file_path:
            self.profile_pic_path = file_path
            self.profile_pic_label.config(text=f"Selected: {file_path.split('/')[-1]}")

    def generate_cv(self):
        # Collect user data
        name = self.user_data["name"].get()
        email = self.user_data["email"].get()
        phone = self.user_data["phone"].get()
        education = self.user_data["education"].get().split(",")
        experience = self.user_data["experience"].get().split(",")
        skills = self.user_data["skills"].get().split(",")

        if not name or not email or not phone:
            messagebox.showerror("Error", "Name, Email, and Phone are required!")
            return

        # Save PDF
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save CV As"
        )
        if file_path:
            self.create_pdf(file_path, name, email, phone, education, experience, skills)
            messagebox.showinfo("Success", f"CV saved as {file_path}")

    def create_pdf(self, file_path, name, email, phone, education, experience, skills):
        pdf = canvas.Canvas(file_path, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        y = 750

        # Add profile picture if available
        if self.profile_pic_path:
            try:
                img = Image.open(self.profile_pic_path)
                img.thumbnail((100, 100))  # Resize image to fit in the PDF
                img_reader = ImageReader(img)
                pdf.drawImage(img_reader, 50, y - 100, width=100, height=100)
                y -= 120  # Adjust y-coordinate for text
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add profile picture: {e}")

        # Header
        pdf.drawString(50, y, f"Name: {name}")
        pdf.drawString(50, y - 20, f"Email: {email}")
        pdf.drawString(50, y - 40, f"Phone: {phone}")
        y -= 60

        # Education
        pdf.drawString(50, y, "Education:")
        y -= 20
        for edu in education:
            pdf.drawString(70, y, f"- {edu.strip()}")
            y -= 20

        # Experience
        pdf.drawString(50, y, "Work Experience:")
        y -= 20
        for exp in experience:
            pdf.drawString(70, y, f"- {exp.strip()}")
            y -= 20

        # Skills
        pdf.drawString(50, y, "Skills:")
        y -= 20
        for skill in skills:
            pdf.drawString(70, y, f"- {skill.strip()}")
            y -= 20

        # Save the PDF
        pdf.save()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CVMakerApp(root)
    root.mainloop()
