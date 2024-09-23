import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class Job:
    def __init__(self, title, company, location, dates):
        self.title = title
        self.company = company
        self.location = location
        self.dates = dates
        self.descriptions = []  # List to hold multiple descriptions

    def add_description(self, description):
        self.descriptions.append(description)

    def format(self):
        job_details = f"**{self.title}**\n{self.company}, {self.location}\n{self.dates}\n"
        for desc in self.descriptions:
            job_details += f"- {desc}\n"
        return job_details

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
        self.jobs = []

    def add_section(self, section):
        self.sections.append(section)

    def toggle_section(self, internal_name, is_active):
        for section in self.sections:
            if section.internal_name == internal_name:
                section.is_active = is_active
                break

    def add_job(self, job):
        self.jobs.append(job)

    def generate_experience_text(self):
        experience_text = ""
        for job in self.jobs:
            experience_text += job.format() + "\n"
        return experience_text

    def generate_resume_text(self):
        resume = ""
        for section in self.sections:
            resume += section.display()
        if self.jobs:
            resume += "**Experience**\n\n" + self.generate_experience_text()
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
st.title("Interactive Resume Builder")

# Resume Builder Instance
resume_builder = ResumeBuilder()

# Sidebar - Customizing Sections
st.sidebar.header("Customize Your Resume")

# Input sections from the user
professional_summary = st.text_area("Professional Summary", "Enter your professional summary here.")

# Create a section for adding multiple jobs with dynamic subcategories
st.subheader("Experience")
all_jobs = []

if 'jobs' not in st.session_state:
    st.session_state.jobs = []

with st.form("add_job"):
    job_title = st.text_input("Job Title")
    job_company = st.text_input("Company")
    job_location = st.text_input("Location")
    job_dates = st.text_input("Dates (e.g., Jan 2020 - Present)")
    description = st.text_area("Job Description", "Enter job description here.")
    add_job_button = st.form_submit_button("Add Job")

    if add_job_button and job_title and job_company and job_location and job_dates:
        new_job = Job(job_title, job_company, job_location, job_dates)
        new_job.add_description(description)
        st.session_state.jobs.append(new_job)
        st.success(f"Added job: {job_title} at {job_company}")

# Display added jobs and allow for additional descriptions
for job in st.session_state.jobs:
    st.subheader(f"{job.title} at {job.company}")
    if st.button(f"Remove {job.title}"):
        st.session_state.jobs.remove(job)
        st.experimental_rerun()
    with st.expander("Add more details"):
        new_detail = st.text_area("Additional Detail", "Type here...")
        if st.button("Add Detail", key=f"add_{job.title}"):
            job.add_description(new_detail)
            st.experimental_rerun()

# Sidebar - Create checkboxes for each section
resume_builder.add_section(ResumeSection("Professional Summary", professional_summary, "professional_summary"))

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
