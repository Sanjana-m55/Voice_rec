import streamlit as st
from PIL import Image
import numpy as np
import pyttsx3
import tempfile
import os
import logging

# Suppress the thread warnings
logging.getLogger('streamlit.runtime.scriptrunner.scriptrunner').setLevel(logging.ERROR)

# Initialize text-to-speech engine at startup
@st.cache_resource
def get_speech_engine():
    return pyttsx3.init()

def speak_text(text, engine):
    """Function to convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error with voice output: {str(e)}")

def analyze_image(image):
    """Basic image analysis using PIL and numpy"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    img_array = np.array(image)
    height, width, _ = img_array.shape
    avg_color = tuple(map(int, img_array.mean(axis=(0, 1))))
    brightness = int(np.mean(img_array))
    
    # Create a detailed description
    description = f"""
    This image has dimensions of {width} by {height} pixels.
    The average color is RGB{avg_color}.
    The overall brightness is {brightness} out of 255.
    The image format is {image.format or 'Unknown'} and uses {image.mode} color mode.
    """
    
    return {
        'dimensions': f"{width}x{height}",
        'average_color': f"RGB{avg_color}",
        'brightness': f"{brightness}/255",
        'format': image.format or 'Unknown',
        'mode': image.mode,
        'description': description.strip()
    }

def analyze_document(file):
    """Analyze document properties"""
    file_size = len(file.getvalue()) / 1024  # Convert to KB
    file_type = file.type
    file_name = file.name
    
    description = f"""
    This is a {file_type} document named {file_name}.
    The file size is {file_size:.2f} kilobytes.
    """
    
    return {
        'name': file_name,
        'type': file_type,
        'size': f"{file_size:.2f} KB",
        'description': description.strip()
    }

def main():
    st.title("Image and Document Analyzer with Voice Output")
    
    # Initialize speech engine
    engine = get_speech_engine()
    
    # Select analysis type
    analysis_type = st.radio("Select what to analyze:", ["Image", "Document"])
    
    if analysis_type == "Image":
        uploaded_file = st.file_uploader("Upload an Image", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file is not None:
            try:
                # Display image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                # Analysis buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Analyze Image"):
                        results = analyze_image(image)
                        
                        st.subheader("Image Analysis Results:")
                        st.write(f"• Dimensions: {results['dimensions']}")
                        st.write(f"• Average Color: {results['average_color']}")
                        st.write(f"• Brightness: {results['brightness']}")
                        st.write(f"• Image Format: {results['format']}")
                        st.write(f"• Color Mode: {results['mode']}")
                
                with col2:
                    if st.button("Speak Analysis"):
                        results = analyze_image(image)
                        st.success("Speaking analysis...")
                        speak_text(results['description'], engine)
                        
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
    
    else:
        uploaded_file = st.file_uploader("Upload a Document", type=['pdf', 'txt', 'doc', 'docx'])
        
        if uploaded_file is not None:
            try:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Analyze Document"):
                        results = analyze_document(uploaded_file)
                        
                        st.subheader("Document Analysis Results:")
                        st.write(f"• File Name: {results['name']}")
                        st.write(f"• File Type: {results['type']}")
                        st.write(f"• File Size: {results['size']}")
                
                with col2:
                    if st.button("Speak Analysis"):
                        results = analyze_document(uploaded_file)
                        st.success("Speaking analysis...")
                        speak_text(results['description'], engine)
                        
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

if __name__ == "__main__":
    main()
