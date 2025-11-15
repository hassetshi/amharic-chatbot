"""
Amharic Chatbot Module using Google Gemini
Handles Amharic text understanding and generation
"""

import google.generativeai as genai
from typing import List, Dict, Optional
import os


class AmharicChatbot:
    """Google Gemini-powered Amharic chatbot"""

    def __init__(self, api_key: str):
        """
        Initialize the Amharic chatbot

        Args:
            api_key: Google API key for Gemini
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_history: List[Dict] = []

    def generate_response(
        self,
        user_message: str,
        detection_context: Optional[str] = None
    ) -> str:
        """
        Generate an Amharic response to user message

        Args:
            user_message: User's message in Amharic or English
            detection_context: Optional context about detected objects

        Returns:
            Response in Amharic
        """
        # Build the prompt
        system_prompt = """አንت የአማርኛ ቻትቦት ነህ። ሁሉንም መልስህን በአማርኛ በግእዝ ፊደል መመለስ አለብህ።
You are an Amharic chatbot. You must respond ONLY in Amharic using Ge'ez script.
Be friendly, helpful, and culturally appropriate for Ethiopian users.
If you receive information about detected objects in an image, describe them naturally in Amharic.
"""

        # Add detection context if available
        if detection_context:
            prompt = f"""{system_prompt}

የምስል መረጃ (Image Detection Info): {detection_context}

የተጠቃሚ መልእክት (User Message): {user_message}

እባክህ በአማርኛ ግልጽ እና ተፈጥሯዊ መልስ ስጥ። (Please respond in clear and natural Amharic.)
"""
        else:
            prompt = f"""{system_prompt}

የተጠቃሚ መልእክት (User Message): {user_message}

እባክህ በአማርኛ መልስ። (Please respond in Amharic.)
"""

        try:
            # Generate response
            response = self.model.generate_content(prompt)

            # Extract response text
            response_text = response.text

            # Store in chat history
            self.chat_history.append({
                "user": user_message,
                "assistant": response_text,
                "detection_context": detection_context
            })

            return response_text

        except Exception as e:
            return f"ይቅርታ፣ ስህተት ተፈጥሯል: {str(e)}"

    def generate_image_description(self, detections: List[Dict]) -> str:
        """
        Generate Amharic description of detected objects

        Args:
            detections: List of detection dictionaries from object detector

        Returns:
            Amharic description of the image
        """
        if not detections:
            detection_info = "No objects were detected in the image."
        else:
            # Count objects
            object_counts = {}
            for det in detections:
                class_name = det["class"]
                object_counts[class_name] = object_counts.get(class_name, 0) + 1

            # Format detection info
            detection_parts = []
            for obj, count in object_counts.items():
                detection_parts.append(f"{count} {obj}(s)")

            detection_info = f"Detected objects: {', '.join(detection_parts)}"

        prompt = f"""በምስሉ ውስጥ የሚከተሉት ነገሮች ተገኝተዋል፡
{detection_info}

እባክህ ይህንን በተፈጥሯዊ አማርኛ በግእዝ ፊደል ግለጽ። ምስሉን በአጭሩ ግለጽ።
Please describe this in natural Amharic using Ge'ez script. Give a brief description of what's in the image.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"ይቅርታ፣ ስህተት ተፈጥሯል: {str(e)}"

    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []

    def get_history(self) -> List[Dict]:
        """Get chat history"""
        return self.chat_history
