import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Font Registration (Example with common fonts, add more as necessary)
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttf'))
pdfmetrics.registerFont(TTFont('Times-Roman', 'Times-Roman.ttf'))
addMapping('Arial', 0, 0, 'Arial')
addMapping('Helvetica', 0, 0, 'Helvetica')
addMapping('Times-Roman', 0, 0, 'Times-Roman')

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

class Job:
    def __init__(self, title, company, location, dates):
        self.title = title
        self.company = company
        self.location = location
        self.dates = dates
        self.descriptions = []

    def add_description(self, description):
        self.descriptions.append(description)

    def format(self):
        job_details = f"**{self.title}**\n{self.company}, {self.location}\n{self.dates}\n"
        for desc in self.descriptions:
            job_details += f"- {desc}\n"
        return job_details

class ResumeBuilder:
    def __init__(self):
        self.sections = []
        self.jobs = []

    def add_section(self, section):
        self.sections.append(section)

    def add_job(self, job):
        self.jobs.append(job)

    def generate_resume_text(self):
        resume = ""
        for section in self.sections:
            resume += section.display()
        if self.jobs:
            resume += "**Experience**\n\n" + self.format_jobs()
        return resume

    def format_jobs(self):
        return ''.join(job.format() for job in self.jobs)

def create_pdf(resume_text, font_name):
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    pdf_canvas.setFont(font_name, 12)  # Set the font here
    width, height = letter
    text_object = pdf_canvas.beginText(40, height - 40)
    
    for line in resume_text.split("\n"):
        if line.startswith("**"):
            text_object.setFont(font_name, 12, leading=14)
            text_object.textLine(line.replace("**", ""))
        else:
            text_object.setFont(font_name, 10, leading=12)
            text_object.textLine(line)
    pdf_canvas.drawText(text_object)
    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return buffer

# Streamlit Setup
st.title("Interactive Resume Builder")

# Resume Builder Instance
resume_builder = ResumeBuilder()

# Sidebar - Customizing Sections
st.sidebar.header("Customize Your Resume")

# User Inputs for Different Sections
sections = {
    "Professional Summary": st.text_area("Professional Summary", ""),
    "Education": st.text_area("Education", ""),
    "Certifications": st.text_area("Certifications", ""),
    "Awards": st.text_area("Awards", ""),
}

# Create a section for adding multiple jobs
st.subheader("Experience")
with st.form("add_job"):
    job_title = st.text_input("Job Title")
    job_company = st.text_input("Company")
    job_location = st.text_input("Location")
    job_dates = st.text_input("Dates (e.g., Jan 2020 - Present)")
    description = st.text_area("Job Description")
    add_job_button = st.form_submit_button("Add Job")

    if add_job_button and job_title and job_company and job_location and job_dates:
        new_job = Job(job_title, job_company, job_location, job_dates)
        new_job.add_description(description)
        resume_builder.add_job(new_job)

# Font selection for the resume
font_selection = st.sidebar.selectbox("Select Font", ["Arial", "Helvetica", "Times-Roman"])

# Add sections and jobs to the builder
for title, content in sections.items():
    resume_builder.add_section(ResumeSection(title, content, title.lower()))

# Display resume preview
st.header("Resume Preview")
resume_text = resume_builder.generate_resume_text()
st.markdown(resume_text)

# PDF generation button
if st.button("Download PDF"):
    pdf_buffer = create_pdf(resume_text, font_selection)
    st.download_button("Download Resume PDF", pdf_buffer, "resume.pdf", "application/pdf")
