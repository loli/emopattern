from abc import ABCMeta, abstractmethod
from . import PromptGeneratorBase

class PromptGeneratorEmotions(PromptGeneratorBase):
    DEFAULT_PROMPT = "highly cinematic photo showing a scene from a dream, photography, film still, shot on kodak"
    EMOTIONS_VALID = [
        "Calmness",
        "Joy",
        "Amusement",
        "Anger",
        "Confusion",
        "Disgust",
        "Sadness",
        "Horror",
        "Surprise",
    ]    

    def get_emotion_descriptors(self, top_emotions):
        descriptors = {
            'calmness': 'serene landscapes, tranquil waters, soft pastel colors',
            'joy': 'vibrant colors, joyful scenes, smiling faces',
            'amusement': 'playful situations, humorous elements, light-hearted imagery',
            'anger': 'intense expressions, stormy skies, bold red and black colors',
            'confusion': 'abstract forms, puzzled expressions, chaotic compositions',
            'disgust': 'distasteful elements, unpleasant scenes, off-putting colors',
            'sadness': 'solitary figures, darker tones, rain',
            'horror': 'frightening scenes, dark shadows, elements of fear',
            'surprise': 'unexpected elements, contrasting colors, expressions of awe'
        }
        return '. '.join(descriptors[emotion.lower()] for emotion, _ in top_emotions if emotion.lower() in descriptors)
    
    @abstractmethod
    def get_prompt(
        self, emotions: dict[str, float], user_input: str | None = None
    ) -> str:
        """Return the prompt generated to the implemented strategy.

        Args:
            emotions: detected emotions in the format {emotion: score} where score in [0,1]
            user_input: user input that can be used to steer the prompt generation

        Returns:
            generated prompt, ready to be consumed by stable diffusion, prompt weighting supported

        """
        # Filter out invalid emotions and sort the remaining by values (scores)
        valid_emotions = {emotion: score for emotion, score in emotions.items() if emotion in self.EMOTIONS_VALID}
        sorted_emotions = sorted(valid_emotions.items(), key=lambda item: item[1], reverse=True)

        # Get the top two emotions
        top_two_emotions = sorted_emotions[:2]

        # Construct a response string with the top two emotions and their scores
        emotions_str = "Top two emotions: "
        for emotion, score in top_two_emotions:
            emotions_str += f"{emotion} ({score:.2f}), "

        # Remove the trailing comma and space
        emotions_str = emotions_str.strip(", ")
        
        # Check if user input is provided, else use default prompt
        prompt = user_input if user_input else self.DEFAULT_PROMPT
        
        # Enhance prompt with emotion-specific descriptors and scenarios
        emotion_descriptors = self.get_emotion_descriptors(top_two_emotions)
        prompt += f" | {emotions_str}. {emotion_descriptors}"

        return prompt


class TestPromptGenerator(PromptGeneratorBase):
    def get_prompt(self, emotions, user_input=None):
        return super().get_prompt(emotions, user_input)

# Create an instance of the test subclass
test_generator = TestPromptGenerator()

# Define a test case with a set of emotions and optional user input
test_emotions = {"Joy": 0.8, "Sadness": 0.6, "Amusement": 0.1}
test_user_input = "A scene from a magical forest"

# Call the get_prompt method and print the result
test_prompt = test_generator.get_prompt(test_emotions, test_user_input)
print("Generated Prompt:", test_prompt)