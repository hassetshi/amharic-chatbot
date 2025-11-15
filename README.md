# 🇪🇹 Multimodal Amharic Chatbot

A beautiful web application that combines **YOLOv8 object detection** with **Google Gemini AI** to create an intelligent chatbot that understands and responds in **Amharic (አማርኛ)** using Ge'ez script.

## ✨ Features

- 🖼️ **Image Upload & Object Detection**: Upload images and detect objects using YOLOv8
- 🔍 **Real-time Object Detection**: Powered by state-of-the-art YOLOv8 model
- 💬 **Amharic Chat Interface**: Full support for Amharic text in Ge'ez script
- 🤖 **AI-Powered Responses**: Google Gemini generates fluent, natural Amharic responses
- 🎨 **Beautiful UI**: Clean, modern Streamlit interface with Ethiopian colors
- 🌐 **Multimodal Understanding**: Combines visual and textual information

## 🎯 Use Cases

- Educational tool for Ethiopian students learning about AI
- Accessibility tool for Amharic speakers
- Object recognition with Amharic descriptions
- Cultural heritage preservation through language technology
- Research and development in low-resource language NLP

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini)
- Webcam or image files for testing

## 🚀 Installation

### 1. Clone or download this project

```bash
cd amharic-chatbot
```

### 2. Create a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### 5. Configure environment variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# Replace 'your_google_api_key_here' with your actual API key
```

Your `.env` file should look like:
```
GOOGLE_API_KEY=AIzaSyD...your_actual_key...xyz
```

### 6. Download YOLOv8 model (automatic)

The YOLOv8 nano model will be automatically downloaded on first run. If you want to use a different model:

- `yolov8n.pt` - Nano (fastest, smallest)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (most accurate)

## 🎮 Usage

### Run the application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the chatbot

1. **Upload an image**:
   - Click "Browse files" in the left panel
   - Select an image (JPG, JPEG, or PNG)
   - Click "🔍 Detect Objects"

2. **View detection results**:
   - See the annotated image with bounding boxes
   - Read the detected objects list
   - View the Amharic description

3. **Chat in Amharic**:
   - Type your message in the chat input (Amharic or English)
   - The bot will respond in Amharic
   - Ask questions about the detected objects
   - Have natural conversations in Amharic

### Example conversations

**With image detection:**
```
User: ምን አይታ? (What do you see?)
Bot: በምስሉ ውስጥ 2 ሰዎች እና 1 መኪና አይቻለሁ። (I see 2 people and 1 car in the image.)
```

**General chat:**
```
User: ጤና ይስጥልኝ (Hello)
Bot: ጤና ይስጥልኝ! እንዴት ሊረዳሁ እችላለሁ? (Hello! How can I help you?)
```

## 📁 Project Structure

```
amharic-chatbot/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
├── README.md                  # This file
├── utils/
│   ├── object_detector.py     # YOLOv8 detection module
│   └── amharic_chatbot.py     # Google Gemini chatbot module
├── models/                    # Downloaded models (created on first run)
└── assets/                    # Images and other assets
```

## 🛠️ Configuration

### Detection Confidence

Adjust the confidence threshold in the sidebar:
- Lower values (0.1-0.3): Detect more objects, may include false positives
- Medium values (0.4-0.6): Balanced detection
- Higher values (0.7-1.0): Only high-confidence detections

### YOLOv8 Model

To change the YOLOv8 model, edit [app.py](app.py):

```python
detector = ObjectDetector(model_path="yolov8n.pt")  # Change to yolov8s.pt, etc.
```

## 🔧 Troubleshooting

### API Key Issues

**Error**: "Google API Key not found"
- Make sure `.env` file exists in the project root
- Check that `GOOGLE_API_KEY` is set correctly
- Verify there are no extra spaces or quotes

### Model Download Issues

**Error**: "Failed to download YOLOv8 model"
- Check your internet connection
- The model will auto-download on first use
- Manually download from [Ultralytics](https://github.com/ultralytics/ultralytics)

### Amharic Text Display

**Issue**: Amharic characters not displaying correctly
- Ensure your system has Ge'ez Unicode fonts installed
- Try browsers: Chrome, Firefox, or Edge (best support)
- On Windows: Install "Ebrima" or "Nyala" fonts

### Memory Issues

**Error**: Out of memory
- Use a smaller YOLOv8 model (`yolov8n.pt`)
- Resize large images before uploading
- Close other applications

## 🌟 Advanced Features

### Custom YOLOv8 Training

Train YOLOv8 on Ethiopian-specific objects:

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='ethiopian_objects.yaml', epochs=100)
```

### Extending the Chatbot

Add custom Amharic prompts in [utils/amharic_chatbot.py](utils/amharic_chatbot.py):

```python
system_prompt = """
Your custom Amharic instructions here...
እዚህ የራስዎን መመሪያዎች ይጨምሩ...
"""
```

## 📚 Technologies Used

- **Streamlit**: Web application framework
- **YOLOv8**: Object detection (Ultralytics)
- **Google Gemini**: Large language model for Amharic
- **Python-dotenv**: Environment variable management
- **Pillow**: Image processing
- **OpenCV**: Computer vision utilities

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add more Ethiopian languages (Oromo, Tigrinya, etc.)
- Improve Amharic natural language understanding
- Add voice input/output
- Create mobile app version
- Add more object detection models
- Improve UI/UX

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8
- [Google AI](https://ai.google.dev/) for Gemini API
- [Streamlit](https://streamlit.io/) for the amazing framework
- The Ethiopian tech community

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review [Google Gemini API docs](https://ai.google.dev/docs)
3. Check [YOLOv8 documentation](https://docs.ultralytics.com/)
4. Open an issue with detailed error messages

---

**Made with ❤️ for Ethiopia**

*ለኢትዮጵያ በፍቅር የተሰራ*
