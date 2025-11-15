"""
Multimodal Amharic Chatbot - Streamlit Application
Combines YOLOv8 object detection with Google Gemini for Amharic responses
"""

import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from utils.object_detector import ObjectDetector
from utils.amharic_chatbot import AmharicChatbot

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="የአማርኛ ቻትቦት | Amharic Chatbot",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #0E9F6E;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #065F46;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
    }
    .bot-message {
        background-color: #D1FAE5;
        border-left: 4px solid #0E9F6E;
    }
    .stButton>button {
        background-color: #0E9F6E;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .detection-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #F59E0B;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_models():
    """Initialize the object detector and chatbot (cached)"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ Google API Key not found. Please set GOOGLE_API_KEY in .env file")
        st.stop()

    detector = ObjectDetector(model_path="yolov8n.pt")
    chatbot = AmharicChatbot(api_key=api_key)

    return detector, chatbot


def main():
    """Main application function"""

    # Header
    st.markdown('<h1 class="main-header">🇪🇹 የአማርኛ ቻትቦት</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Multimodal Amharic Chatbot with Object Detection</p>', unsafe_allow_html=True)

    # Initialize models
    detector, chatbot = initialize_models()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Confidence threshold
        confidence = st.slider(
            "Detection Confidence",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Minimum confidence for object detection"
        )

        st.divider()

        st.header("ℹ️ About")
        st.markdown("""
        **Features:**
        - 🖼️ Upload images for object detection
        - 🔍 YOLOv8-powered detection
        - 💬 Chat in Amharic (አማርኛ)
        - 🤖 Google Gemini AI responses
        - 🇪🇹 Full Ge'ez script support
        """)

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            chatbot.clear_history()
            st.session_state.messages = []
            st.rerun()

    # Initialize session state for chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📤 Upload Image")

        # Image upload
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png"],
            help="Upload an image for object detection"
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

            # Detect button
            if st.button("🔍 Detect Objects", use_container_width=True):
                with st.spinner("Detecting objects..."):
                    # Run detection
                    annotated_image, detections = detector.detect(image, confidence=confidence)

                    # Store in session state
                    st.session_state.current_image = annotated_image
                    st.session_state.detections = detections

                    # Generate Amharic description
                    description = chatbot.generate_image_description(detections)
                    st.session_state.image_description = description

                st.success("✅ Detection complete!")
                st.rerun()

        # Display detection results
        if "current_image" in st.session_state:
            st.subheader("🎯 Detection Results")
            st.image(
                st.session_state.current_image,
                caption="Detected Objects",
                use_container_width=True
            )

            # Detection summary
            if st.session_state.detections:
                st.markdown('<div class="detection-box">', unsafe_allow_html=True)
                st.markdown(f"**Detected {len(st.session_state.detections)} object(s):**")
                for det in st.session_state.detections:
                    st.write(f"- {det['class']} ({det['confidence']:.0%})")
                st.markdown('</div>', unsafe_allow_html=True)

                # Show Amharic description
                if "image_description" in st.session_state:
                    st.markdown("**የምስል መግለጫ (Image Description):**")
                    st.info(st.session_state.image_description)

    with col2:
        st.subheader("💬 Chat in Amharic")

        # Chat container
        chat_container = st.container()

        # Display chat history
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(
                        f'<div class="chat-message user-message">👤 {message["content"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="chat-message bot-message">🤖 {message["content"]}</div>',
                        unsafe_allow_html=True
                    )

        # Chat input
        user_input = st.text_input(
            "Type your message in Amharic or English:",
            key="user_input",
            placeholder="ጤና ይስጥልኝ... (Hello...)"
        )

        if st.button("📨 Send", use_container_width=True) and user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Generate response with detection context if available
            detection_context = None
            if "detections" in st.session_state and st.session_state.detections:
                detection_context = detector.get_detection_summary(st.session_state.detections)

            with st.spinner("Generating response..."):
                response = chatbot.generate_response(user_input, detection_context)

            # Add bot response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Rerun to update chat
            st.rerun()

    # Footer
    st.divider()
    st.markdown(
        '<p style="text-align: center; color: #6B7280;">Made with ❤️ for Ethiopia | Powered by YOLOv8 & Google Gemini</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
