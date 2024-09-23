import streamlit as st
import json
import io
from docx import Document
from docx.shared import Inches
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ... [previous functions remain the same] ...

def edit_personal_info(data):
  st.subheader("Personal Information")
  data["personal_info"]["name"] = st.text_input("Name", data["personal_info"].get("name", ""))
  data["personal_info"]["email"] = st.text_input("Email", data["personal_info"].get("email", ""))
  data["personal_info"]["phone"] = st.text_input("Phone", data["personal_info"].get("phone", ""))  # New phone field
  data["personal_info"]["location"] = st.text_input("Location", data["personal_info"].get("location", ""))
  data["personal_info"]["linkedin"] = st.text_input("LinkedIn", data["personal_info"].get("linkedin", ""))
  data["personal_info"]["website"] = st.text_input("Website", data["personal_info"].get("website", ""))

def edit_professional_experience(data):
  st.subheader("Professional Experience")
  for i, job in enumerate(data["professional_experience"]):
      with st.expander(f"{job['title']} at {job['company']}"):
          job["title"] = st.text_input(f"Job Title", job["title"], key=f"job_title_{i}")
          job["company"] = st.text_input(f"Company", job["company"], key=f"job_company_{i}")
          job["location"] = st.text_input(f"Location", job["location"], key=f"job_location_{i}")
          job["start_date"] = st.text_input(f"Start Date", job["start_date"], key=f"job_start_date_{i}")
          job["end_date"] = st.text_input(f"End Date", job["end_date"], key=f"job_end_date_{i}")
          
          # Responsibilities section
          st.write("Responsibilities:")
          if "responsibilities" not in job:
              job["responsibilities"] = []
          
          for j, resp in enumerate(job["responsibilities"]):
              col1, col2, col3 = st.columns([3, 1, 0.5])
              with col1:
                  job["responsibilities"][j]["content"] = st.text_input(f"Responsibility {j+1}", resp.get("content", ""), key=f"job_resp_content_{i}_{j}")
              with col2:
                  job["responsibilities"][j]["internal_name"] = st.text_input(f"Internal Name (optional)", resp.get("internal_name", ""), key=f"job_resp_name_{i}_{j}")
              with col3:
                  if st.button("Delete", key=f"del_resp_{i}_{j}"):
                      job["responsibilities"].pop(j)
                      st.experimental_rerun()
          
          if st.button("Add Responsibility", key=f"add_resp_{i}"):
              job["responsibilities"].append({"content": "", "internal_name": ""})
              st.experimental_rerun()
  
  if st.button("Add New Job"):
      data["professional_experience"].append({
          "title": "",
          "company": "",
          "location": "",
          "start_date": "",
          "end_date": "",
          "responsibilities": []
      })

# ... [other functions remain the same] ...

def display_resume(data):
  st.header("Resume Preview")
  st.subheader(data['personal_info'].get('name', ''))
  st.write(f"Email: {data['personal_info'].get('email', '')}")
  st.write(f"Phone: {data['personal_info'].get('phone', '')}")  # New phone field
  st.write(f"Location: {data['personal_info'].get('location', '')}")
  st.write(f"LinkedIn: {data['personal_info'].get('linkedin', '')}")
  st.write(f"Website: {data['personal_info'].get('website', '')}")
  
  # ... [rest of the function remains the same] ...

def export_to_doc(data):
  doc = Document()
  
  # Personal Information
  doc.add_heading(data['personal_info'].get('name', ''), 0)
  doc.add_paragraph(f"Email: {data['personal_info'].get('email', '')}")
  doc.add_paragraph(f"Phone: {data['personal_info'].get('phone', '')}")  # New phone field
  doc.add_paragraph(f"Location: {data['personal_info'].get('location', '')}")
  doc.add_paragraph(f"LinkedIn: {data['personal_info'].get('linkedin', '')}")
  doc.add_paragraph(f"Website: {data['personal_info'].get('website', '')}")
  
  # ... [rest of the function remains the same] ...

def export_to_pdf(data):
  bio = io.BytesIO()
  doc = SimpleDocTemplate(bio, pagesize=letter)
  styles = getSampleStyleSheet()
  styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
  story = []

  # Personal Information
  story.append(Paragraph(data['personal_info'].get('name', ''), styles['Title']))
  story.append(Paragraph(f"Email: {data['personal_info'].get('email', '')}", styles['Normal']))
  story.append(Paragraph(f"Phone: {data['personal_info'].get('phone', '')}", styles['Normal']))  # New phone field
  story.append(Paragraph(f"Location: {data['personal_info'].get('location', '')}", styles['Normal']))
  story.append(Paragraph(f"LinkedIn: {data['personal_info'].get('linkedin', '')}", styles['Normal']))
  story.append(Paragraph(f"Website: {data['personal_info'].get('website', '')}", styles['Normal']))
  story.append(Spacer(1, 12))

  # ... [rest of the function remains the same] ...

# ... [main function remains the same] ...

if __name__ == "__main__":
  main()
