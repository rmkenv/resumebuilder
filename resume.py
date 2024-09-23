import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class ResumeSection:
    def __init__(self, title, content, internal_name, is_active=True):
        self.title = title
        self.content = content
        self.internal_name = internal_name
        self.is_active = is_active

    def display(self):
        if self.is_active:
            return f"**{self.title}**\n\n{self.content}\n"
        return ""

class ResumeBuilder:
    def __init__(self):
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    def toggle_section(self, internal_name, is_active):
        for section in self.sections:
            if section.internal_name == internal_name:
                section.is_active = is_active
                break

    def generate_resume_text(self):
        resume = ""
        for section in self.sections:
            resume += section.display()
        return resume

def create_pdf(resume_text):
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text_object = pdf_canvas.beginText(40, height - 40)
    
    for line in resume_text.split("\n"):
        text_object.textLine(line)
        
    pdf_canvas.drawText(text_object)
    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return buffer

# Streamlit Setup
st.title("Generic Resume Builder")

# Resume Builder Instance
resume_builder = ResumeBuilder()

# Sidebar - Customizing Sections
st.sidebar.header("Customize Your Resume")

# Example of generic sections
sections = [
    {"title": "Professional Summary", "content": "This is the professional summary section.", "internal_name": "professional_summary"},
    {"title": "Experience", "content": "Details about work experience go here.", "internal_name": "experience"},
    {"title": "Education", "content": "Education details go here.", "internal_name": "education"},
    {"title": "Skills", "content": "A list of relevant skills go here.", "internal_name": "skills"},
    {"title": "Certifications", "content": "Certifications and relevant qualifications.", "internal_name": "certifications"},
    {"title": "Awards", "content": "Awards and recognitions can be listed here.", "internal_name": "awards"}
]

# Add sections to the resume builder
for section_data in sections:
    section = ResumeSection(
        section_data["title"],
        section_data["content"],
        section_data["internal_name"]
    )
    resume_builder.add_section(section)

# Sidebar - Create checkboxes for each section
for section in resume_builder.sections:
    is_active = st.sidebar.checkbox(f"Include {section.title}", value=section.is_active)
    resume_builder.toggle_section(section.internal_name, is_active)

# Generate and display the resume preview
st.header("Resume Preview")
resume_text = resume_builder.generate_resume_text()
st.markdown(resume_text)

# PDF generation button
if st.button("Download PDF"):
    pdf_buffer = create_pdf(resume_text)
    st.download_button("Download Resume PDF", pdf_buffer, "resume.pdf", "application/pdf")
