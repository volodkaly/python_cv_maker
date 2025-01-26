import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


class CVMakerApp:
    def __init__(self, root):
        self.root = root
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.title("Customizable CV Maker")
        self.root.geometry(f"{int(0.5*screen_width)}x{int(0.5*screen_height)}+{int(0.25*screen_width)}+{int(0.25*screen_height)}")



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
        y = 750  # Starting y-coordinate for the content

        # Add profile picture if available
        if self.profile_pic_path:
            try:
                img = Image.open(self.profile_pic_path)

                # Crop the image to a square (centered crop)
                width, height = img.size
                min_dim = min(width, height)  # Use the smaller dimension
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2
                img = img.crop((left, top, right, bottom))

                # Resize the cropped image to fit in the PDF
                img.thumbnail((150, 150))
                img_reader = ImageReader(img)

                # Draw the image on the PDF
                pdf.drawImage(img_reader, 400, y - 150, width=150, height=150)
                y -= 120  # Adjust y-coordinate for text
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add profile picture: {e}")
        # Add user information with proper styling and spacing
        line_spacing = 30  # Space between lines

        # Name
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Name:")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(150, y, name.title())  # Indent value to align with title
        y -= line_spacing

        # Email
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Email:")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(150, y, email)
        y -= line_spacing

        # Phone
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Phone:")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(150, y, phone)
        y -= line_spacing

        # Education
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Education:")
        y -= line_spacing
        pdf.setFont("Helvetica", 14)
        for edu in education:
            pdf.drawString(70, y, f"- {edu.strip().title()}")
            y -= 20  # Smaller spacing for list items

        # Experience
        y -= 10  # Add some extra spacing before the next section
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Work Experience:")
        y -= line_spacing
        pdf.setFont("Helvetica", 14)
        for exp in experience:
            pdf.drawString(70, y, f"- {exp.strip().title()}")
            y -= 20

        # Skills
        y -= 10  # Add some extra spacing before the next section
        if any(skill.strip() for skill in skills):
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, y, "Skills:")
            y -= line_spacing
            pdf.setFont("Helvetica", 14)
            for skill in skills:
                pdf.drawString(70, y, f"- {skill.strip().title()}")
                y -= 20

        # Save the PDF
        pdf.save()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CVMakerApp(root)
    root.mainloop()
