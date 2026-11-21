from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def add_slide(prs, layout_idx, title=None, bg_color=(15, 23, 42)): # Slate 900
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
    
    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)
    
    if title and slide.shapes.title:
        title_shape = slide.shapes.title
        title_shape.text = title
        title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(20, 184, 166) # Teal 500
        title_shape.text_frame.paragraphs[0].font.name = "Arial"
        title_shape.text_frame.paragraphs[0].font.bold = True
        title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
    return slide

def style_text(shape, color=(248, 250, 252)): # Slate 50
    if not shape.has_text_frame:
        return
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.color.rgb = RGBColor(*color)
            run.font.name = "Arial"

def create_ppt():
    prs = Presentation()
    
    # Slide 1: Title
    slide = add_slide(prs, 0)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "MediCheck"
    title.text_frame.paragraphs[0].font.color.rgb = RGBColor(2, 132, 199) # Sky 600
    title.text_frame.paragraphs[0].font.size = Pt(54)
    title.text_frame.paragraphs[0].font.bold = True
    
    subtitle.text = "Diagnostic Lab & Home Sample Collection System\n\nA Comprehensive Healthcare Platform"
    style_text(subtitle, color=(148, 163, 184)) # Slate 400
    
    # Slide 2: Team Details
    slide = add_slide(prs, 1, "Team Details")
    body_shape = slide.shapes.placeholders[1]
    tf = body_shape.text_frame
    tf.text = "Project Led By:"
    p = tf.add_paragraph()
    p.text = "• Shreya (Lead Developer)"
    style_text(body_shape)

    # Slide 3: Project Details
    slide = add_slide(prs, 1, "Project Details")
    body_shape = slide.shapes.placeholders[1]
    tf = body_shape.text_frame
    tf.text = "MediCheck is a seamless, full-stack platform designed to simplify diagnostic healthcare access."
    p = tf.add_paragraph()
    p.text = "Key Features:"
    p = tf.add_paragraph()
    p.text = "• Direct booking for walk-in lab tests and home sample collections."
    p = tf.add_paragraph()
    p.text = "• Staff Portal for Admins and Technicians to manage workflows."
    p = tf.add_paragraph()
    p.text = "• Dynamic PDF Report Generation."
    style_text(body_shape)

    # Slide 4: ER Diagram
    slide = add_slide(prs, 5, "Entity-Relationship Diagram")
    try:
        slide.shapes.add_picture("er_diagram.png", Inches(1.5), Inches(2.0), width=Inches(7))
    except Exception as e:
        print("Could not add ER Diagram:", e)

    # Slide 5: Webpage Screenshots (Home)
    slide = add_slide(prs, 5, "User Interface - Patient Portal")
    try:
        slide.shapes.add_picture("screenshot_home.png", Inches(1), Inches(1.5), width=Inches(8))
    except Exception as e:
        print("Could not add Home Screenshot:", e)

    # Slide 6: Webpage Screenshots (Admin)
    slide = add_slide(prs, 5, "User Interface - Staff Portal")
    try:
        slide.shapes.add_picture("screenshot_admin.png", Inches(1), Inches(1.5), width=Inches(8))
    except Exception as e:
        print("Could not add Admin Screenshot:", e)
        
    # Slide 7: Advantages & Disadvantages
    slide = add_slide(prs, 1, "Advantages & Disadvantages")
    body_shape = slide.shapes.placeholders[1]
    tf = body_shape.text_frame
    tf.text = "Advantages:"
    p = tf.add_paragraph()
    p.text = "• High accessibility for elderly and immobile patients (Home Collection)."
    p = tf.add_paragraph()
    p.text = "• Fully digitized, paperless workflow reducing manual errors."
    p = tf.add_paragraph()
    p.text = "• Streamlined staff management with role-based access."
    
    p = tf.add_paragraph()
    p.text = "\nDisadvantages & Mitigation:"
    p = tf.add_paragraph()
    p.text = "• Challenge: Logistics for scaling home collection fleet."
    p = tf.add_paragraph()
    p.text = "• Mitigation: Integrating map-based route optimization in the future."
    style_text(body_shape)

    # Slide 8: Future Scope
    slide = add_slide(prs, 1, "Future Scope")
    body_shape = slide.shapes.placeholders[1]
    tf = body_shape.text_frame
    tf.text = "The platform is designed to scale with future healthcare demands:"
    p = tf.add_paragraph()
    p.text = "• AI-driven Health Insights based on historical test reports."
    p = tf.add_paragraph()
    p.text = "• Integration with Smart Wearables for real-time vitals tracking."
    p = tf.add_paragraph()
    p.text = "• Multi-clinic franchising support."
    style_text(body_shape)

    # Slide 9: References
    slide = add_slide(prs, 1, "References")
    body_shape = slide.shapes.placeholders[1]
    tf = body_shape.text_frame
    tf.text = "Helpful Links & Tools:"
    p = tf.add_paragraph()
    p.text = "• html2pdf library (PDF generation engine)"
    p = tf.add_paragraph()
    p.text = "• Local Storage API documentation"
    p = tf.add_paragraph()
    p.text = "• Google Fonts (Outfit & Plus Jakarta Sans)"
    style_text(body_shape)
    
    prs.save("MediCheck_Presentation.pptx")
    print("Presentation created successfully.")

if __name__ == "__main__":
    create_ppt()
